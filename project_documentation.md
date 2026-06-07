# AI Classroom RAG System
## Comprehensive Project Documentation

---

### 1. Project Title
**AI Classroom: A Retrieval-Augmented Generation (RAG) System for Smart Document Interaction and Automated Question Answering**

### 2. Abstract
The rapid digitization of educational content has led to an overwhelming amount of study material for students. Locating specific information within dense PDFs, PPTs, and Word documents is time-consuming and inefficient. The **AI Classroom RAG System** is an intelligent web application designed to solve this problem. Built using Python, Flask, LangChain, FAISS, and the Google Gemini API, this system allows students to upload their course materials and interact with them through a conversational AI tutor. Utilizing Retrieval-Augmented Generation (RAG), the system ensures that the AI answers questions *strictly* based on the uploaded documents, preventing hallucinations. The system features a modern, user-friendly interface with seven distinct answer generation modes (such as Detailed, Exam-ready, and MCQ generation), making it a comprehensive digital study companion.

### 3. Problem Statement
Students often struggle to efficiently extract relevant information from large volumes of unstructured study materials (PDFs, presentations, and documents) during exam preparation. Traditional keyword search tools (like Ctrl+F) lack contextual understanding and cannot answer complex conceptual questions. Furthermore, generic Large Language Models (LLMs) like ChatGPT or standard Gemini often hallucinate or provide generalized answers that may conflict with the student's specific university syllabus or textbook. There is a need for an intelligent system that can "read" a student's specific notes and act as a personalized tutor, answering questions strictly within the context of the provided curriculum.

### 4. Existing System
Currently, students rely on:
- Manual reading and highlighting of physical or digital notes.
- Standard document readers (Adobe Acrobat, Microsoft Word) which only offer basic keyword searching.
- General-purpose AI chatbots (like ChatGPT) which provide answers based on public internet data rather than the student's specific course materials, leading to unreliable or out-of-scope information.

### 5. Drawbacks of Existing System
1. **Time-Consuming:** Searching for specific topics across multiple documents takes immense time.
2. **Lack of Contextual Search:** Keyword searches fail if the exact word isn't used, even if the concept is discussed.
3. **AI Hallucinations:** General LLMs often invent facts or provide generic answers that are not applicable to the specific curriculum.
4. **No Custom Output Formats:** Standard tools cannot automatically generate MCQs, Viva questions, or concise bullet-point summaries from the text.

### 6. Proposed System
The proposed **AI Classroom RAG System** overcomes these drawbacks by creating a private, context-aware AI tutor. 
- The system extracts text from uploaded documents (PDF, DOCX, PPTX, TXT).
- It converts this text into mathematical vectors (embeddings) and stores them in a local FAISS vector database.
- When a user asks a question, the system retrieves only the most relevant text chunks from the database.
- It feeds this specific context to the Google Gemini LLM, instructing it to generate an answer based *only* on the provided text.
- It provides dynamic output formatting, allowing the user to request answers as MCQs, Exam Notes, or Simple explanations.

### 7. Objectives
- To develop a secure, authenticated web platform for students to manage their study materials.
- To implement text extraction algorithms for multiple file formats.
- To utilize LangChain and FAISS for efficient semantic searching.
- To integrate Google Gemini LLM for high-quality, context-restricted natural language generation.
- To provide a seamless, interactive chat interface with multiple pedagogical output modes.

### 8. Scope of Project
The project is scoped to function as a web-based educational tool. It handles personal document management and text-based QA. The scope includes text parsing, chunking, embedding generation (using local HuggingFace models for reliability), vector storage, and prompt engineering for the Gemini API. Future scope may include OCR for handwritten notes and audio-based interaction, though these are outside the current implementation.

### 9. System Requirements
#### Hardware Requirements
- **Processor:** Intel Core i5 / AMD Ryzen 5 or higher
- **RAM:** 8 GB minimum (16 GB recommended for local embedding processing)
- **Storage:** 500 MB of free disk space (for virtual environment, libraries, and FAISS indices)
- **Internet:** Active broadband connection (required for Gemini API calls)

