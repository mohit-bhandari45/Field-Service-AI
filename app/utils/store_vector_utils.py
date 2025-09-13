from app.config.db import SessionLocal
from app.models import EquipmentImage
import asyncio

async def store_vector(vector: list[float], metadata: dict) -> int:
    """
    Store vector and metadata in TiDB using SQLAlchemy.
    Vectors are stored as TiDB VECTOR type.
    """
    loop = asyncio.get_event_loop()

    def _db_task():
        db = SessionLocal()
        try:
            data_embedding = EquipmentImage(
                filename=metadata["filename"],
                vector=vector,  # list[float], matches VECTOR column
                extra_metadata=metadata
            )
            db.add(data_embedding)
            db.commit()
            db.refresh(data_embedding)
            return data_embedding.id
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()

    embedding_id = await loop.run_in_executor(None, _db_task)
    return embedding_id