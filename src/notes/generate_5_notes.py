import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

INPUT_PATH = "data/processed/heart_cleaned.csv"
OUTPUT_PATH = "data/processed/patient_notes_sample.csv"

df = pd.read_csv(INPUT_PATH)

df_sample = df.head(5)

notes = []

for index, row in df_sample.iterrows():

    prompt = f"""
Hãy viết một Patient Note ngắn bằng tiếng Việt dựa trên thông tin y khoa được cung cấp.

Yêu cầu:
- Viết như một ghi chú lâm sàng ngắn gọn, tự nhiên.
- Chỉ mô tả dữ liệu được cung cấp.
- Không chẩn đoán bệnh.
- Không đề cập đến biến HeartDisease hoặc kết quả dự đoán.
- Không suy đoán tình trạng bệnh lý.
- Không thêm triệu chứng hoặc thông tin không có trong dữ liệu.
- Viết khoảng 2-4 câu.
- Không giải thích ý nghĩa y khoa của các chỉ số.
- Không tự chuyển FastingBS = 0 thành "đường huyết bằng 0".


Quy ước dữ liệu:
- ChestPainType:
  ATA = đau ngực không điển hình
  NAP = đau ngực không do đau thắt ngực
  ASY = không có triệu chứng đau ngực
  TA = đau thắt ngực điển hình

- FastingBS:
  0 = không vượt ngưỡng đường huyết lúc đói được quy ước trong dataset
  1 = vượt ngưỡng đường huyết lúc đói được quy ước trong dataset

- RestingECG:
  Normal = điện tâm đồ bình thường
  ST = có bất thường ST-T
  LVH = dấu hiệu phì đại thất trái

- ExerciseAngina:
  N = không xuất hiện đau thắt ngực khi vận động
  Y = có xuất hiện đau thắt ngực khi vận động

- ST_Slope:
  Up = độ dốc đoạn ST hướng lên
  Flat = độ dốc đoạn ST dạng phẳng
  Down = độ dốc đoạn ST hướng xuống

Thông tin bệnh nhân:
Tuổi: {row['Age']}
Giới tính: {row['Sex']}
Loại đau ngực: {row['ChestPainType']}
Huyết áp lúc nghỉ: {row['RestingBP']}
Cholesterol: {row['Cholesterol']}
FastingBS: {row['FastingBS']}
Điện tâm đồ: {row['RestingECG']}
Nhịp tim tối đa: {row['MaxHR']}
Đau thắt ngực khi vận động: {row['ExerciseAngina']}
Oldpeak: {row['Oldpeak']}
ST slope: {row['ST_Slope']}
"""

    interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=prompt,
    generation_config={
        "thinking_level": "low"
        }
    )

    note = interaction.output_text.strip()

    notes.append({
        "patient_id": index + 1,
        "note": note
    })

    print(f"\n===== Patient {index + 1} =====")
    print(note)


notes_df = pd.DataFrame(notes)

notes_df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("\nĐã lưu:", OUTPUT_PATH)
print("Số Patient Notes:", len(notes_df))