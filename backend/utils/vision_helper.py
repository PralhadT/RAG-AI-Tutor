import os
import warnings

# Suppress the massive FutureWarning from the old Google SDK
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
import PIL.Image

def encode_image(image_path):
    """Encodes an image to base64. Maintained for legacy compatibility."""
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(image_path):
    """
    Sends the image to Gemini's Vision model and returns a detailed description.
    """
    import time

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "Image description unavailable: GOOGLE_API_KEY not set."

    for attempt in range(3):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')  # fixed: was 'gemini-flash-latest'

            with PIL.Image.open(image_path) as img:
                prompt = "You are an OCR and Image Analysis expert. Describe this image, graph, or diagram in extreme detail. CRITICAL: You MUST transcribe EVERY SINGLE WORD of text visible in the image word-for-word exactly as it appears. If it is a list of questions, an assignment, or a document, transcribe the entire text perfectly. Also describe any visual elements, axes labels, numbers, and key takeaways so that it can be used for search retrieval."
                response = model.generate_content([prompt, img])
                return response.text

        except Exception as e:
            err_str = str(e)
            print(f"Error calling Gemini Vision API (Attempt {attempt+1}/3): {err_str}")
            if "429" in err_str or "exhausted" in err_str.lower() or "quota" in err_str.lower():
                time.sleep(5 * (attempt + 1))  # Exponential backoff
            else:
                return f"Image description unavailable due to API error."

    return "Image description unavailable due to API rate limit."
