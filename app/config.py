import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # Load environment variables

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID")
    SERVICE_ACCOUNT_FILE: str = os.getenv("SERVICE_ACCOUNT_FILE")
    NUM_ROWS: int = int(os.getenv("NUM_ROWS", 10))
    SHEET_TAB_NAME: str = os.getenv("SHEET_TAB_NAME")
    SHEET_TABS: list = os.getenv("SHEET_TABS", "Sheet1,Sheet2,Sheet3,Sheet4").split(",")
    WAIT_SECONDS: int = int(os.getenv("WAIT_SECONDS", 60))  

settings = Settings()
