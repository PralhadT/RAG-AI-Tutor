import os
import fitz # PyMuPDF
from utils.vision_helper import get_image_description

def extract_text_from_pdf(file_path, user_id=None):
    """
    Extract text and images from a PDF file using PyMuPDF.
    """
    text = ""
    try:
        # Create user image directory
        img_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'extracted_images')
        if user_id:
            img_dir = os.path.join(img_dir, str(user_id))
        os.makedirs(img_dir, exist_ok=True)
        
        doc = fitz.open(file_path)
        base_filename = os.path.basename(file_path).replace(".pdf", "")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            # 1. Extract raw text
            text += page.get_text() + "\n"
            
            # 2. Extract images
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                width = base_image.get("width", 0)
                height = base_image.get("height", 0)
                
                # Skip tiny images (e.g. icons, bullet points, decorative lines) to massively speed up uploads
                if width < 150 or height < 150:
                    continue
                
                image_filename = f"{base_filename}_p{page_num}_i{img_index}.{image_ext}"
                image_path = os.path.join(img_dir, image_filename)
                
                # Save the image
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                    
                # Get AI description
                print(f"Sending {image_filename} (Size: {width}x{height}) to Vision AI...")
                description = get_image_description(image_path)
                
                # Create the special tag for the Frontend to render
                relative_path = f"/static/extracted_images/{user_id}/{image_filename}" if user_id else f"/static/extracted_images/{image_filename}"
                text += f"\n[IMAGE_START]{relative_path}[IMAGE_END]\nImage Description: {description}\n"
                
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    
    return text
