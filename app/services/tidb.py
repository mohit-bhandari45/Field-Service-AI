from dotenv import load_dotenv
import asyncio
import os
import pickle
import pymysql

# Loading environment variables from .env
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "ssl": {"ca": os.getenv("DB_CA_PATH")}
}

def db_connection():
    try:
        # Try to connect to TiDB
        conn = pymysql.connect(**DB_CONFIG)
        print("✅ Database connected successfully!")
        conn.close()
    except pymysql.MySQLError as e:
        print("❌ Database connection failed:", e)

# Call the test function
db_connection()

async def store_vector(vector, metadata):
    """
    Store vector and metadata in TiDB
    """

    # Serialize vector using pickle
    vector_blob = pickle.dumps(vector)

    # Convert metadata dict to JSON string
    import json

    metadata_json = json.dumps(metadata)

    # TiDB is sync, wrapping in executor for async
    import concurrent.futures
    loop = asyncio.get_event_loop()

    def db_insert():
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = """
        INSERT INTO equipment_embeddings (filename, vector, metadata)
        VALUES (%s, %s, %s)    
        """
        cursor.execute(sql, (metadata["filename"], vector_blob, metadata_json))
        conn.commit()
        cursor.close()
        conn.close()

    await loop.run_in_executor(None, db_insert)
    return True
