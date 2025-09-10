import asyncio
import torch
from sentence_transformers import SentenceTransformer

# Load a SentenceTransformer model once at startup
# This is small, fast, and free (good for hackathon/RAG use cases)
text_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

async def generate_text_embedding(text: str):
    """
    Generate embedding from text using Hugging Face SentenceTransformers
    """
    loop = asyncio.get_event_loop()

    def _embed():
        # Encode text -> vector
        embedding = text_model.encode(text, convert_to_tensor=True, normalize_embeddings=True)
        return embedding.cpu().numpy().tolist()

    # Run embedding computation in executor (non-blocking)
    embedding = await loop.run_in_executor(None, _embed)
    return embedding