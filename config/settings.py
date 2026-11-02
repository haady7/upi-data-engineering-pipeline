from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports"

for folder in (RAW_DIR, PROCESSED_DIR, REPORTS_DIR):
    folder.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL")