#### Software Requirements
- **Operating System:** Windows 10/11, macOS, or Linux
- **Language:** Python 3.9+
- **Framework:** Flask (Web Framework)
- **Database:** SQLite3 (Relational), FAISS (Vector Database)
- **Web Technologies:** HTML5, CSS3, Vanilla JavaScript, Bootstrap 5
- **Key Libraries:** `langchain`, `langchain-google-genai`, `sentence-transformers`, `PyPDF2`, `python-docx`, `python-pptx`

---

### 10. Technology Stack
1. **Python:** The core programming language used for backend logic, chosen for its vast AI/ML ecosystem.
2. **Flask:** A lightweight WSGI web application framework used to build the routing and backend API.
3. **HTML/CSS/JS/Bootstrap:** Used to build a responsive, modern, and interactive frontend interface.
4. **LangChain:** A framework for developing applications powered by language models. It handles document loading, chunking, and pipeline routing.
5. **FAISS (Facebook AI Similarity Search):** A highly efficient library that allows quick searching of multimedia documents based on vector similarity.
6. **HuggingFace Embeddings:** Used locally to convert text chunks into high-dimensional vectors. (Used to ensure 100% reliable local processing without API rate limits).
7. **Google Gemini API (gemini-3.5-flash):** The core LLM used to read the retrieved context and generate intelligent, human-like responses.
8. **SQLite:** A C-language library that implements a small, fast, self-contained SQL database engine. Used for managing user accounts securely.

---

### 11. Detailed System Architecture

The architecture follows a modular, client-server model combined with a sophisticated RAG pipeline.

**Components:**
1. **Client (Browser):** Renders the UI, handles user input, and makes AJAX calls to the backend.
2. **Web Server (Flask):** Intercepts HTTP requests, handles session management, and routes requests to appropriate backend modules.
3. **Database Layer:**
   - *SQLite:* Stores user credentials and session data.
   - *File System:* Stores the raw uploaded study materials.
   - *FAISS Vector Store:* Stores mathematical representations (embeddings) of the document text.
4. **RAG Pipeline (LangChain):**
   - *Extractor:* Reads raw files.
   - *Splitter:* Breaks text into chunks.
   - *Embedder:* Converts chunks to vectors.
   - *Retriever:* Finds vectors similar to the user's question.
   - *Generator:* Formats the prompt and calls the Gemini API.

**Interaction:**
The user uploads a file via the browser. Flask saves the file and passes it to the Extractor. The text is chunked and embedded, then saved in FAISS. Later, when the user asks a question in the Chat UI, Flask sends the question to the RAG Pipeline. The pipeline embeds the question, queries FAISS for similar text, combines the text with the question into a prompt, and sends it to the Gemini API. The response is relayed back to the browser.

---

### 12. Complete Workflow

1. **Registration/Login:** The user creates an account. Passwords are securely hashed using `werkzeug.security`.
2. **Dashboard:** The user logs in and is presented with a dashboard showing their previously uploaded files.
3. **Upload:** The user uploads a new PDF. 
4. **Processing:** The system reads the PDF, chunks the text into 1000-character segments, converts them to vectors using `all-MiniLM-L6-v2`, and saves them to a unique FAISS index (`faiss_index_{user_id}`).
5. **Chat Interface:** The user opens the Chatbot and selects an "Answer Mode" (e.g., MCQ).
6. **Querying:** The user types "What is the definition of AI?".
7. **Retrieval:** The system converts this question into a vector, searches the FAISS database, and retrieves the top 4 most relevant text chunks from the user's PDF.
8. **Generation:** The system builds a prompt containing the retrieved chunks, the user's question, and the specific instructions for "MCQ Mode". It sends this to `gemini-3.5-flash`.
9. **Response:** The LLM generates the MCQs based *only* on the text chunks. The answer is displayed dynamically on the screen.

---

### 13. Data Flow Diagram (Level 0 - Context Diagram)

```text
                        +-------------------+
  User Credentials      |                   |   UI Views / Responses
----------------------->|                   |----------------------->
                        |   AI Classroom    |
  Study Materials       |    RAG System     |   Processed Answers
----------------------->|                   |----------------------->
                        |                   |
  Chat Questions        |                   |   Error Messages
----------------------->|                   |----------------------->
                        +-------------------+
                                  ^ |
                 Prompts/Context  | |  Generated Content
                                  | v
                        +-------------------+
                        | Google Gemini API |
                        +-------------------+
```

