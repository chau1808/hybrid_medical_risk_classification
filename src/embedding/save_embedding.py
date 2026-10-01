import os
import psycopg2
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

note = "Bệnh nhân khó thở khi gắng sức, phù chân 2 bên"

res = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[note],
    config=types.EmbedContentConfig(
        task_type="CLASSIFICATION",
        output_dimensionality=768
    )
)

embedding = res.embeddings[0].values

print("Số chiều:", len(embedding))

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS patient_notes (
    patient_id INT PRIMARY KEY,
    note TEXT,
    embedding VECTOR(768)
)
""")

cur.execute(
    """
    INSERT INTO patient_notes (patient_id, note, embedding)
    VALUES (%s, %s, %s)
    ON CONFLICT (patient_id)
    DO UPDATE SET
        note = EXCLUDED.note,
        embedding = EXCLUDED.embedding
    """,
    (1, note, str(embedding))
)

conn.commit()

print("Đã lưu Embedding thật vào PostgreSQL!")

cur.close()
conn.close()