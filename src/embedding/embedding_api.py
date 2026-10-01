import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

res = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[
        "Bệnh nhân khó thở khi gắng sức, phù chân 2 bên"
    ],
    config=types.EmbedContentConfig(
        task_type="CLASSIFICATION",
        output_dimensionality=768
    ),
)

vec = res.embeddings[0].values

print("Số chiều:", len(vec))
print("5 giá trị đầu:", vec[:5])