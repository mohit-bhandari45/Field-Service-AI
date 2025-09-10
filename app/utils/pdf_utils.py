from PyPDF2 import PdfReader

def extract_chunks_from_pdf(path, chunk_size=800, overlap=100):
    """
    Extracts text from PDF and splits into overlapping chunks.
    
    Args:
        path (str): Path to the PDF file
        chunk_size (int): Number of characters per chunk
        overlap (int): Overlap between chunks
    
    Returns:
        List of (chunk_text, page_number)
    """
    reader = PdfReader(path)
    chunks = []

    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue
        
        # Split text into chunks
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append((chunk, page_no))
            start += chunk_size - overlap

    return chunks