# MSML_PROJECT_CONTEXT.md

> Workspace assumption: the current working directory is already the `MSML` submission workspace. All paths in this file are relative to this current directory. Do **not** generate `MSML/MSML/`.


## 1. Project Overview

This project is a Dicoding final submission for the class **Membangun Sistem Machine Learning**.

The target is to achieve **5-star / Advanced** by implementing an end-to-end MLOps workflow, not only a machine learning notebook.

The final project must demonstrate:

- dataset understanding;
- exploratory data analysis;
- reproducible preprocessing;
- automated preprocessing script;
- model training;
- hyperparameter tuning;
- MLflow Tracking;
- MLflow Project;
- GitHub Actions workflow;
- model artifact generation;
- Docker-based serving;
- Prometheus monitoring;
- Grafana dashboard;
- Grafana alerting;
- inference testing;
- complete final documentation.

## 2. Identity and Naming Convention

Use the following identity consistently:

```text
Student name        : Agung Trisutaji Aprian
Dicoding username   : agungtrisutaji
GitHub username     : agungtrisutaji
Docker Hub username : agungtrisutaji
DagsHub username    : agungtrisutaji
Grafana dashboard   : agungtrisutaji
```

Use these names for submission artifacts:

```text
SMSML_Agung_Trisutaji_Aprian
Eksperimen_SML_Agung_Trisutaji_Aprian.txt
telco_customer_churn_preprocessing
telco-customer-churn-agungtrisutaji
agungtrisutaji/telco-churn-mlops:latest
```

## 3. Dataset

Dataset:

```text
Telco Customer Churn
```

Source:

```text
Kaggle: blastchar/telco-customer-churn
```

Raw file path:

