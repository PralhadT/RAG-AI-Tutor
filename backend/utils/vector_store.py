import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'faiss_index')

def get_embeddings_model():
    """Returns a local HuggingFace embeddings model (Free, no API key needed).
    Instantiated per request to avoid cross-thread client closure errors."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_and_save_vector_store(chunks, user_id):
    """
    Creates a FAISS vector store from text chunks and saves it locally.
    We append the user_id to the index path to keep user indices separate.
    """
    if not chunks:
        return False
        
    embeddings = get_embeddings_model()
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    # Save index uniquely for each user
    user_index_path = f"{FAISS_INDEX_PATH}_{user_id}"
    vector_store.save_local(user_index_path)
    return True

def load_vector_store(user_id):
    """
    Loads an existing FAISS vector store for a specific user.
    """
    user_index_path = f"{FAISS_INDEX_PATH}_{user_id}"
    index_file = os.path.join(user_index_path, "index.faiss")
    
    if not os.path.exists(user_index_path) or not os.path.exists(index_file):
        return None
        
    embeddings = get_embeddings_model()
    # allow_dangerous_deserialization is required for local FAISS loading
    vector_store = FAISS.load_local(user_index_path, embeddings, allow_dangerous_deserialization=True)
    return vector_store
