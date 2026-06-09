# Monitoring dan Logging

This folder contains the FastAPI serving app, inference test, Prometheus configuration, Dockerfile, and screenshot placeholder folders.

## Run The Serving API

From the repository root after activating `.venv` and training a model:

```bash
python -m uvicorn "Monitoring dan Logging.app:app" --host 127.0.0.1 --port 8000
```

If the quoted module path causes issues on your shell because the folder name contains spaces, run from inside the folder:

```bash
cd "Monitoring dan Logging"
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Endpoints:

```text
GET  /health
POST /predict
GET  /metrics
```

## Run Inference

From the repository root:

```bash
python "Monitoring dan Logging/7.Inference.py"
```

The script first tries `http://127.0.0.1:8000/predict`. If the server is not running, it uses FastAPI `TestClient` in-process.

## Docker

Build from the repository root:

```bash
docker build -f "Monitoring dan Logging/Dockerfile" -t agungtrisutaji/telco-churn-mlops:latest .
```

Run:

```bash
docker run --rm -p 8000:8000 agungtrisutaji/telco-churn-mlops:latest
```

## Prometheus

Run Prometheus with:

```bash
prometheus --config.file="Monitoring dan Logging/2.prometheus.yml"
```

For Prometheus running in Docker on Windows/WSL, use the `host.docker.internal:8000` target already included in the config.

Useful metric queries:

```promql
model_requests_total
model_predictions_total
model_prediction_errors_total
rate(model_prediction_latency_seconds_sum[1m]) / rate(model_prediction_latency_seconds_count[1m])
model_positive_predictions_total
model_negative_predictions_total
model_input_missing_values_total
model_health_status
model_loaded_status
model_probability_score
model_last_prediction_timestamp
```

## Grafana

Create a dashboard named:

```text
agungtrisutaji
```

Advanced requirement:

- Show at least 10 different Grafana metric panels.
- Configure at least 3 Grafana alert rules.
- Capture real screenshots manually; do not create fake screenshots.

Recommended panels:

- Total requests: `model_requests_total`
- Total predictions: `model_predictions_total`
- Positive predictions: `model_positive_predictions_total`
- Negative predictions: `model_negative_predictions_total`
- Prediction errors: `model_prediction_errors_total`
- Prediction latency: `rate(model_prediction_latency_seconds_sum[1m]) / rate(model_prediction_latency_seconds_count[1m])`
- Missing input values: `model_input_missing_values_total`
- Model health: `model_health_status`
- Model loaded: `model_loaded_status`
- Last probability: `model_probability_score`
- Last prediction timestamp: `model_last_prediction_timestamp`

Recommended alert rules:

- High prediction latency: average latency above 1 second for 5 minutes.
- High prediction error count: increase in `model_prediction_errors_total` above 0 for 5 minutes.
- Model health down: `model_health_status == 0`.
- Model loaded down: `model_loaded_status == 0`.

Use at least 3 of the alert rules above for Advanced evidence.

## Manual Screenshot Checklist

Place screenshots in these folders:

```text
1.bukti_serving/
4.bukti monitoring Prometheus/
5.bukti monitoring Grafana/
6.bukti alerting Grafana/
```

Do not invent screenshots. Capture them manually after services are running.
