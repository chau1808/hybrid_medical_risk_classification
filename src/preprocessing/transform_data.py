import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline


TRAIN_PATH = "data/processed/train.csv"
TEST_PATH = "data/processed/test.csv"

TRAIN_OUTPUT = "data/processed/train_transformed.csv"
TEST_OUTPUT = "data/processed/test_transformed.csv"


train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

X_train = train_df.drop(columns=["HeartDisease"])
y_train = train_df["HeartDisease"]

X_test = test_df.drop(columns=["HeartDisease"])
y_test = test_df["HeartDisease"]


numeric_features = [
    "Age",
    "RestingBP",
    "Cholesterol",
    "FastingBS",
    "MaxHR",
    "Oldpeak"
]

categorical_features = [
    "Sex",
    "ChestPainType",
    "RestingECG",
    "ExerciseAngina",
    "ST_Slope"
]


numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])


preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])


X_train_transformed = preprocessor.fit_transform(X_train)

X_test_transformed = preprocessor.transform(X_test)


feature_names = preprocessor.get_feature_names_out()

train_transformed = pd.DataFrame(
    X_train_transformed,
    columns=feature_names
)

test_transformed = pd.DataFrame(
    X_test_transformed,
    columns=feature_names
)


train_transformed["HeartDisease"] = y_train.values
test_transformed["HeartDisease"] = y_test.values


train_transformed.to_csv(TRAIN_OUTPUT, index=False)
test_transformed.to_csv(TEST_OUTPUT, index=False)


print("===== BƯỚC 5: TRANSFORM DỮ LIỆU =====")

print("Train ban đầu:", X_train.shape)
print("Test ban đầu:", X_test.shape)

print("Train sau xử lý:", X_train_transformed.shape)
print("Test sau xử lý:", X_test_transformed.shape)

print("\nSố lượng features:", len(feature_names))

print("\nĐã tạo:")
print(TRAIN_OUTPUT)
print(TEST_OUTPUT)