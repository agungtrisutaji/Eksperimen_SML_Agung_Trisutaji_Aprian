from __future__ import annotations

import json
import os
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
API_URL = os.getenv("PREDICTION_API_URL", "http://127.0.0.1:8000")

SAMPLE_PAYLOAD = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 1,
    "PhoneService": "No",
    "MultipleLines": "No phone service",
    "InternetService": "DSL",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 29.85,
    "TotalCharges": 29.85,
}


def request_running_api() -> dict:
    response = requests.post(f"{API_URL}/predict", json=SAMPLE_PAYLOAD, timeout=10)
    response.raise_for_status()
    return response.json()


def request_in_process_api() -> dict:
    import importlib.util

    app_path = ROOT / "Monitoring dan Logging" / "app.py"
    spec = importlib.util.spec_from_file_location("monitoring_app", app_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import FastAPI app from {app_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    from fastapi.testclient import TestClient

    client = TestClient(module.app)
    response = client.post("/predict", json=SAMPLE_PAYLOAD)
    response.raise_for_status()
    return response.json()


def main() -> None:
    try:
        result = request_running_api()
        source = API_URL
    except Exception:
        result = request_in_process_api()
        source = "in-process FastAPI TestClient"

    print("Inference completed.")
    print(f"Source: {source}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

