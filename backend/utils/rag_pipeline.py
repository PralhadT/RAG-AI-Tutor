import os
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from utils.vector_store import load_vector_store

def get_llm():
    """Returns the Groq language model instance for ultra-fast generation."""
    # Switched to Mixtral 8x7b to bypass the exhausted Llama 3 70B daily token limit
    return ChatGroq(model_name="mixtral-8x7b-32768", temperature=0.3, max_tokens=8000)

def build_prompt(mode, custom_instruction=""):
    """
    Builds a prompt template based on the selected answer mode.
    The AI must answer ONLY from the uploaded content.
    """
    base_instructions = """
    You are an AI Classroom Tutor. Your ONLY source of knowledge is the uploaded study material provided in the context below.
    If the context does not contain the answer, strictly reply: "I cannot answer this based on the uploaded notes."
    
    IMPORTANT INSTRUCTION: If the attached file, image, or context contains MULTIPLE questions, you MUST explicitly address and answer EVERY SINGLE QUESTION. Do not summarize or just pick one. Provide separate, clear answers for each distinct question found.
    
    If the context contains an image description and a tag like [IMAGE_START]/path/to/img.png[IMAGE_END], and you use that information to answer the question, you MUST include the exact [IMAGE_START]...[IMAGE_END] tag somewhere in your final answer so the student can see the graph/image.
    
    Context:
    {context}
    
    Question: {question}
    """
    
    mode_instructions = {
        "Simple": """Provide a single, one-liner explanation in very simple, beginner-friendly terms. Your answer for each topic MUST be exactly one sentence.
If there are multiple questions, format your output professionally using Markdown:

**Q: [Question Text]**

[Exactly one sentence simple explanation]

CRITICAL: DO NOT use large headers like # or ##. Only use **bold text** for the questions.
CRITICAL: You MUST place a blank line between the Question and the Answer. Do not write the answer on the same line as the question.
""",
        "Exam": """You are an expert academic answer-writing assistant.
Generate answers strictly from the retrieved context.

CRITICAL REQUIREMENT: Your answer MUST start with the 'Introduction' or 'Definition' of the topic, and it MUST end with a 'Conclusion'.

Answer Format:

# Topic Name

## Introduction / Definition
Provide a concise introduction and definition of the topic.

## Detailed Explanation
Explain all concepts thoroughly using headings and subheadings.

## Features / Components / Steps
Use numbered points where applicable.

## Advantages
List advantages if present.

## Limitations
List limitations if present.

## Applications
List applications if present.

## Conclusion
Provide a concise exam-oriented conclusion. This MUST be the final section.

Rules:
- You ARE AUTHORIZED to use your internal academic knowledge to elaborate on the specific topic asked, but keep the explanation concise and exam-focused.
- STAY STRICTLY ON TOPIC. Do not explain terms, concepts, or facts that are not directly related to the specific question being asked, even if they appear in the notes.
- CRITICAL: Ensure the answer is concise, punchy, and formatted perfectly for a time-limited exam. Do not write excessively long paragraphs; prioritize clarity and structure over extreme length.
- If there are multiple questions, DO NOT STOP EARLY. You must provide a complete answer for every single question.
- Prioritize completeness, clarity, and academic presentation.""",
        "Detailed": """You are an expert academic tutor and subject-matter educator.
Your task is to answer questions based on the retrieved context provided.

Instructions:
1. You ARE ENCOURAGED AND AUTHORIZED to use your extensive internal academic knowledge to fully expand upon the concepts requested. Elaborate heavily to ensure the student gets a complete, master-level explanation.
2. CRITICAL: STAY STRICTLY ON TOPIC. Do not explain unrelated terms or concepts that are not directly relevant to the answer.
3. Do not contradict the retrieved context.

4. Structure every answer as follows:
# Topic Title
## Introduction
- Introduce the topic, purpose, or role.
## Core Concept / Definition
- Explain the main idea in detail and define important terminology.
## Detailed Explanation
- Break the topic into logical sections. Explain each section thoroughly.
## Working / Process / Methodology (if applicable)
- Present step-by-step explanations.
## Components / Features (if applicable)
- Explain each component individually.
## Advantages / Benefits (if available)
- Explain each point in detail.
## Limitations / Challenges (if available)
- Explain each point in detail.
## Applications / Use Cases (if available)
- Explain practical relevance.
## Important Points for Examination
- Summarize key concepts.
## Conclusion
- Provide a concise but meaningful summary.

5. Use formal academic language and preserve terminology.
6. Use headings, subheadings, numbered lists, and bullet points.
7. Use tables whenever comparisons improve clarity.
8. Explain concepts thoroughly, but ONLY concepts relevant to the question.
9. Prioritize understanding and completeness.
10. Ensure the answer is long, comprehensive, and deeply informative.""",
        "Bullet Points": """Format the answer strictly as a list of bullet points. Keep each point brief, concise, and focused on key facts without long, detailed explanations.
If there are multiple questions, format your output professionally using Markdown:

**Q: [Question Text]**

- [Brief bullet point]
- [Brief bullet point]

CRITICAL: DO NOT use large headers like # or ##. Only use **bold text** for the questions.
CRITICAL: You MUST place a blank line between the Question and the bullet points. Do not write the answer on the same line as the question.
""",
        "Short Notes": """Provide extremely short, ultra-concise revision notes. You MUST cover all the key topics and critical information, but do so using the absolute minimum number of words possible. Use bullet points and keep sentences extremely brief.
Format your output strictly and professionally using Markdown:

**Q: [Question Text or Topic]**

- [Ultra-short bullet point]
- [Ultra-short bullet point]

CRITICAL: DO NOT use large headers like # or ##. Only use **bold text** for the questions.
CRITICAL: You MUST place a blank line between the Question and the bullet points. Do not write the answer on the same line as the question.
""",
        "Viva": """Generate exactly 10 potential viva (oral exam) questions related to this topic based on the context.
Format your output professionally using Markdown:
**Q1. [Question Text]**
*Answer:* [Highly detailed answer]
""",
        "MCQ": """Generate exactly 10 multiple-choice questions with 4 options each based on the context.
Format your output strictly and professionally using Markdown:

**Q1. [Question Text]**
- A) [Option 1]
- B) [Option 2]
- C) [Option 3]
- D) [Option 4]

✅ **Correct Answer:** [Correct Option]
*Explanation:* [Brief 1-2 sentence explanation of why it is correct]"""
    }
    
    selected_instruction = mode_instructions.get(mode, "Provide a clear, detailed, and comprehensive answer.")
    
    if custom_instruction:
        selected_instruction += f"\n\nCRITICAL USER CUSTOM INSTRUCTION:\n{custom_instruction}\nYou MUST strictly follow this custom instruction while formatting your answer."
    
    template = base_instructions + f"\n\nFormat Instruction: {selected_instruction}\n\nAnswer:"
    return PromptTemplate(template=template, input_variables=["context", "question"])

