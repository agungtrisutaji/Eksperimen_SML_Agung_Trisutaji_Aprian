from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGING_NAME = "SMSML_Agung_Trisutaji_Aprian"
ZIP_NAME = f"{STAGING_NAME}.zip"

EXCLUDED_NAMES = {
    ".venv",
    ".git",
    ".env",
    "__pycache__",
    ".pytest_cache",
    "mlruns",
    "AGENTS.md",
    "MSML_PROJECT_CONTEXT.md",
    "CODEX_INITIAL_PROMPT.md",
    "SKILLS_RECOMMENDATION.md",
    "HOW_TO_USE_CONTEXT_FILES.md",
    "VENV_SETUP.md",
}

REQUIRED_ITEMS = [
    "Eksperimen_SML_Agung_Trisutaji_Aprian.txt",
    "Membangun_model",
    "Workflow-CI.txt",
    "Monitoring dan Logging",
]


def ignore_submission_noise(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDED_NAMES or name.endswith(".pyc")}


def copy_item(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination, ignore=ignore_submission_noise)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def prepare_submission(make_zip: bool) -> Path:
    staging_dir = ROOT / STAGING_NAME
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True)

    for item in REQUIRED_ITEMS:
        source = ROOT / item
        if not source.exists():
            raise FileNotFoundError(f"Required submission item not found: {source}")
        copy_item(source, staging_dir / item)

    if make_zip:
        zip_path = ROOT / ZIP_NAME
        if zip_path.exists():
            zip_path.unlink()
        shutil.make_archive(str(zip_path.with_suffix("")), "zip", ROOT, STAGING_NAME)
        print(f"ZIP created: {zip_path}")

    print(f"Submission staging folder created: {staging_dir}")
    return staging_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare Dicoding MSML submission folder.")
    parser.add_argument(
        "--zip",
        action="store_true",
        help=f"Also create {ZIP_NAME}. Do not put another ZIP inside it.",
    )
    args = parser.parse_args()
    prepare_submission(make_zip=args.zip)


if __name__ == "__main__":
    main()

