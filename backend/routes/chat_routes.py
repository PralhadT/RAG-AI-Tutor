from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from utils.rag_pipeline import answer_question

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['GET'])
def chat_page():
    """Render the chat interface with user files."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    import os
    user_id = str(session.get('user_id'))
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
    
    user_files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.startswith(user_id + '_'):
                display_name = filename[len(user_id) + 1:]
                user_files.append(display_name)
                
    return render_template('chat.html', files=user_files)

@chat_bp.route('/ask', methods=['POST'])
def ask():
    """API endpoint to handle chat messages."""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    # Handle form data (multipart/form-data) instead of JSON
    question = request.form.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
        
    mode = request.form.get('mode', 'Simple')
    custom_instruction = request.form.get('custom_instruction', '').strip()
    user_id = session.get('user_id')
    
    # Handle File Upload in Chat
    file = request.files.get('file')
    extracted_assignment_text = ""
    if file and file.filename != '':
        import os
        from werkzeug.utils import secure_filename
        from routes.upload_routes import extract_text, ALLOWED_EXTENSIONS
        
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext in ALLOWED_EXTENSIONS or ext in ['png', 'jpg', 'jpeg']:
            # Save it temporarily
            temp_filename = secure_filename(file.filename)
            temp_path = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', f"temp_chat_{user_id}_{temp_filename}")
            file.save(temp_path)
            
            try:
                if ext in ['png', 'jpg', 'jpeg']:
                    from utils.vision_helper import get_image_description
                    extracted_assignment_text = get_image_description(temp_path)
                else:
                    extracted_assignment_text = extract_text(temp_path, temp_filename, user_id)
            except Exception as e:
                print(f"Chat extraction error: {e}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            if extracted_assignment_text:
                # Don't append to question, pass it as extra context instead
                pass

    answer = answer_question(user_id, question, mode, custom_instruction, extracted_assignment_text)
    
    return jsonify({'answer': answer})
