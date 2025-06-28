import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")       # load env vars

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID")
    SA_FILE: str = os.getenv("SERVICE_ACCOUNT_FILE")
    NUM_ROWS: int = int(os.getenv("NUM_ROWS", 10))

settings = Settings()
