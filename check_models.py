import os
import google.generativeai as genai

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY is not set in this terminal.")
    exit()

try:
    genai.configure(api_key=api_key)
    print("Available Models for your API Key:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print("Error connecting to Google API:", str(e))
