import os
from flask import Blueprint, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from utils.pdf_reader import extract_text_from_pdf
from utils.docx_reader import extract_text_from_docx
from utils.ppt_reader import extract_text_from_ppt
from utils.text_chunker import chunk_text
from utils.vector_store import create_and_save_vector_store

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'txt'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file_path, filename, user_id=None):
    """Extract text based on file extension."""
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(file_path, user_id=user_id)
    elif ext == 'docx':
        return extract_text_from_docx(file_path)
    elif ext == 'pptx':
        return extract_text_from_ppt(file_path)
    elif ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

@upload_bp.route('/', methods=['POST'])
def upload_file():
    """Handle file uploads from the dashboard."""
    if 'user_id' not in session:
        flash('Please login to upload files.', 'warning')
        return redirect(url_for('auth.login'))

    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('dashboard'))
        
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'warning')
        return redirect(url_for('dashboard'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_id = session.get('user_id')
        user_filename = f"{user_id}_{filename}"
        
        save_path = os.path.join(UPLOAD_FOLDER, user_filename)
        file.save(save_path)
        
        # Process the file for RAG
        try:
            from utils.rag_pipeline import clear_cache
            # 1. Extract text (pass user_id for image extraction)
            raw_text = extract_text(save_path, filename, user_id)
            
            # 2. Chunk text
            chunks = chunk_text(raw_text)
            
            # 3. Save to FAISS
            from utils.vector_store import load_vector_store
            existing_store = load_vector_store(user_id)
            if existing_store:
                existing_store.add_texts(chunks)
                user_index_path = os.path.join(os.path.dirname(__file__), '..', '..', f'faiss_index_{user_id}')
                existing_store.save_local(user_index_path)
            else:
                create_and_save_vector_store(chunks, user_id)
                
            clear_cache(user_id) # Invalidate memory cache so new chunks are loaded
                
            flash(f'File "{filename}" successfully uploaded and processed for AI Classroom!', 'success')
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'danger')
            
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid file type. Allowed types are PDF, DOCX, PPTX, TXT.', 'danger')
        return redirect(url_for('dashboard'))

@upload_bp.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Handle file deletion."""
    if 'user_id' not in session:
        flash('Please login to manage files.', 'warning')
        return redirect(url_for('auth.login'))
        
    user_id = session.get('user_id')
    user_filename = f"{user_id}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, user_filename)
    
    if os.path.exists(file_path):
        try:
            from utils.rag_pipeline import clear_cache
            os.remove(file_path)
            
            # Rebuild FAISS index from remaining files
            remaining_chunks = []
            for f in os.listdir(UPLOAD_FOLDER):
                if f.startswith(f"{user_id}_"):
                    curr_path = os.path.join(UPLOAD_FOLDER, f)
                    raw_text = extract_text(curr_path, f, user_id)
                    remaining_chunks.extend(chunk_text(raw_text))
            
            user_index_path = os.path.join(os.path.dirname(__file__), '..', '..', f'faiss_index_{user_id}')
            if remaining_chunks:
                create_and_save_vector_store(remaining_chunks, user_id)
            else:
                # If no files left, remove the index directory if it exists
                import shutil
                import stat
                
                def remove_readonly(func, path, _):
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                    
                if os.path.exists(user_index_path):
                    shutil.rmtree(user_index_path, onerror=remove_readonly)
            
            clear_cache(user_id) # Invalidate memory cache so old chunks are removed
                    
            flash(f'File "{filename}" deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting file: {str(e)}', 'danger')
    else:
        flash('File not found.', 'danger')
        
    return redirect(url_for('dashboard'))
