import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.DataFrame({
    "amount": [
        500, 1000, 1500, 2000, 2500,
        3000, 3500, 4000, 4500, 5000,
        6000, 7000, 8000, 9000, 10000,
        1200, 2200, 3200, 5500, 7500
    ],

    "previous_failures": [
        0, 0, 1, 1, 2,
        2, 3, 1, 2, 3,
        3, 2, 4, 5, 4,
        0, 1, 2, 3, 4
    ],

    "customer_history": [
        1, 1, 1, 0, 1,
        0, 1, 1, 0, 0,
        1, 0, 1, 0, 0,
        1, 1, 0, 0, 1
    ],

    "failure_reason": [
        0, 1, 0, 2, 0,
        2, 1, 0, 2, 3,
        1, 3, 0, 3, 2,
        1, 0, 2, 3, 0
    ],

    "recovered": [
        1, 1, 1, 0, 1,
        0, 1, 1, 0, 0,
        1, 0, 1, 0, 0,
        1, 1, 0, 0, 1
    ]
})

X = data[
    [
        "amount",
        "previous_failures",
        "customer_history",
        "failure_reason"
    ]
]

y = data["recovered"]

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "ml/recovery_model.pkl")

print("AI model trained successfully!")