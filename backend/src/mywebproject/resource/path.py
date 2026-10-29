from pathlib import Path

RESOURCE_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = RESOURCE_DIR.parent
SRC_DIR = PACKAGE_DIR.parent
BACKEND_DIR = SRC_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent

ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE_FILE = PROJECT_ROOT / ".env.example"

DATA_DIR = BACKEND_DIR / "data"
LOG_DIR = BACKEND_DIR / "logs"
UPLOAD_DIR = DATA_DIR / "uploads"

RUNTIME_DIRS = (DATA_DIR, LOG_DIR, UPLOAD_DIR)


def ensure_runtime_dirs() -> None:
    for directory in RUNTIME_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
