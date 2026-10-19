import os
import warnings
import PIL.Image

warnings.filterwarnings("ignore", category=FutureWarning)

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

    prompt = (
        "You are an OCR and Image Analysis expert. Describe this image, graph, or diagram in extreme detail. "
        "CRITICAL: You MUST transcribe EVERY SINGLE WORD of text visible in the image word-for-word exactly as it appears. "
        "If it is a list of questions, an assignment, or a document, transcribe the entire text perfectly. "
        "Also describe any visual elements, axes labels, numbers, and key takeaways so that it can be used for search retrieval."
    )

    # First try using google.genai Client (current standard)
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        with PIL.Image.open(image_path) as img:
            for model_name in ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-2.5-flash"]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[prompt, img]
                    )
                    if response.text:
                        return response.text
                except Exception as m_err:
                    print(f"Vision model {model_name} failed: {m_err}")
                    continue
    except Exception as e:
        print(f"google.genai client error: {e}")

    # Fallback to legacy google.generativeai if available
    try:
        import google.generativeai as legacy_genai
        legacy_genai.configure(api_key=api_key)
        for model_name in ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]:
            try:
                model = legacy_genai.GenerativeModel(model_name)
                with PIL.Image.open(image_path) as img:
                    response = model.generate_content([prompt, img])
                    if response.text:
                        return response.text
            except Exception as leg_err:
                continue
    except Exception as e:
        pass

    return "Image description unavailable due to API error."