### 14. Data Flow Diagram (Level 1)

```text
[User] ---> (1.0 Auth Module) <---> [SQLite Database]
  |
  +-------> (2.0 Upload Module) ---> [Local File System]
                  |
                  v
            (3.0 Extractor & Chunker)
                  |
                  v
            (4.0 Embedding Module) ---> [FAISS Vector DB]
                  |
[User] ---> (5.0 Chat Module) <---------+
                  |
                  v
            (6.0 LLM Generation) <---> [Google Gemini API]
                  |
                  +---> [User UI]
```

### 15. Use Case Diagram Explanation
**Actors:** Student (User), Gemini API (System Actor).
**Use Cases:**
- *Register/Login:* User authenticates to the system.
- *Upload File:* User uploads a study document.
- *Delete File:* User removes a document (which triggers automatic FAISS index rebuilding).
- *Select Answer Mode:* User selects how the AI should format the response.
- *Ask Question:* User inputs a query.
- *Generate Answer:* System retrieves context and queries the Gemini API.

### 16. Activity Diagram Explanation
1. Start.
2. User logs in.
3. Decision: Upload File or Chat?
   - If Upload: Validate file type -> Extract Text -> Chunk Text -> Generate Embeddings -> Save to FAISS -> Return to Dashboard.
   - If Chat: Enter Question -> Select Mode -> Embed Question -> FAISS Similarity Search -> Build Prompt -> Call Gemini API -> Display Output.
4. End.

### 17. Sequence Diagram Explanation (Chat Flow)
1. **User** sends a POST request with `{question, mode}` to the **Flask Server**.
2. **Flask Server** calls `answer_question` in **RAG Pipeline**.
3. **RAG Pipeline** loads the **FAISS Vector Store**.
4. **FAISS** returns the top 4 similar text chunks.
5. **RAG Pipeline** formats the prompt and sends it to **Gemini API**.
6. **Gemini API** returns the generated text string.
7. **Flask Server** wraps the string in a JSON response and sends it to the **User Browser**.
8. **User Browser** updates the DOM using JavaScript.

---

### 18. Database Design
The application utilizes two distinct databases:
1. **Relational Database (SQLite):** Used for strict, structured data such as user credentials.
2. **Vector Database (FAISS):** Used for unstructured data (text embeddings) allowing for high-speed mathematical similarity searches in high-dimensional space.

### 19. Database Schema
**Table Name:** `users`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique ID for the user |
| `username` | TEXT | UNIQUE, NOT NULL | User's chosen display name |
| `password` | TEXT | NOT NULL | Securely hashed password string |

---

### 20. Folder Structure Explanation
```text
ai-classroom-rag-system/
│
├── backend/
│   ├── app.py                  # Main Flask application entry point
│   ├── models/                 # Database schema and queries
│   │   └── user_model.py
│   ├── routes/                 # API endpoint handlers (Controllers)
│   │   ├── auth_routes.py
│   │   ├── chat_routes.py
│   │   └── upload_routes.py
│   ├── utils/                  # Core logic and helper functions
│   │   ├── docx_reader.py
│   │   ├── pdf_reader.py
│   │   ├── ppt_reader.py
│   │   ├── rag_pipeline.py     # LLM and Prompt logic
│   │   ├── text_chunker.py
│   │   └── vector_store.py     # FAISS database logic
│   ├── templates/              # HTML Frontend templates
│   │   ├── base.html
│   │   ├── chat.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   └── register.html
│   └── static/                 # CSS, JS, Images
│
├── uploads/                    # Physical storage for uploaded files
├── faiss_index_{user_id}/      # Generated vector databases
├── requirements.txt            # Python dependencies
└── venv/                       # Virtual environment
```

---

### 21. Module Description

