import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

FAISS_INDEX_PATH = "faiss_index_1" # user 1
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if os.path.exists(FAISS_INDEX_PATH):
    vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    doc_count = vector_store.index.ntotal
    print(f"FAISS Index contains {doc_count} chunks.")
    
    # Let's peek at the actual documents
    doc_dict = vector_store.docstore._dict
    print("Sample content from chunks:")
    for i, (k, v) in enumerate(doc_dict.items()):
        if i < 5: # Print first 5 chunks
            print(f"- {v.page_content[:100]}...")
else:
    print("FAISS index not found.")
