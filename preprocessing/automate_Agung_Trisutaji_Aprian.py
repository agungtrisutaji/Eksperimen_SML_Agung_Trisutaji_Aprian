from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT / "telco_customer_churn_raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
OUTPUT_DIR = ROOT / "preprocessing" / "telco_customer_churn_preprocessing"

TARGET_COLUMN = "Churn"
DROP_COLUMNS = ["customerID"]
RANDOM_STATE = 42
TEST_SIZE = 0.2


def validate_dataset(data: pd.DataFrame) -> None:
    required_columns = {TARGET_COLUMN, "TotalCharges"}
    missing_columns = sorted(required_columns.difference(data.columns))
    if missing_columns:
        raise ValueError(f"Dataset missing required columns: {missing_columns}")

    target_values = set(data[TARGET_COLUMN].dropna().unique())
    unsupported_values = sorted(target_values.difference({"No", "Yes"}))
    if unsupported_values:
        raise ValueError(
            f"Unsupported target values in {TARGET_COLUMN}: {unsupported_values}"
        )


def run_preprocessing() -> dict[str, object]:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            "Raw Telco Customer Churn dataset not found at "
            f"{RAW_DATA_PATH}. Put the Kaggle CSV in telco_customer_churn_raw/."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(RAW_DATA_PATH)
    validate_dataset(data)

    data = data.copy()
    data["TotalCharges"] = pd.to_numeric(data["TotalCharges"], errors="coerce")

    y = data[TARGET_COLUMN].map({"No": 0, "Yes": 1}).astype(int)
    X = data.drop(columns=[TARGET_COLUMN, *DROP_COLUMNS], errors="ignore")

    numeric_columns = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = X.select_dtypes(exclude=["number"]).columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_columns),
            ("cat", categorical_pipeline, categorical_columns),
        ]
    )

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    feature_names = preprocessor.get_feature_names_out().tolist()

    pd.DataFrame(X_train_processed, columns=feature_names).to_csv(
        OUTPUT_DIR / "X_train.csv", index=False
    )
    pd.DataFrame(X_test_processed, columns=feature_names).to_csv(
        OUTPUT_DIR / "X_test.csv", index=False
    )
    y_train.rename(TARGET_COLUMN).to_csv(OUTPUT_DIR / "y_train.csv", index=False)
    y_test.rename(TARGET_COLUMN).to_csv(OUTPUT_DIR / "y_test.csv", index=False)
    (OUTPUT_DIR / "feature_names.json").write_text(
        json.dumps(feature_names, indent=2), encoding="utf-8"
    )
    joblib.dump(preprocessor, OUTPUT_DIR / "preprocessor.pkl")

    summary = {
        "dataset": "Telco Customer Churn",
        "source": "Kaggle blastchar/telco-customer-churn",
        "raw_data_path": str(RAW_DATA_PATH.relative_to(ROOT)),
        "target_column": TARGET_COLUMN,
        "target_mapping": {"No": 0, "Yes": 1},
        "dropped_columns": DROP_COLUMNS,
        "rows": int(data.shape[0]),
        "columns": int(data.shape[1]),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "train_rows": int(X_train.shape[0]),
        "test_rows": int(X_test.shape[0]),
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "totalcharges_missing_after_numeric_conversion": int(
            data["TotalCharges"].isna().sum()
        ),
        "preprocessing": {
            "numeric": ["SimpleImputer(strategy='median')", "StandardScaler"],
            "categorical": [
                "SimpleImputer(strategy='most_frequent')",
                "OneHotEncoder(handle_unknown='ignore')",
            ],
            "fit_scope": "fit only on X_train, transform X_train and X_test",
        },
        "outputs": [
            "X_train.csv",
            "X_test.csv",
            "y_train.csv",
            "y_test.csv",
            "feature_names.json",
            "preprocessing_summary.json",
            "preprocessor.pkl",
        ],
    }
    (OUTPUT_DIR / "preprocessing_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print("Automated preprocessing completed.")
    print(f"Output directory: {OUTPUT_DIR}")
    return summary


if __name__ == "__main__":
    run_preprocessing()

