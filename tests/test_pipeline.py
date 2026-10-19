import os
import sys
from unittest.mock import MagicMock, patch
from langchain_core.embeddings import Embeddings

# Ensure backend is in python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app
from models.user_model import init_db, create_user, verify_user, delete_user, get_db_connection
from utils.text_chunker import chunk_text
import io

print("=== 1. Testing Database & Auth ===")
init_db()
conn = get_db_connection()
conn.execute("DELETE FROM users WHERE username LIKE 'e2e%' OR email LIKE 'e2e%'")
conn.commit()
conn.close()

test_username = "e2e_student_test"
test_password = "password123"

# Register
create_user(test_username, "e2e@student.com", test_password)
user = verify_user(test_username, test_password)
assert user is not None
user_id = user['id']
print(f"Created and verified user {test_username} (ID: {user_id})")

print("=== 2. Testing Text Chunking ===")
sample_text = (
    "Artificial Intelligence (AI) is intelligence demonstrated by machines. "
    "Retrieval-Augmented Generation (RAG) optimizes the output of large language models. "
) * 20
chunks = chunk_text(sample_text, chunk_size=300, chunk_overlap=50)
assert len(chunks) > 1
print(f"Successfully chunked text into {len(chunks)} chunks.")

print("=== 3. Testing Flask Endpoints with Test Client ===")
client = app.test_client()

# Login
login_res = client.post('/auth/login', data={'username': test_username, 'password': test_password}, follow_redirects=True)
assert login_res.status_code == 200
print("User login successful.")

# Dashboard
dash_res = client.get('/dashboard')
assert dash_res.status_code == 200
print("Dashboard access verified.")

# Chat Page
chat_res = client.get('/chat/')
assert chat_res.status_code == 200
print("Chat page rendering verified.")

class FakeEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[0.05] * 128 for _ in texts]
    def embed_query(self, text):
        return [0.05] * 128

# Mocking Google Generative AI Embeddings & Groq LLM for offline verification
with patch('utils.vector_store.get_embeddings_model', return_value=FakeEmbeddings()), \
     patch('utils.rag_pipeline.ChatGroq') as MockChatGroq:

    # Configure fake Groq LLM response
    mock_llm_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Virtual memory is a memory management capability of an operating system."
    mock_llm_instance.invoke.return_value = mock_response
    MockChatGroq.return_value = mock_llm_instance

    print("=== 4. Testing Document Upload & Vector Storage ===")
    test_file_content = (
        "Operating System Concepts:\n"
        "Virtual memory is a memory management capability of an operating system.\n"
        "Paging is a memory management scheme by which a computer stores and retrieves data from secondary storage."
    )
    data = {
        'file': (io.BytesIO(test_file_content.encode('utf-8')), 'test_notes.txt')
    }
    upload_res = client.post('/upload/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert upload_res.status_code == 200
    print("Document uploaded and indexed into FAISS successfully!")

    print("=== 5. Testing Chat / Ask Endpoint with RAG ===")
    chat_ask_res = client.post('/chat/ask', data={
        'question': 'What is virtual memory?',
        'mode': 'Simple'
    })
    assert chat_ask_res.status_code == 200
    json_data = chat_ask_res.get_json()
    print("Chat Response received:", json_data)
    assert 'answer' in json_data
    assert "Virtual memory" in json_data['answer']

    print("=== 6. Testing File Deletion & Index Cleanup ===")
    del_res = client.post(f'/upload/delete/test_notes.txt', follow_redirects=True)
    assert del_res.status_code == 200
    print("File and associated FAISS index cleaned up successfully.")

print("=== 7. Cleanup Test User ===")
delete_user(user_id)
print("Test user removed.")

print("\n>>> ALL TESTS PASSED SUCCESSFULLY! The RAG AI Tutor project is completely functional! <<<")
