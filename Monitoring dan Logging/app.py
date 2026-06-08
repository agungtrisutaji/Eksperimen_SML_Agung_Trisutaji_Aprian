from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from pydantic import BaseModel, ConfigDict


ROOT = Path(__file__).resolve().parents[1]
PREPROCESSOR_PATH = (
    ROOT
    / "Membangun_model"
    / "telco_customer_churn_preprocessing"
    / "artifacts"
    / "preprocessor.pkl"
)
MODEL_DIR = ROOT / "Membangun_model" / "artifacts"
TUNED_MODEL_PATH = MODEL_DIR / "tuned_model.pkl"
BASELINE_MODEL_PATH = MODEL_DIR / "best_model.pkl"

RAW_FEATURE_COLUMNS = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
]

model_requests_total = Counter("model_requests_total", "Total prediction requests.")
model_predictions_total = Counter("model_predictions_total", "Total successful predictions.")
model_prediction_errors_total = Counter("model_prediction_errors_total", "Total prediction errors.")
model_prediction_latency_seconds = Histogram(
    "model_prediction_latency_seconds", "Prediction latency in seconds."
)
model_positive_predictions_total = Counter(
    "model_positive_predictions_total", "Total churn predictions."
)
model_negative_predictions_total = Counter(
    "model_negative_predictions_total", "Total non-churn predictions."
)
model_input_missing_values_total = Counter(
    "model_input_missing_values_total", "Total missing input values observed."
)
model_input_payload_size_bytes = Histogram(
    "model_input_payload_size_bytes", "Input payload size in bytes."
)
model_health_status = Gauge("model_health_status", "Model service health, 1 healthy or 0 down.")
model_probability_score = Gauge(
    "model_probability_score", "Last churn probability score returned by the model."
)
model_last_prediction_timestamp = Gauge(
    "model_last_prediction_timestamp", "Unix timestamp of the last successful prediction."
)
model_loaded_status = Gauge("model_loaded_status", "Model loaded status, 1 loaded or 0 missing.")


class TelcoCustomerPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    gender: str | None = None
    SeniorCitizen: int | None = None
    Partner: str | None = None
    Dependents: str | None = None
    tenure: int | float | None = None
    PhoneService: str | None = None
    MultipleLines: str | None = None
    InternetService: str | None = None
    OnlineSecurity: str | None = None
    OnlineBackup: str | None = None
    DeviceProtection: str | None = None
    TechSupport: str | None = None
    StreamingTV: str | None = None
    StreamingMovies: str | None = None
    Contract: str | None = None
    PaperlessBilling: str | None = None
    PaymentMethod: str | None = None
    MonthlyCharges: int | float | None = None
    TotalCharges: int | float | str | None = None


def _load_model_artifacts() -> tuple[Any | None, Any | None, Path | None]:
    model_path = TUNED_MODEL_PATH if TUNED_MODEL_PATH.exists() else BASELINE_MODEL_PATH
    if not PREPROCESSOR_PATH.exists() or not model_path.exists():
        model_loaded_status.set(0)
        model_health_status.set(0)
        return None, None, None

    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(model_path)
    model_loaded_status.set(1)
    model_health_status.set(1)
    return preprocessor, model, model_path


preprocessor, model, active_model_path = _load_model_artifacts()

app = FastAPI(
    title="Telco Customer Churn MLOps API",
    version="1.0.0",
    description="FastAPI serving app for Dicoding Membangun Sistem Machine Learning submission.",
)


@app.get("/health")
def health() -> dict[str, Any]:
    loaded = preprocessor is not None and model is not None
    model_loaded_status.set(1 if loaded else 0)
    model_health_status.set(1 if loaded else 0)
    return {
        "status": "ok" if loaded else "model_not_loaded",
        "model_loaded": loaded,
        "model_path": str(active_model_path.relative_to(ROOT)) if active_model_path else None,
        "preprocessor_path": (
            str(PREPROCESSOR_PATH.relative_to(ROOT)) if PREPROCESSOR_PATH.exists() else None
        ),
    }


@app.post("/predict")
def predict(payload: TelcoCustomerPayload) -> dict[str, Any]:
    if preprocessor is None or model is None:
        model_prediction_errors_total.inc()
        raise HTTPException(
            status_code=503,
            detail=(
                "Model artifacts are not available. Run preprocessing and modelling first."
            ),
        )

    started = time.perf_counter()
    model_requests_total.inc()

    payload_dict = payload.model_dump()
    model_input_payload_size_bytes.observe(len(json.dumps(payload_dict).encode("utf-8")))

    missing_values = sum(
        1 for column in RAW_FEATURE_COLUMNS if payload_dict.get(column) in (None, "")
    )
    if missing_values:
        model_input_missing_values_total.inc(missing_values)

    try:
        input_row = {column: payload_dict.get(column) for column in RAW_FEATURE_COLUMNS}
        input_frame = pd.DataFrame([input_row])
        input_frame["TotalCharges"] = pd.to_numeric(
            input_frame["TotalCharges"], errors="coerce"
        )
        transformed = pd.DataFrame(
            preprocessor.transform(input_frame),
            columns=preprocessor.get_feature_names_out(),
        )
        prediction = int(model.predict(transformed)[0])
        probability = float(model.predict_proba(transformed)[0][1])
    except Exception as exc:
        model_prediction_errors_total.inc()
        model_health_status.set(0)
        raise HTTPException(status_code=400, detail=f"Prediction failed: {exc}") from exc

    model_prediction_latency_seconds.observe(time.perf_counter() - started)
    model_predictions_total.inc()
    model_probability_score.set(probability)
    model_last_prediction_timestamp.set(time.time())
    model_health_status.set(1)

    if prediction == 1:
        model_positive_predictions_total.inc()
        prediction_label = "Yes"
    else:
        model_negative_predictions_total.inc()
        prediction_label = "No"

    return {
        "prediction": prediction,
        "prediction_label": prediction_label,
        "prediction_probability": probability,
    }


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
