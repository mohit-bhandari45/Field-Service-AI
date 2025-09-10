import numpy as np
import pickle
from sqlalchemy.orm import Session
from app.models import EquipmentImage
from app.config.db import SessionLocal


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors"""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


async def search_similar_images(query_vector, top_k=5):
    db: Session = SessionLocal()
    try:
        results = []
        images = db.query(EquipmentImage).all()

        for img in images:
            stored_vector = pickle.loads(img.vector)
            score = cosine_similarity(query_vector, stored_vector)
            results.append((img, score))

        results = sorted(results, key=lambda x: x[1], reverse=True)
        return results[:top_k]
    finally:
        db.close()
