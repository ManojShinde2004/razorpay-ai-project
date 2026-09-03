import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import joblib
import os


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "payment_training_data.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "recovery_model.pkl"
)


# ============================================================
# LOAD DATASET
# ============================================================

print("Loading dataset...")

data = pd.read_csv(CSV_PATH)

print("Dataset loaded successfully!")
print("Training rows:", len(data))
print("Columns:", list(data.columns))


# ============================================================
# REQUIRED COLUMNS CHECK
# ============================================================

features = [
    "amount",
    "previous_failures",
    "customer_history",
    "failure_reason",
    "payment_method",
    "retry_count",
    "customer_age_days",
    "time_of_day",
    "day_type"
]

target = "recovered"


required_columns = features + [target]

missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in CSV: {missing_columns}"
    )


# ============================================================
# REMOVE MISSING VALUES
# ============================================================

data = data.dropna(
    subset=required_columns
)

print(
    "Rows after removing missing values:",
    len(data)
)


# ============================================================
# FEATURES AND TARGET
# ============================================================

X = data[features]

y = data[target]


# ============================================================
# CATEGORICAL FEATURES
# ============================================================

categorical_features = [
    "failure_reason",
    "payment_method",
    "day_type"
]


# ============================================================
# NUMERICAL FEATURES
# ============================================================

numerical_features = [
    "amount",
    "previous_failures",
    "customer_history",
    "retry_count",
    "customer_age_days",
    "time_of_day"
]


# ============================================================
# PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),

        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# ============================================================
# RANDOM FOREST CLASSIFIER
# ============================================================

classifier = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    random_state=42,
    class_weight="balanced"
)


# ============================================================
# COMPLETE MACHINE LEARNING PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),

        (
            "classifier",
            classifier
        )
    ]
)


# ============================================================
# TRAIN MODEL
# ============================================================

print("Training AI model...")

pipeline.fit(
    X,
    y
)

print("AI model trained successfully!")

print(
    "Training rows:",
    len(X)
)


# ============================================================
# CREATE MODEL DIRECTORY
# ============================================================

os.makedirs(
    os.path.dirname(MODEL_PATH),
    exist_ok=True
)


# ============================================================
# SAVE TRAINED MODEL
# ============================================================

joblib.dump(
    pipeline,
    MODEL_PATH
)

print("Model saved successfully!")

print(
    "Model path:",
    MODEL_PATH
)


# ============================================================
# TRAINING SUMMARY
# ============================================================

print("\n==============================")
print("MODEL TRAINING SUMMARY")
print("==============================")
print(
    "Dataset rows:",
    len(data)
)
print(
    "Features:",
    len(features)
)
print(
    "Target:",
    target
)
print(
    "Model: Random Forest Classifier"
)
print(
    "Trees:",
    100
)
print(
    "Max depth:",
    8
)
print(
    "Categorical encoding: One-Hot Encoding"
)
print("==============================")
print("Training completed!")