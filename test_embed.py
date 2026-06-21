import os
from dotenv import load_dotenv
load_dotenv
import google.generativeai as genai

def list_models():
    for m in genai.list_models():
        if 'embedContent' in m.supported_generation_methods:
            print(f"Model: {m.name}")

if __name__ == "__main__":
    list_models()
 
