from pathlib import Path

CURRENT_FILE = Path.cwd(__file__).resolve()
ROOT_DIR = CURRENT_FILE.parent.parent.parent
ENV_FILE = ROOT_DIR / ".env.example"
