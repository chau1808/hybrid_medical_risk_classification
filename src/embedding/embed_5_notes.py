
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from google import genai
from google.genai import types

# =========================
# LOAD ENVIRONMENT
# =========================

load_dotenv()

# =========================
# GEMINI
# =========================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================
# INPUT
# =========================

INPUT_PATH = "data/processed/patient_notes_sample.csv"

# Chỉ chạy 5 mẫu để kiểm tra
df = pd.read_csv(INPUT_PATH).head(5)

print("Số Patient sẽ xử lý:", len(df))

# =========================
# POSTGRESQL DOCKER
# =========================

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

# Kiểm tra database đang kết nối
cur.execute("SELECT version();")
print("PostgreSQL:", cur.fetchone()[0])

# =========================
# CREATE EXTENSION + TABLE
# =========================

cur.execute("""
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS patient_notes (
    patient_id INT PRIMARY KEY,
    note TEXT NOT NULL,
    embedding VECTOR(768),
    generator_model VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

print("Đã kiểm tra bảng patient_notes.")

# =========================
# CREATE EMBEDDINGS
# =========================

for _, row in df.iterrows():

    patient_id = int(row["patient_id"])
    note = row["note"]

    print(f"\nĐang tạo embedding Patient {patient_id}...")

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[note],
        config=types.EmbedContentConfig(
            task_type="CLASSIFICATION",
            output_dimensionality=768
        )
    )

    embedding = response.embeddings[0].values

    print("Số chiều:", len(embedding))

    # Lưu embedding vào PostgreSQL Docker
    cur.execute(
        """
        INSERT INTO patient_notes
            (patient_id, note, embedding, generator_model)
        VALUES
            (%s, %s, %s, %s)
        ON CONFLICT (patient_id)
        DO UPDATE SET
            note = EXCLUDED.note,
            embedding = EXCLUDED.embedding,
            generator_model = EXCLUDED.generator_model
        """,
        (
            patient_id,
            note,
            str(embedding),
            "gemini-embedding-001"
        )
    )

# =========================
# COMMIT
# =========================

conn.commit()

print("\n===== HOÀN TẤT =====")
print(f"Đã lưu {len(df)} embedding vào PostgreSQL.")

# =========================
# VERIFY
# =========================

cur.execute("SELECT COUNT(*) FROM patient_notes;")
count = cur.fetchone()[0]

print("Số bản ghi hiện có trong patient_notes:", count)

# =========================
# CLOSE
# =========================

cur.close()
conn.close()

print("Đã đóng kết nối PostgreSQL.")