```text
Membangun_model/telco_customer_churn_preprocessing/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

Problem type:

```text
Binary classification
```

Target column:

```text
Churn
```

Expected target mapping:

```text
No  -> 0
Yes -> 1
```

Main business objective:

```text
Predict whether a customer is likely to churn.
```

Recommended primary metric:

```text
F1-score
```

Recommended secondary metrics:

```text
accuracy
precision
recall
roc_auc
```

## 4. Notebook Requirement

The notebook must follow `Template_Eksperimen_MSML.ipynb`.

The notebook should include:

1. Dataset introduction.
2. Import library.
3. Dataset loading.
4. Exploratory Data Analysis.
5. Data preprocessing.

The notebook should clearly explain:

- source of dataset;
- meaning of target variable;
- number of rows and columns;
- missing values;
- duplicated rows;
- numeric and categorical columns;
- target distribution;
- key feature distributions;
- preprocessing decisions;
- why each preprocessing step is needed.

The notebook is for analysis and explanation. The reproducible preprocessing must also be implemented in a separate Python script.

## 5. Preprocessing Requirements

Create:

```text
Membangun_model/telco_customer_churn_preprocessing/preprocess.py
```

The preprocessing script must:

1. Load the raw CSV.
2. Validate that the dataset exists.
3. Convert `TotalCharges` to numeric.
4. Handle missing values.
5. Drop `customerID` from features.
6. Convert `Churn` to numeric target.
7. Split data into train and test with stratification.
8. Fit preprocessing only on train data to prevent data leakage.
9. Use `ColumnTransformer`.
10. Use median imputation and standard scaling for numeric columns.
11. Use most-frequent imputation and one-hot encoding for categorical columns.
12. Save transformed train and test data.
13. Save target train and test data.
14. Save fitted preprocessor.
15. Save feature names.
16. Save preprocessing summary.

Expected output folder:

```text
Membangun_model/telco_customer_churn_preprocessing/processed/
```

Expected outputs:

```text
X_train.csv
X_test.csv
y_train.csv
y_test.csv
feature_names.json
preprocessing_summary.json
```

Expected artifact folder:

```text
Membangun_model/telco_customer_churn_preprocessing/artifacts/
```

Expected artifact:

```text
preprocessor.pkl
```

## 6. Model Training Requirements

Create:

```text
Membangun_model/modelling.py
```

The script must:

1. Run preprocessing automatically if processed files are missing.
2. Load processed train and test files.
3. Train at least two baseline models:
   - LogisticRegression
   - RandomForestClassifier
4. Track experiments with MLflow.
5. Use DagsHub/MLflow env vars if available.
6. Never hardcode tokens.
7. Log parameters.
8. Log metrics.
9. Log classification report.
10. Log confusion matrix image.
11. Log model artifact.
12. Log input example.
13. Log model signature.
14. Select best model by `f1_score`.
15. Save best model locally.

Expected local outputs:

```text
Membangun_model/artifacts/best_model.pkl
Membangun_model/artifacts/model_info.json
```

MLflow experiment name:

```text
telco-customer-churn-agungtrisutaji
```

## 7. Tuning Requirements

Create:

```text
Membangun_model/modelling_tuning.py
```

The script must:

1. Run lightweight hyperparameter tuning.
2. Be safe to run on GitHub Actions.
3. Use GridSearchCV or RandomizedSearchCV with a small search space.
4. Log best parameters to MLflow.
5. Log best metrics to MLflow.
6. Save tuned model locally.
7. Save tuning results as JSON.

Expected outputs:

```text
Membangun_model/artifacts/tuned_model.pkl
Membangun_model/artifacts/tuning_results.json
```

## 8. MLflow Project Requirement

Create:

```text
Membangun_model/MLproject
Membangun_model/conda.yaml
```

Required MLflow entry points:

```text
main
tuning
```

Expected commands:

```bash
cd Membangun_model
mlflow run . -e main
mlflow run . -e tuning
```

## 9. GitHub Actions Requirement

Create this GitHub Actions workflow at the current repository root:

```text
.github/workflows/mlops-ci.yml
```

The workflow should:

1. Run on `push`.
2. Run on `pull_request`.
3. Run on `workflow_dispatch`.
4. Set up Python 3.11.
5. Install dependencies.
6. Check dataset presence.
7. Run preprocessing.
8. Run baseline training.
9. Run tuning.
10. Upload processed data and model artifacts.
11. Check whether required secrets exist without printing values.
12. Build Docker image.
13. Push Docker image only if Docker Hub secrets exist.

Docker image tag:

```text
agungtrisutaji/telco-churn-mlops:latest
```

Required GitHub Actions secrets:

```text
DAGSHUB_USERNAME
DAGSHUB_TOKEN
MLFLOW_TRACKING_URI
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

## 10. Serving Requirement

Create serving files under:

```text
Monitoring dan Logging/
```

Required files:

```text
app.py
Dockerfile
requirements.txt
7.Inference.py
2.prometheus.yml
3.prometheus_exporter.py
README.md
```

Use FastAPI for serving.

Required endpoints:

```text
GET  /health
POST /predict
GET  /metrics
```

The `/predict` endpoint should accept raw Telco Customer Churn features and return:

```text
prediction
prediction_label
prediction_probability
```

The app must load:

```text
Membangun_model/telco_customer_churn_preprocessing/artifacts/preprocessor.pkl
Membangun_model/artifacts/best_model.pkl
```

If `tuned_model.pkl` exists, the app may use it as the preferred model.

## 11. Prometheus Requirement

Create:

```text
Monitoring dan Logging/2.prometheus.yml
```

Prometheus should scrape:

```text
http://127.0.0.1:8000/metrics
```

or, for Docker/Windows/WSL:

```text
host.docker.internal:8000
```

Prometheus metrics should include at least 10 metrics.

Recommended metrics:

```text
model_requests_total
model_predictions_total
model_prediction_errors_total
model_prediction_latency_seconds
model_positive_predictions_total
model_negative_predictions_total
model_input_missing_values_total
model_input_payload_size_bytes
model_health_status
model_probability_score
model_last_prediction_timestamp
model_loaded_status
```

## 12. Grafana Requirement

Grafana dashboard name:

```text
agungtrisutaji
```

Dashboard should show at least:

- request total;
- prediction total;
- positive predictions;
- negative predictions;
- prediction latency;
- prediction error total;
- input missing values;
- model health status;
- probability score;
- last prediction timestamp;
- model loaded status.

