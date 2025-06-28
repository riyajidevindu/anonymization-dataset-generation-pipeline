import datetime, json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from .config import settings

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def _service():
    creds = Credentials.from_service_account_file(
        settings.SA_FILE, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)

def push_rows(rows):
    svc = _service().spreadsheets()
    body = {"values": rows}
    svc.values().append(
        spreadsheetId=settings.SHEET_ID,
        range="Employment, Education & Social Context!A1", 
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",  
        body=body
    ).execute()

def build_sheet_rows(parsed_json):
    for r in parsed_json:
        yield [
            r.get("original", ""),
            r.get("need_anonymization", ""),
            r.get("anonymized") or "",
            ", ".join(r.get("pii_identifiers", [])),
            r.get("anonymization_technique", ""),
            r.get("improved_prompt", ""),
            datetime.datetime.now().isoformat()  
        ]
