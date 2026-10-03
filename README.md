# Hybrid Medical Risk Classification

**Đề tài:** Phân loại Lai ghép (Hybrid Classification) giữa dữ liệu có cấu trúc và vector ngữ nghĩa trong cảnh báo rủi ro y khoa cá nhân hóa.

## 1. Giới thiệu

Project nghiên cứu phương pháp kết hợp:

* Dữ liệu y khoa có cấu trúc.
* Patient Notes dạng văn bản.
* Embedding Vector từ Gemini Embedding API.
* Machine Learning để phân loại rủi ro.
* Gemini để hỗ trợ tạo báo cáo cá nhân hóa.

Pipeline chính:

```text
Structured Data
      │
      ├──► Preprocessing
      │
      └──► Patient Notes
                │
                ▼
        Gemini Embedding API
                │
                ▼
          768D Embedding
                │
                ▼
       PostgreSQL + pgvector
                │
                ▼
        Feature Fusion
                │
                ▼
     Hybrid Classification
```

## 2. Công nghệ

* Python
* Pandas / NumPy
* Scikit-learn
* Google Gemini API
* PostgreSQL
* pgvector
* Docker
* Git / GitHub

## 3. Cấu trúc project

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
│   ├── notes/
│   ├── embedding/
│   ├── models/
│   └── agent/
│
├── docker/
│   └── docker-compose.yml
│
├── docs/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 4. Cài đặt

### Clone project

```bash
git clone <repository-url>
cd hybrid_medical_risk_classification
```

### Tạo môi trường Python

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Cài thư viện

```powershell
pip install -r requirements.txt
```

## 5. Cấu hình `.env`

Tạo file `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_risk
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
```

> Không commit file `.env` lên GitHub.

## 6. Chạy PostgreSQL + pgvector

Khởi động Docker:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml up -d
```

Kiểm tra container:

```powershell
docker ps
```

Dừng Docker:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml down
```

## 7. Chạy các bước xử lý

### Preprocessing

Các script xử lý dữ liệu nằm trong:

```text
src/preprocessing/
```

### Generate Patient Notes

```text
src/notes/
```

### Generate Embedding

```text
src/embedding/
```

Embedding sử dụng:

```text
gemini-embedding-001
```

với vector **768 chiều**.

## 8. Kiểm tra PostgreSQL

Kiểm tra số lượng dữ liệu:

```powershell
docker exec medical_postgres psql -U postgres -d medical_risk -c "SELECT COUNT(*) FROM patient_notes;"
```

Kiểm tra embedding:

```powershell
docker exec medical_postgres psql -U postgres -d medical_risk -c "SELECT patient_id, vector_dims(embedding) FROM patient_notes ORDER BY patient_id;"
```

## 9. Trạng thái project

### Đã hoàn thành

* [x] Dataset và preprocessing
* [x] Generate Patient Notes mẫu
* [x] Docker PostgreSQL
* [x] pgvector
* [x] Gemini Embedding API
* [x] Embedding 768 chiều
* [x] Lưu embedding vào PostgreSQL

### Đang phát triển

* [ ] Embedding toàn bộ dataset
* [ ] Feature Fusion
* [ ] Hybrid Classification
* [ ] Huấn luyện mô hình
* [ ] Đánh giá mô hình
* [ ] Feature Importance
* [ ] Personalized Medical Report

## 10. Lưu ý

Dataset và Patient Notes trong project phục vụ mục đích nghiên cứu và thử nghiệm.