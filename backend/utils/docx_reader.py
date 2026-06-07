import io
import docx

def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX file.
    """
    text = ""
    try:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
            
        doc = docx.Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            if para.text:
                text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        
    return text
