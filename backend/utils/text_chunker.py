from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Splits text into smaller chunks for RAG processing.
    
    Args:
        text (str): The large text to be chunked.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The overlap between consecutive chunks to maintain context.
        
    Returns:
        list: A list of text chunks (strings).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    return chunks
