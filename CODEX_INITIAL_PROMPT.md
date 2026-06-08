# CODEX_INITIAL_PROMPT.md

> Use this version only when Codex is opened inside the `MSML` folder/workspace. Do **not** create a nested `MSML/` folder.


Copy this prompt into Codex after placing `AGENTS.md`, `MSML_PROJECT_CONTEXT.md`, and `SKILLS_RECOMMENDATION.md` in the repository root.

---

Before making changes, read these files carefully:

1. `AGENTS.md`
2. `MSML_PROJECT_CONTEXT.md`
3. `SKILLS_RECOMMENDATION.md`

Follow the project context exactly.

Prepare the current `MSML` workspace submission structure for the Dicoding final project **Membangun Sistem Machine Learning** using the **Telco Customer Churn** dataset.

Repository identity:

- Student name: Agung Trisutaji Aprian
- Dicoding username: agungtrisutaji
- GitHub username: agungtrisutaji
- Docker Hub username: agungtrisutaji
- DagsHub username: agungtrisutaji
- Grafana dashboard name: agungtrisutaji

Dataset:

- Dataset: Telco Customer Churn
- Source: Kaggle `blastchar/telco-customer-churn`
- Target: `Churn`
- Type: binary classification
- Raw dataset path:
  `Membangun_model/telco_customer_churn_preprocessing/WA_Fn-UseC_-Telco-Customer-Churn.csv`

Additional `.venv` requirement:

- All local dependencies must be installed into `.venv` at the current workspace root.
- Do not install dependencies globally.
- Add `.venv/` to `.gitignore`.
- Update README instructions to use `.venv`.
- Update GitHub Actions so the runner creates `.venv`, activates it, installs dependencies there, and runs preprocessing/training commands inside that virtual environment.
- For local MLflow Project commands, document `--env-manager local` because dependencies are already installed in `.venv`.
- Keep `conda.yaml` for MLflow compatibility, but `.venv` is the main local workflow.

Rules:

- Preserve existing files, especially `Template_Eksperimen_MSML.ipynb`.
- Do not delete user files.
- Do not hardcode secrets.
- Use environment variables for all credentials.
- Use `pathlib.Path`.
- Ensure all scripts can run from repository root.
- Implement clean, simple, maintainable code.
- Do not create ZIP inside ZIP.
- Prepare screenshot placeholder folders, but do not invent screenshots.

Tasks:

1. Inspect the existing repository tree.
2. Create or complete the required submission structure in the current workspace root.
3. Implement preprocessing script.
4. Implement baseline modelling script with MLflow.
5. Implement lightweight tuning script with MLflow.
6. Add MLflow Project files.
7. Add GitHub Actions workflow.
8. Add FastAPI serving app.
9. Add Prometheus metrics and config.
10. Add inference test script.
11. Add Dockerfile and serving requirements.
12. Add README files and submission documentation.
13. Validate that the required commands are documented and likely to run.
14. Summarize changed files, commands to run, assumptions, and remaining manual screenshot tasks.

Required commands from repository root after activating `.venv`:

```bash
python Membangun_model/telco_customer_churn_preprocessing/preprocess.py
python Membangun_model/modelling.py
python Membangun_model/modelling_tuning.py
python "Monitoring dan Logging/7.Inference.py"
```

Required MLflow Project commands:

```bash
cd Membangun_model
mlflow run . -e main --env-manager local
mlflow run . -e tuning --env-manager local
```

Required GitHub Actions secrets:

```text
DAGSHUB_USERNAME
DAGSHUB_TOKEN
MLFLOW_TRACKING_URI
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

Do not print secret values.

At the end, provide:

1. Created/modified files.
2. Exact commands to create/activate `.venv`, install dependencies, and run locally.
3. GitHub Actions notes.
4. Docker run notes.
5. Prometheus/Grafana notes.
6. Manual screenshots still required.
7. Any assumptions made.
