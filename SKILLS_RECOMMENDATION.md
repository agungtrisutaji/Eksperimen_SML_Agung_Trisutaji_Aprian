# SKILLS_RECOMMENDATION.md

## Purpose

This file lists recommended skills or skill categories to enable for the coding agent before working on this Dicoding MLOps submission.

The project intentionally uses a tabular classification dataset, not NLP or computer vision, so the recommended skills should focus on Python, scikit-learn, MLflow, CI/CD, Docker, FastAPI, Prometheus, Grafana, and technical documentation.

## Recommended High-Priority Skills

Use these first if available in `skills.sh` or another trusted skill source.

| Priority | Skill / Category Keyword | Purpose |
|---:|---|---|
| 1 | `python-project` / `python-engineering` | Project structure, `.venv`, CLI scripts, pathlib, robust error handling |
| 1 | `data-science-python` | pandas, EDA, train-test split, preprocessing |
| 1 | `scikit-learn` | Pipeline, ColumnTransformer, metrics, model training |
| 1 | `mlflow` / `experiment-tracking` | MLflow Tracking, model logging, model signature, artifacts |
| 1 | `github-actions` / `ci-cd` | Workflow YAML, secrets check, artifact upload, Docker build |
| 1 | `docker` / `containerization` | Dockerfile, image build, local container run |
| 1 | `fastapi` / `api-serving` | Health endpoint, predict endpoint, request validation |
| 1 | `prometheus` / `metrics` | `/metrics`, counters, gauges, histograms |
| 1 | `grafana` / `observability` | Dashboard and alert rule planning |

## Recommended Medium-Priority Skills

| Priority | Skill / Category Keyword | Purpose |
|---:|---|---|
| 2 | `markdown-docs` / `technical-writing` | README, Workflow-CI.txt, DagsHub.txt |
| 2 | `jupyter-notebook` | Filling `Template_Eksperimen_MSML.ipynb` |
| 2 | `pytest` / `testing` | Smoke tests for preprocessing, model load, and endpoint |
| 2 | `security-secrets` | Prevent token leaks and bad GitHub Actions logging |
| 2 | `kaggle-dataset` | Optional support for dataset documentation and download instruction |

## Skills to Avoid for This Project

Avoid these unless the project scope changes:

```text
NLP
computer-vision
deep-learning-heavy
kubernetes
cloud-deployment
airflow
spark
llm
streamlit
```

Reason: this submission is intentionally scoped to a tabular classification MLOps workflow. Adding heavy infrastructure or unrelated ML domains may increase complexity without improving the submission score.

## Skill Safety Checklist

Before enabling a skill:

1. Read its `SKILL.md`.
2. Check whether it runs scripts automatically.
3. Check whether it can modify files.
4. Check whether it can access secrets.
5. Prefer official, trusted, and version-controlled skills.
6. Do not enable skills that ask to print tokens, `.env`, credentials, or secret values.
7. Do not enable skills that override project structure without asking.

## Minimal Skill Set

If you want to keep the agent simple, use only:

```text
python-project
data-science-python
scikit-learn
mlflow
github-actions
docker
fastapi
prometheus
grafana
technical-writing
```
