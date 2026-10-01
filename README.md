# Hybrid Medical Risk Classification

Đề tài: **Phân loại Lai ghép (Hybrid Classification) giữa dữ liệu có cấu trúc và vector ngữ nghĩa trong cảnh báo rủi ro y khoa cá nhân hóa.**

## 1. Tổng quan

Project nghiên cứu mô hình phân loại lai ghép giữa:

* **Dữ liệu y khoa có cấu trúc:** tuổi, giới tính, BMI, huyết áp, chỉ số xét nghiệm, dấu hiệu sinh tồn,...
* **Dữ liệu văn bản:** clinical notes, triệu chứng và mô tả tình trạng bệnh nhân.
* **Embedding Vector:** chuyển dữ liệu văn bản thành vector ngữ nghĩa bằng Embedding API.
* **Machine Learning:** kết hợp dữ liệu có cấu trúc và vector để thực hiện phân loại rủi ro.
* **Gemini:** hỗ trợ sinh báo cáo y khoa cá nhân hóa dựa trên kết quả dự đoán và Feature Importance.

Mục tiêu là xây dựng pipeline có thể chạy trên tài nguyên tương đối nhẹ, chủ yếu sử dụng CPU/RAM, không tự huấn luyện mô hình Embedding hoặc mạng nơ-ron sâu.

---

## 2. Cấu trúc project

```text
hybrid_medical_risk_classification/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── src/
│   ├── preprocessing/
│   ├── embedding/
│   │   ├── __init__.py
│   │   ├── embedding_api.py
│   │   └── save_embedding.py
│   ├── models/
│   └── agent/
│
├── docs/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

> Dữ liệu y khoa thực tế không được đưa trực tiếp lên GitHub.

---

## 3. Yêu cầu môi trường

* Windows 10/11
* Python 3.x
* PostgreSQL 18.x
* PostgreSQL extension `pgvector`
* Git
* VS Code

---

## 4. Tạo môi trường Python

Mở Terminal tại thư mục project:

```powershell
python -m venv .venv
```

Kích hoạt môi trường:

```powershell
.venv\Scripts\activate
```

Nếu thành công, Terminal sẽ có:

```text
(.venv)
```

---

## 5. Cài thư viện

Cài dependencies:

```powershell
pip install -r requirements.txt
```

Hoặc cài thủ công:

```powershell
pip install google-genai python-dotenv psycopg2-binary
```

Sau khi cài:

```powershell
pip freeze > requirements.txt
```

---

## 6. Cấu hình biến môi trường

Không đưa API key và password lên GitHub.

Tạo file:

```text
.env
```

Nội dung:

```env
GEMINI_API_KEY=your_gemini_api_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_risk
DB_USER=postgres
DB_PASSWORD="your_postgresql_password"
```

File `.env` đã được thêm vào `.gitignore`.

### Tạo từ file mẫu

Copy:

```text
.env.example
```

thành:

```text
.env
```

Sau đó điền API key và password PostgreSQL của máy cá nhân.

---

## 7. PostgreSQL + pgvector

Tạo database:

```text
medical_risk
```

Trong pgAdmin → chọn database `medical_risk` → Query Tool.

Kiểm tra pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Tạo bảng lưu clinical notes và embedding:

```sql
CREATE TABLE IF NOT EXISTS patient_notes (
    patient_id INT PRIMARY KEY,
    note TEXT,
    embedding VECTOR(768)
);
```

Kiểm tra:

```sql
SELECT * FROM patient_notes;
```

---

## 8. Kiểm tra Embedding API

File:

```text
src/embedding/embedding_api.py
```

Chạy:

```powershell
python src/embedding/embedding_api.py
```

Kết quả mong muốn:

```text
Số chiều: 768
5 giá trị đầu: [...]
```

Embedding model đang sử dụng:

```text
gemini-embedding-001
```

Vector được cấu hình với:

```text
768 dimensions
```

---

## 9. Lưu Embedding vào PostgreSQL

File:

```text
src/embedding/save_embedding.py
```

Chạy:

```powershell
python src/embedding/save_embedding.py
```

Kết quả mong muốn:

```text
Số chiều: 768
Đã lưu Embedding thật vào PostgreSQL!
```

Kiểm tra trong pgAdmin:

```sql
SELECT
    patient_id,
    note,
    vector_dims(embedding) AS dimensions
FROM patient_notes;
```

Kết quả mong muốn:

```text
patient_id | note | dimensions
-----------+------+-----------
1          | ...  | 768
```

---

## 10. Quy trình tổng thể

```text
Clinical Notes
      │
      ▼
Embedding API
      │
      ▼
768-dimensional Vector
      │
      ▼
PostgreSQL + pgvector
      │
      │
      ├──────────────┐
      │              │
      ▼              ▼
Structured Data   Text Vector
      │              │
      └──────┬───────┘
             ▼
      Feature Fusion
             │
             ▼
     Hybrid Classification
             │
             ▼
       Risk Prediction
             │
             ▼
   Personalized Medical Report
```

---

## 11. Bảo mật

Các file/thông tin sau **không được commit lên GitHub**:

```text
.env
.venv/
data/raw/
data/processed/
```

API key và mật khẩu PostgreSQL phải được lưu trong `.env`.

File `.env.example` chỉ chứa tên biến và giá trị mẫu:

```env
GEMINI_API_KEY=your_gemini_api_key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_risk
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
```

---

## 12. Git workflow

Kiểm tra thay đổi:

```powershell
git status
```

Thêm file:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Update project"
```

Push:

```powershell
git push
```

Không commit file `.env`.

---

## 13. Trạng thái hiện tại

### Đã thực hiện

* [x] Tạo repository
* [x] Tạo Python virtual environment
* [x] Cài đặt Google GenAI SDK
* [x] Cấu hình Gemini API
* [x] Cài đặt PostgreSQL
* [x] Cài đặt pgvector
* [x] Tạo database `medical_risk`
* [x] Tạo bảng `patient_notes`
* [x] Kết nối Python với PostgreSQL
* [x] Gọi Embedding API
* [x] Lưu vector vào PostgreSQL

### Đang phát triển

* [ ] Khảo sát và xử lý dataset y khoa
* [ ] Tiền xử lý dữ liệu có cấu trúc
* [ ] Sinh embedding cho clinical notes
* [ ] Kết hợp structured features + embedding vectors
* [ ] PCA / giảm chiều
* [ ] Huấn luyện mô hình XGBoost / LightGBM
* [ ] Đánh giá mô hình
* [ ] Feature Importance
* [ ] Sinh báo cáo y khoa cá nhân hóa bằng Gemini
