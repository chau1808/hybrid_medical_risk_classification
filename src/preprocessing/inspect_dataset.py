
import pandas as pd

# Đọc dataset
df = pd.read_csv("data/raw/heart.csv")

# 1. Kích thước dữ liệu
print("===== KÍCH THƯỚC DATASET =====")
print("Số dòng:", df.shape[0])
print("Số cột:", df.shape[1])

# 2. Danh sách các cột
print("\n===== DANH SÁCH CỘT =====")
print(df.columns.tolist())

# 3. Kiểu dữ liệu
print("\n===== KIỂU DỮ LIỆU =====")
print(df.dtypes)

# 4. Thông tin tổng quan
print("\n===== THÔNG TIN DATASET =====")
df.info()

# 5. Kiểm tra giá trị thiếu
print("\n===== GIÁ TRỊ THIẾU =====")
print(df.isnull().sum())

# 6. Kiểm tra dữ liệu trùng lặp
print("\n===== DỮ LIỆU TRÙNG LẶP =====")
print("Số dòng trùng:", df.duplicated().sum())

# 7. Thống kê dữ liệu số
print("\n===== THỐNG KÊ DỮ LIỆU =====")
print(df.describe())

# 8. Phân phối nhãn
print("\n===== PHÂN PHỐI NHÃN =====")
print(df["HeartDisease"].value_counts())
print(df["HeartDisease"].value_counts(normalize=True) * 100)

# 9. Kiểm tra các giá trị 0 cần chú ý
print("\n===== KIỂM TRA GIÁ TRỊ 0 =====")
print("Cholesterol = 0:", (df["Cholesterol"] == 0).sum())
print("RestingBP = 0:", (df["RestingBP"] == 0).sum())