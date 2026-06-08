# VENV_SETUP.md

## Requirement

Install all local dependencies inside `.venv` at the current `MSML` workspace root.

Do not install project dependencies globally.

Do not commit `.venv/`.

## WSL/Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
python -m pip install -r "Monitoring dan Logging/requirements.txt"
```

## Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
python -m pip install -r "Monitoring dan Logging/requirements.txt"
```

## Run Commands After Activation

```bash
python Membangun_model/telco_customer_churn_preprocessing/preprocess.py
python Membangun_model/modelling.py
python Membangun_model/modelling_tuning.py
python "Monitoring dan Logging/7.Inference.py"
```

## MLflow Project

Because dependencies are already installed in `.venv`, use:

```bash
cd Membangun_model
mlflow run . -e main --env-manager local
mlflow run . -e tuning --env-manager local
```

## GitHub Actions

The workflow should create and use `.venv` in the runner:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
```

Run all subsequent Python commands from the activated `.venv`.
