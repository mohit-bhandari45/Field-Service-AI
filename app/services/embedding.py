import openai
import asyncio

openai.api_key = "YOUR_OPENAI_API_KEY"


async def generate_embedding(image):
    """
    Generate embedding from image using OpenAI CLIP model
    """

    import base64
    import io

    # Convert PIL image to bytes
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    # OpenAI API call is sync, wrap in executor
    import concurrent.futures

    loop = asyncio.get_event_loop()

    def get_embedding():
        response = openai.Embedding.create(
            input=img_bytes, model="clip-vit-base-patch32"
        )
        return response["data"][0]["embedding"]

    embedding = await loop.run_in_executor(None, get_embedding)
    return embedding
