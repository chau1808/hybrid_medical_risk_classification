import pandas as pd
import numpy as np

TRAIN_PATH = "data/processed/train_transformed.csv"
TEST_PATH = "data/processed/test_transformed.csv"

train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH)

print("===== KIỂM TRA DỮ LIỆU SAU PREPROCESSING =====")

print("\nTrain shape:", train.shape)
print("Test shape:", test.shape)

print("\nNaN Train:", train.isna().sum().sum())
print("NaN Test:", test.isna().sum().sum())

print("\nInf Train:", np.isinf(train.select_dtypes(include=np.number)).sum().sum())
print("Inf Test:", np.isinf(test.select_dtypes(include=np.number)).sum().sum())

print("\nSố features Train:", len(train.columns) - 1)
print("Số features Test:", len(test.columns) - 1)

print("\nNhãn Train:")
print(train["HeartDisease"].value_counts())

print("\nNhãn Test:")
print(test["HeartDisease"].value_counts())

print("\n===== DANH SÁCH FEATURES =====")
for i, col in enumerate(train.columns[:-1], 1):
    print(f"{i}. {col}")