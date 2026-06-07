import os
os.environ['GOOGLE_API_KEY'] = 'fake_key'

from langchain_google_genai import GoogleGenerativeAIEmbeddings

e1 = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
print("e1.model:", e1.model)

e2 = GoogleGenerativeAIEmbeddings(model="text-embedding-004")
print("e2.model:", e2.model)
