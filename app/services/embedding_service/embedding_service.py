import asyncio
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from sentence_transformers import SentenceTransformer

# -----------------------------
# Load CLIP once for images
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# -----------------------------
# Load SentenceTransformer for text embeddings (free, local)
# -----------------------------
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim embeddings

# -----------------------------
# Generate image embedding (512-dim, CLIP)
# -----------------------------
async def generate_image_embedding(image: Image.Image):
    loop = asyncio.get_event_loop()

    def _embed():
        inputs = clip_processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = clip_model.get_image_features(**inputs)
        # Normalize to unit vector
        embedding = outputs / outputs.norm(p=2, dim=-1, keepdim=True)
        return embedding.squeeze(0).cpu().numpy().tolist()

    return await loop.run_in_executor(None, _embed)

# -----------------------------
# Generate text embedding (384-dim, local SentenceTransformer)
# -----------------------------
async def generate_text_embedding(text: str):
    if not text.strip():
        return None  # skip empty text

    loop = asyncio.get_event_loop()
    embedding = await loop.run_in_executor(None, lambda: sbert_model.encode(text))
    return embedding.tolist()