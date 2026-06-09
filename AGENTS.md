# AGENTS.md

> Workspace assumption: the agent is running inside the `MSML` folder. Do **not** create another nested `MSML/` directory.


## Project Identity

This repository is for Dicoding final submission: **Membangun Sistem Machine Learning**.

Target submission quality: **5-star / Advanced**.

Student identity:

- Student name: Agung Trisutaji Aprian
- Dicoding username: agungtrisutaji
- GitHub username: agungtrisutaji
- Docker Hub username: agungtrisutaji
- DagsHub username: agungtrisutaji
- Grafana dashboard name: agungtrisutaji

## Main Goal

Build an end-to-end MLOps project using the Telco Customer Churn dataset.

The project must cover:

1. Dataset experiment notebook based on `Template_Eksperimen_MSML.ipynb`.
2. Automated data preprocessing.
3. Model training with MLflow Tracking.
4. Hyperparameter tuning with MLflow Tracking.
5. GitHub Actions workflow for CI.
6. Docker image build and optional Docker Hub push.
7. Local model serving.
8. Prometheus metrics.
9. Grafana dashboard.
10. Grafana alerting.

## Dataset

Dataset: Telco Customer Churn  
Source: Kaggle `blastchar/telco-customer-churn`  
Problem type: binary classification  
Target column: `Churn`

Expected raw dataset path:

```text
Membangun_model/telco_customer_churn_preprocessing/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

Do not rename this file unless all references are updated consistently.

## Required Root Structure

Use the current repository/workspace root as the submission root folder. This folder is named `MSML` on the user's local machine.

Expected structure:

```text
./
├── Eksperimen_SML_Agung_Trisutaji_Aprian.txt
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
├── Workflow-CI.txt
└── README.md
```

## Important Rules

- Do not delete `Template_Eksperimen_MSML.ipynb`.
- Do not hardcode secrets, tokens, passwords, API keys, or credentials.
- Read secrets only from environment variables.
- Do not print secret values in logs.
- Use `pathlib.Path` for cross-platform compatibility.
- Ensure scripts can run from repository root.
- Keep file and folder names aligned with Dicoding submission requirements.
- Do not create ZIP inside ZIP.
- Do not make the repository private.
- Do not store `.env` files in Git.
- Do not commit `.venv/`.
- Do not commit local `mlruns/` unless explicitly required.
- Do not change the target column from `Churn`.
- Monitoring must follow the Dicoding Monitoring dan Optimasi ML context: monitor both model-level signals and system-level signals, then prepare Grafana dashboard and at least two alert rules.

## Local Virtual Environment Requirement

All local project dependencies must be installed inside a repository-local virtual environment named `.venv`.

Do not install dependencies globally.

Required local setup commands for Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
python -m pip install -r "Monitoring dan Logging/requirements.txt"
```

Required local setup commands for WSL/Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
python -m pip install -r "Monitoring dan Logging/requirements.txt"
```

The `.venv/` folder must be added to `.gitignore` and must never be committed.

GitHub Actions should also create and use `.venv` inside the runner, then execute Python commands through the virtual environment. For Linux runners, use:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
```

For MLflow Project execution, prefer running from the activated `.venv` with:

```bash
cd Membangun_model
mlflow run . -e main --env-manager local
mlflow run . -e tuning --env-manager local
```

Keep `conda.yaml` for MLflow Project compatibility, but the primary local workflow must use `.venv`.

## Environment Variables

Use these environment variables if available:

```text
DAGSHUB_USERNAME
DAGSHUB_TOKEN
MLFLOW_TRACKING_URI
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

Expected MLflow Tracking URI placeholder:

```text
https://dagshub.com/agungtrisutaji/Eksperimen_SML_Agung_Trisutaji_Aprian.mlflow
```

## Commands That Must Work

From repository root, after activating `.venv`, these commands should work:

```bash
python Membangun_model/telco_customer_churn_preprocessing/preprocess.py
python Membangun_model/modelling.py
python Membangun_model/modelling_tuning.py
python "Monitoring dan Logging/7.Inference.py"
```

MLflow Project commands should also work from:

```bash
cd Membangun_model
mlflow run . -e main --env-manager local
mlflow run . -e tuning --env-manager local
```

## Expected Model Metrics

Classification metrics to log:

- accuracy
- precision
- recall
- f1_score
- roc_auc

Primary model selection metric:

```text
f1_score
```

## Expected Prometheus Metrics

The serving app should expose at least 10 metrics, such as:

- model_requests_total
- model_predictions_total
- model_prediction_errors_total
- model_prediction_latency_seconds
- model_positive_predictions_total
- model_negative_predictions_total
- model_input_missing_values_total
- model_input_payload_size_bytes
- model_health_status
- model_probability_score
- model_last_prediction_timestamp
- model_loaded_status

## Agent Working Style

When modifying the project:

1. Inspect the existing tree first.
2. Preserve existing user files.
3. Make small, coherent changes.
4. Prefer simple, robust implementation over over-engineering.
5. Validate paths after creating files.
6. Add clear README instructions.
7. Ensure scripts fail with helpful error messages.
8. Summarize changed files at the end.
