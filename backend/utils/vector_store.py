import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'faiss_index')

def get_embeddings_model():
    """Returns the lightweight Google Cloud Embeddings model.
    Instantiated per request to avoid cross-thread client closure errors."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

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
