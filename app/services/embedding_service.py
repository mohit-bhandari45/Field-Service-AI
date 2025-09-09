import asyncio
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# Load CLIP model once at startup
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

async def generate_embedding(image: Image.Image):
    """
    Generate embedding from image using Hugging Face CLIP
    """

    loop = asyncio.get_event_loop()

    def _embed():
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model.get_image_features(**inputs)
        # Normalize to unit vector (good for vector search)
        embedding = outputs[0] / outputs[0].norm(p=2)
        return embedding.cpu().numpy().tolist()

    # Run embedding computation in executor (non-blocking)
    embedding = await loop.run_in_executor(None, _embed)
    return embedding