- **Authentication Module:** Handles secure access. It uses `werkzeug.security` to generate password hashes to ensure passwords are never stored in plain text.
- **File Upload Module:** Validates file extensions, secures filenames to prevent directory traversal attacks, and saves files uniquely identified by the `user_id`.
- **Text Extraction Module:** A collection of parsers (`PyPDF2`, `python-docx`, `python-pptx`) that strip out formatting and return raw strings of text.
- **Chunking Module:** Utilizes LangChain's `RecursiveCharacterTextSplitter`. It splits large text blocks into smaller, overlapping chunks (e.g., 1000 characters) to ensure context isn't lost across chunk boundaries.
- **Embedding Module:** Uses HuggingFace's `all-MiniLM-L6-v2` transformer model to convert text chunks into mathematical vectors.
- **Vector Database Module:** Manages the FAISS indices. It saves indices uniquely per user to ensure data privacy (User A cannot query User B's notes).
- **Retrieval Module:** Compares the user's question vector against the FAISS index to find the most mathematically similar text chunks.
- **Gemini Answer Generation Module:** Constructs a strict prompt utilizing the retrieved context and calls `gemini-3.5-flash` to generate the final human-readable response.
- **Chat Interface Module:** A dynamic HTML/JS frontend that handles asynchronous user inputs and renders responses (including converting markdown to HTML line breaks).

---

### 22. Detailed Python File Explanations

1. **app.py:** The core configuration file. It initializes the Flask app, sets up the secret key for session management, connects to the SQLite database, and registers the Blueprint routes (Auth, Upload, Chat).
2. **auth_routes.py:** Contains the `/login`, `/register`, and `/logout` endpoints. It handles form submission, database insertion, password verification, and session creation.
3. **upload_routes.py:** Contains the `/upload` endpoint. It saves files, triggers the extraction/chunking/embedding pipeline, and redirects the user. It also contains the `/delete` endpoint which removes files and dynamically rebuilds the FAISS index.
4. **chat_routes.py:** Contains the `/chat/ask` API endpoint. It receives JSON POST requests from the frontend, calls the RAG pipeline, and returns the LLM's answer as a JSON response.
5. **user_model.py:** Contains raw SQLite queries hidden behind Python functions (`create_user`, `get_user_by_username`, `init_db`) representing the Data Access Layer.
6. **pdf_reader.py / text_chunker.py:** Utility scripts. `pdf_reader.py` iterates through PDF pages to extract text. `text_chunker.py` uses Langchain splitters to manage string lengths securely.
7. **vector_store.py:** The bridge between our text and FAISS. It initializes the `HuggingFaceEmbeddings` model and handles `FAISS.from_texts()`, `save_local()`, and `load_local()`.
8. **rag_pipeline.py:** The intelligence hub. It contains `build_prompt(mode)` which houses the prompt engineering logic for the 7 different answer modes. It instantiates `ChatGoogleGenerativeAI(model="gemini-3.5-flash")` and executes the `invoke` command, ensuring the output is cast to a strict string format.

---

### 23. API Flow Explanation
When a user asks a question, the flow is strictly asynchronous:
1. Browser Javascript intercepts the form submit.
2. An async `fetch()` request sends a JSON payload `{"question": "...", "mode": "..."}` to `/chat/ask`.
3. The Flask server validates the session. If valid, it passes data to the Python pipeline.
4. The pipeline performs the heavy lifting (Vector Search + LLM API Call over HTTPS).
5. The pipeline returns a string.
6. Flask wraps the string: `jsonify({"answer": answer_string})`.
7. Javascript awaits the JSON, parses it, and dynamically injects the text into the DOM without refreshing the webpage.

### 24. Security Features
- **Password Hashing:** Utilizing `generate_password_hash` with `scrypt` or `pbkdf2`.
- **Session Management:** Cryptographically signed session cookies via Flask `secret_key`.
- **Directory Traversal Protection:** `secure_filename()` ensures uploaded files cannot overwrite system files.
- **Data Isolation:** User FAISS indices are separated by physical file paths (`faiss_index_{user_id}`). User A cannot access User B's index.
- **Prompt Injection Mitigation:** The prompt template strictly instructs the LLM: *"You must answer the student's question based ONLY on the provided context below. DO NOT use outside knowledge."*

### 25. Error Handling Strategy
- **Frontend:** `try-catch` blocks in Javascript ensure that if the API fails, a clean UI error message ("An error occurred. Please try again.") is shown, rather than breaking the application.
- **Backend:** File processing is wrapped in `try-except` blocks. If text extraction or embedding fails, Flask catches the exception and uses `flash()` to display a warning on the dashboard, preventing a 500 Server Error crash.
- **LLM Failsafe:** The `rag_pipeline.py` specifically catches exceptions during LLM invocation and returns a formatted string containing the error, allowing the user to see what went wrong (e.g., API key issues).

---

### 26. Advantages
- **Highly Accurate:** Answers are strictly based on the uploaded syllabus, eliminating generic hallucinations.
- **Time Saving:** Instantly finds answers in 500-page textbooks.
- **Pedagogical Flexibility:** Allows students to generate MCQs or Viva questions instantly to test themselves.
- **Data Privacy:** Local embedding generation means raw document text isn't constantly sent to third-party APIs during the indexing phase.

### 27. Limitations
- **Format Dependency:** Highly complex PDFs with nested tables or multi-column layouts may not extract perfectly cleanly.
- **Context Window:** The system retrieves the top 4 chunks. If an answer spans 10 different pages, the LLM might only receive partial context.
- **No Image Recognition:** Currently, diagrams and images inside PDFs and PPTs are ignored.

### 28. Future Enhancements
- **OCR Integration:** Implement Tesseract OCR to read scanned PDFs and images.
- **Multi-modal LLMs:** Send images to Gemini to explain diagrams.
- **Global Knowledge Toggle:** Allow the user to toggle a switch that lets the AI search the web if the answer isn't in their notes.
- **Progress Tracking:** Save the generated MCQs and track the student's quiz scores over time.

---

### 29. Testing Strategy
- **Unit Testing:** Individual testing of the text extraction algorithms (e.g., ensuring `pdf_reader.py` returns a string for a valid PDF and handles empty PDFs gracefully).
- **Integration Testing:** Ensuring the FAISS database correctly links to the LangChain retriever.
- **System Testing:** Uploading a document, waiting for processing, and asking a question via the UI to test the complete end-to-end flow.
- **Stress Testing:** Uploading a large textbook (1000+ pages) to verify chunking and embedding memory limits.

### 30. Sample Test Cases

| Test Case ID | Description | Expected Output | Status |
|---|---|---|---|
| TC_01 | User logs in with incorrect password | "Invalid credentials" error flashed | PASS |
| TC_02 | User uploads `.exe` file | "Invalid file type" error flashed | PASS |
| TC_03 | User uploads valid PDF | File saved, FAISS index updated | PASS |
| TC_04 | User asks question not in notes | AI responds "I cannot answer this..." | PASS |
| TC_05 | User deletes file | File removed, FAISS index rebuilt | PASS |

### 31. Results and Output Screens
*(For the physical report, include screenshots here)*
- **Figure 1:** Login and Registration Screen demonstrating secure access.
- **Figure 2:** User Dashboard showing the list of successfully uploaded files and the "Delete" action buttons.
- **Figure 3:** The Chatbot interface demonstrating the "MCQ Generator" Answer Mode successfully creating a quiz from the uploaded text.
- **Figure 4:** The Chatbot interface demonstrating a successful RAG response to a direct question.

### 32. Conclusion
The AI Classroom RAG System successfully demonstrates the integration of modern NLP techniques with traditional web development. By combining Flask, FAISS, and the Gemini API, the system provides a robust solution to the problem of information overload in education. It transforms static documents into an interactive, intelligent tutor. The project meets all proposed objectives, offering a secure, user-friendly, and highly accurate educational tool suitable for university-level deployment.

### 33. References
1. Google Generative AI Documentation: https://ai.google.dev/docs
2. LangChain Official Documentation: https://python.langchain.com/
3. FAISS (Facebook AI Similarity Search) Repository: https://github.com/facebookresearch/faiss
4. Flask Web Development framework: https://flask.palletsprojects.com/
5. HuggingFace Sentence Transformers: https://sbert.net/

---
*Prepared by Antigravity (Senior Software Architect)*