_faiss_cache = {}

def clear_cache(user_id):
    """Clears the FAISS memory cache for a user, forcing a reload from disk."""
    global _faiss_cache
    if user_id in _faiss_cache:
        del _faiss_cache[user_id]

def answer_question(user_id, question, mode="Simple", custom_instruction="", extra_context=""):
    """
    Main function to answer a question using RAG.
    """
    # Use cached vector store if available, otherwise load and cache it
    global _faiss_cache
    if user_id in _faiss_cache:
        vector_store = _faiss_cache[user_id]
    else:
        vector_store = load_vector_store(user_id)
        if vector_store:
            _faiss_cache[user_id] = vector_store
            
    if not vector_store and not extra_context:
        return "No study materials found. Please upload notes first or attach a file to your question."
        
    # Retrieve relevant chunks (top 4)
    context = ""
    if vector_store:
        docs = vector_store.similarity_search(question, k=4)
        context = "\n\n".join([doc.page_content for doc in docs])
        
    if extra_context:
        context = f"--- Attached File Content ---\n{extra_context}\n\n--- Knowledge Base ---\n{context}"
    
    if not context.strip():
        return "No relevant information found in your notes or attached file for this question."
        
    prompt = build_prompt(mode, custom_instruction)
    formatted_prompt = prompt.format(context=context, question=question)
    
    # Priority list of free models to try. If one hits a rate limit or is decommissioned, the system automatically falls back to the next!
    FALLBACK_MODELS = [
        "llama-3.3-70b-versatile", # Primary: Most powerful
        "llama3-70b-8192",         # Fallback 1: High capability
        "gemma2-9b-it",            # Fallback 2: Google's intelligent Gemma
        "llama-3.1-8b-instant"     # Fallback 3: Super fast, very high rate limit
    ]
    
    last_error = ""
    for model_name in FALLBACK_MODELS:
        try:
            print(f"Attempting to generate answer using {model_name}...")
            # Reduced max_tokens to 4000 to stay safely under Groq's 6000 TPM limit
            llm = ChatGroq(model_name=model_name, temperature=0.3, max_tokens=4000)
            response = llm.invoke(formatted_prompt)
            
            content = response.content
            if isinstance(content, list):
                # Extract text from list of blocks if applicable
                content = " ".join([str(c.get("text", "")) if isinstance(c, dict) else str(c) for c in content])
            return str(content)
            
        except Exception as e:
            error_str = str(e)
            # If the error is a Rate Limit (429) OR Model Decommissioned (400), catch it and loop to the next model
            if "429" in error_str or "rate limit" in error_str.lower() or "400" in error_str or "decommissioned" in error_str.lower():
                print(f"{model_name} unavailable (Rate Limit / Decommissioned). Automatically falling back to the next model...")
                last_error = error_str
                continue
            else:
                # If it's a completely different error (e.g. no internet), stop and show it
                return f"Error generating answer: {error_str}"
                
    # If the loop finishes and ALL models are unavailable
    return f"All AI models are currently overwhelmed with traffic. Please try again in an hour or two. (Last Error: {last_error})"
