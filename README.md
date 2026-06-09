# Membangun Sistem Machine Learning - Telco Customer Churn

Dicoding final submission for **Membangun Sistem Machine Learning**.

Student identity:

- Student name: Agung Trisutaji Aprian
- Dicoding username: agungtrisutaji
- GitHub username: agungtrisutaji
- Docker Hub username: agungtrisutaji
- DagsHub username: agungtrisutaji
- Grafana dashboard name: agungtrisutaji

Dataset:

- Telco Customer Churn
- Kaggle source: `blastchar/telco-customer-churn`
- Target: `Churn`
- Problem type: binary classification

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       ├── preprocessing.yml
│       └── mlops-ci.yml
├── Eksperimen_SML_Agung_Trisutaji_Aprian.txt
├── Template_Eksperimen_MSML.ipynb
├── telco_customer_churn_raw/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
├── preprocessing/
│   ├── Eksperimen_Agung_Trisutaji_Aprian.ipynb
│   ├── automate_Agung_Trisutaji_Aprian.py
│   └── telco_customer_churn_preprocessing/
├── Membangun_model/
│   ├── MLproject
│   ├── conda.yaml
│   ├── modelling.py
│   ├── modelling_tuning.py
│   ├── requirements.txt
│   ├── DagsHub.txt
│   ├── artifacts/
│   └── telco_customer_churn_preprocessing/
│       ├── WA_Fn-UseC_-Telco-Customer-Churn.csv
│       ├── preprocess.py
│       ├── README.md
│       ├── processed/
│       └── artifacts/
├── Monitoring dan Logging/
│   ├── 1.bukti_serving/
│   ├── 2.prometheus.yml
│   ├── 3.prometheus_exporter.py
│   ├── 4.bukti monitoring Prometheus/
│   ├── 5.bukti monitoring Grafana/
│   ├── 6.bukti alerting Grafana/
│   ├── 7.Inference.py
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── Workflow-CI/
│   ├── .github/workflows/mlops-ci.yml
│   └── MLProject/
├── scripts/
│   └── prepare_submission.py
├── Workflow-CI.txt
└── README.md
```

## Local Setup With `.venv`

Do not install dependencies globally. Use a repository-local virtual environment named `.venv`.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
python -m pip install -r "Monitoring dan Logging/requirements.txt"
```

WSL/Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
python -m pip install -r "Monitoring dan Logging/requirements.txt"
```

`.venv/` is ignored by Git and must not be committed.

## Run The Pipeline

From the repository root after activating `.venv`:

```bash
python preprocessing/automate_Agung_Trisutaji_Aprian.py
python Membangun_model/telco_customer_churn_preprocessing/preprocess.py
python Membangun_model/modelling.py
python Membangun_model/modelling_tuning.py
python "Monitoring dan Logging/7.Inference.py"
```

The preprocessing script creates train/test data and `preprocessor.pkl`. The modelling scripts log metrics to MLflow and save local model artifacts.

## Kriteria 1 Preprocessing

Notebook final:

```text
preprocessing/Eksperimen_Agung_Trisutaji_Aprian.ipynb
```

Automated preprocessing output:

```text
preprocessing/telco_customer_churn_preprocessing/
```

Workflow:

```text
.github/workflows/preprocessing.yml
```

## MLflow Project

Keep `conda.yaml` for MLflow compatibility, but the main local workflow uses `.venv`. Run MLflow Project commands with `--env-manager local`:

```bash
cd Membangun_model
mlflow run . -e main --env-manager local
mlflow run . -e tuning --env-manager local
```

Experiment name:

```text
telco-customer-churn-agungtrisutaji
```

Metrics logged:

- accuracy
- precision
- recall
- f1_score
- roc_auc

Primary selection metric:

```text
f1_score
```

## DagsHub / MLflow Tracking

Use environment variables only:

```text
DAGSHUB_USERNAME
DAGSHUB_TOKEN
MLFLOW_TRACKING_URI
```

Expected tracking URI:

```text
https://dagshub.com/agungtrisutaji/Workflow-CI_Agung_Trisutaji_Aprian.mlflow
```

Never print or commit secret values.

## Serving API

Train the model first, then run:

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

Run inference from the repository root:

```bash
python "Monitoring dan Logging/7.Inference.py"
```

## Docker

Build from the repository root:

```bash
docker build -f "Monitoring dan Logging/Dockerfile" -t agungtrisutaji/telco-churn-mlops:latest .
```

Run:

```bash
docker run --rm -p 8000:8000 agungtrisutaji/telco-churn-mlops:latest
```

Push only after logging in with Docker Hub credentials:

```bash
docker push agungtrisutaji/telco-churn-mlops:latest
```

## Prometheus and Grafana

Start the API first, then run Prometheus:

```bash
prometheus --config.file="Monitoring dan Logging/2.prometheus.yml"
```

Grafana dashboard name:

```text
agungtrisutaji
```

Recommended alert rules:

- High prediction latency.
- High prediction error count.
- Model health status down.
- Model loaded status down.

## GitHub Actions

Workflow files:

```text
.github/workflows/mlops-ci.yml
.github/workflows/preprocessing.yml
```

Required secrets:

```text
DAGSHUB_USERNAME
DAGSHUB_TOKEN
MLFLOW_TRACKING_URI
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

The main runner creates `.venv`, installs dependencies inside it, runs preprocessing, runs MLflow Project from `Workflow-CI/MLProject`, uploads artifacts, tries Advanced Docker build with `mlflow models build-docker`, falls back to the manual Dockerfile if needed, and pushes only when Docker Hub secrets are configured.

## Submission Staging

Create the final staging folder:

```bash
python scripts/prepare_submission.py
```

Create the final ZIP only when ready:

```bash
python scripts/prepare_submission.py --zip
```

## Manual Screenshots Still Required

Capture and place screenshots manually:

- MLflow dashboard.
- MLflow artifact/model.
- GitHub Actions workflow success.
- Docker Hub image.
- FastAPI `/health`.
- Inference result.
- Prometheus target UP.
- Prometheus metrics query.
- Grafana dashboard named `agungtrisutaji`.
- Grafana alert rules.

Use these folders:

```text
Monitoring dan Logging/1.bukti_serving/
Monitoring dan Logging/4.bukti monitoring Prometheus/
Monitoring dan Logging/5.bukti monitoring Grafana/
Monitoring dan Logging/6.bukti alerting Grafana/
```
