from sqlalchemy import text
from sqlalchemy.orm import Session
from app.config.db import SessionLocal
from app.models import EquipmentImage

async def search_similar_images(query_vector, top_k=5):
    db: Session = SessionLocal()
    try:
        # TiDB expects string format for vector
        vec_str = "[" + ",".join(str(float(x)) for x in query_vector) + "]"

        sql = text(f"""
            SELECT id, filename, metadata, vector,
                   VEC_COSINE_DISTANCE(vector, CAST(:vec AS VECTOR(512))) AS score
            FROM equipment_embeddings
            ORDER BY score ASC
            LIMIT :k
        """)

        rows = db.execute(sql, {"vec": vec_str, "k": top_k}).fetchall()

        # Return list of (EquipmentImage, score)
        results = []
        for row in rows:
            img = db.query(EquipmentImage).get(row.id)
            results.append((img, row.score))

        return results
    finally:
        db.close()