# HOW_TO_USE_CONTEXT_FILES.md

## Files Included

This package contains:

```text
AGENTS.md
MSML_PROJECT_CONTEXT.md
SKILLS_RECOMMENDATION.md
CODEX_INITIAL_PROMPT.md
HOW_TO_USE_CONTEXT_FILES.md
```

## Where to Put These Files

Copy these files to the **root of your current `MSML` workspace/repository**.

Expected placement:

```text
MSML/
├── AGENTS.md
├── MSML_PROJECT_CONTEXT.md
├── SKILLS_RECOMMENDATION.md
├── CODEX_INITIAL_PROMPT.md
├── Template_Eksperimen_MSML.ipynb
├── Membangun_model/
└── Monitoring dan Logging/
```

## How to Use

1. Copy all `.md` files from this package to your repository root.
2. Confirm the dataset exists at:

```text
Membangun_model/telco_customer_churn_preprocessing/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

3. Open Codex in the repository.
4. Ask Codex to read `AGENTS.md`, `MSML_PROJECT_CONTEXT.md`, and `SKILLS_RECOMMENDATION.md`.
5. Paste the contents of `CODEX_INITIAL_PROMPT.md` into Codex.
6. Let Codex implement the project structure and scripts.
7. After Codex finishes, run the local validation commands.
8. Push to GitHub and verify GitHub Actions.

## Local `.venv` Setup

Because the project is worked on directly inside the `MSML` folder, create `.venv` in that folder.

For WSL/Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
python -m pip install -r "Monitoring dan Logging/requirements.txt"
```

For Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r Membangun_model/requirements.txt
python -m pip install -r "Monitoring dan Logging/requirements.txt"
```

Make sure `.venv/` is listed in `.gitignore`.

## Important

Do not commit secrets or `.env` files.

GitHub Actions secrets should already be configured in the repository settings:

```text
DAGSHUB_USERNAME
DAGSHUB_TOKEN
MLFLOW_TRACKING_URI
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

GitHub will not show secret values after saving them. This is expected.