Grafana alerting should include at least 2 rules.

Recommended alert rules:

1. High prediction error count.
2. High prediction latency.
3. Model health status down.
4. Model loaded status down.

## 13. Screenshot Requirement

At the end, the user will manually capture screenshots.

Prepare placeholder folders:

```text
Monitoring dan Logging/1.bukti_serving/
Monitoring dan Logging/4.bukti monitoring Prometheus/
Monitoring dan Logging/5.bukti monitoring Grafana/
Monitoring dan Logging/6.bukti alerting Grafana/
```

Required final screenshots:

- MLflow dashboard.
- MLflow artifact/model.
- GitHub Actions workflow success.
- Docker Hub image.
- FastAPI serving health.
- Inference result.
- Prometheus target UP.
- Prometheus metrics query.
- Grafana dashboard named `agungtrisutaji`.
- Grafana alert rules.

## 14. Security Rules

Never commit:

```text
.env
API keys
access tokens
passwords
DAGSHUB_TOKEN
DOCKERHUB_TOKEN
MLFLOW credentials
```

Do not print secret values in CI logs.

Only check whether secrets exist using conditional logic.

## 15. Path Compatibility

Use `pathlib.Path` everywhere.

The project must work on:

- Windows;
- WSL Ubuntu;
- GitHub Actions Ubuntu runner.

Avoid hardcoded backslashes.

Use paths like:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
```

## 16. Final Submission Reminder

The final ZIP should be named:

```text
SMSML_Agung_Trisutaji_Aprian.zip
```

The ZIP should contain this workspace's required submission contents, starting with `Eksperimen_SML_Agung_Trisutaji_Aprian.txt`, `Membangun_model/`, `Workflow-CI.txt`, and `Monitoring dan Logging/`.

Do not create ZIP inside ZIP.

## 17. Monitoring and Optimization Learning Context

The project must align with the Dicoding learning material **Monitoring dan Optimasi ML**.

After the model is trained, evaluated, deployed, and served, the project must not stop at prediction functionality. The deployed ML service must also support:

- logging;
- monitoring;
- alerting;
- troubleshooting;
- optimization.

The monitoring system should observe both:

### Model Performance

Recommended monitored model-related signals:

- prediction count;
- positive prediction count;
- negative prediction count;
- prediction probability score;
- prediction distribution;
- input missing value count;
- inference error count;
- model loaded status;
- model health status.

If labels are available in a real production scenario, model quality metrics may also include:

- accuracy;
- precision;
- recall;
- F1-score;
- confusion matrix;
- ROC-AUC.

For this submission, the serving API may not have real production labels, so monitoring should focus on observable serving-time signals and prediction distribution.

### System Performance

Recommended monitored system-related signals:

- request count;
- request latency;
- throughput;
- error count;
- API health status;
- payload size;
- last prediction timestamp;
- service uptime/readiness.

The FastAPI service must expose metrics through:

```text
GET /metrics
```

Prometheus must scrape this endpoint periodically, and Grafana must use Prometheus as a data source.

The Grafana dashboard must be named:

```text
agungtrisutaji
```

The Grafana dashboard should include panels for at least:

- total requests;
- total predictions;
- prediction latency;
- prediction errors;
- positive churn predictions;
- negative churn predictions;
- input missing values;
- model health status;
- model loaded status;
- prediction probability score;
- last prediction timestamp.

Grafana alerting should include at least two alert rules.

Recommended alert rules:

1. High prediction latency.
2. High prediction error count.
3. Model health status down.
4. Model loaded status down.

The monitoring design should reflect this principle:

```text
Model serving
-> logging
-> monitoring
-> alerting
-> diagnosis
-> optimization / retraining / redeployment
```

The final submission should include screenshots proving:

- FastAPI service is running;
- inference endpoint returns prediction;
- Prometheus target is UP;
- Prometheus can query model metrics;
- Grafana dashboard `agungtrisutaji` displays metrics;
- Grafana alert rules are configured.
