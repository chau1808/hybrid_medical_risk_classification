import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_PATH = "data/raw/heart.csv"
OUTPUT_PATH = "data/processed/heart_cleaned.csv"

df = pd.read_csv(INPUT_PATH)

print("===== BƯỚC 3: XỬ LÝ GIÁ TRỊ 0 =====")

print("Trước khi xử lý:")
print("RestingBP = 0:", (df["RestingBP"] == 0).sum())
print("Cholesterol = 0:", (df["Cholesterol"] == 0).sum())

df["RestingBP"] = df["RestingBP"].replace(0, pd.NA)
df["Cholesterol"] = df["Cholesterol"].replace(0, pd.NA)

print("\nSau khi chuyển thành giá trị thiếu:")
print(df[["RestingBP", "Cholesterol"]].isna().sum())

df.to_csv(OUTPUT_PATH, index=False)

print("\nĐã lưu:", OUTPUT_PATH)
print("Kích thước:", df.shape)


print("\n===== BƯỚC 4: CHIA TRAIN / TEST =====")

X = df.drop(columns=["HeartDisease"])
y = df["HeartDisease"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

train_df = X_train.copy()
train_df["HeartDisease"] = y_train

test_df = X_test.copy()
test_df["HeartDisease"] = y_test

train_df.to_csv(
    "data/processed/train.csv",
    index=False
)

test_df.to_csv(
    "data/processed/test.csv",
    index=False
)

print("\nTrain:", train_df.shape)
print("Test:", test_df.shape)

print("\nNhãn Train:")
print(train_df["HeartDisease"].value_counts())

print("\nNhãn Test:")
print(test_df["HeartDisease"].value_counts())

print("\nĐã tạo:")
print("data/processed/train.csv")
print("data/processed/test.csv")