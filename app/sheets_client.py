import datetime, json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from .config import settings

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def _service():
    creds = Credentials.from_service_account_file(
        settings.SERVICE_ACCOUNT_FILE, scopes=SCOPES)  # ✅ fixed key name
    return build("sheets", "v4", credentials=creds)

def current_row_count():
    svc = _service().spreadsheets()
    response = svc.values().get(
        spreadsheetId=settings.SHEET_ID,
        range=f"{settings.SHEET_TAB_NAME}!A:A"  # ✅ use dynamic sheet name
    ).execute()
    return len(response.get("values", []))

def push_rows(rows):
    if current_row_count() > 1000:
        print("⚠️ Sheet already has over 1000 rows. Skipping this batch.")
    else:
        svc = _service().spreadsheets()
        body = {"values": rows}
        svc.values().append(
            spreadsheetId=settings.SHEET_ID,
            range=f"{settings.SHEET_TAB_NAME}!A1",  # ✅ dynamic tab name
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        print(f"📤 Wrote {len(rows)} rows to sheet.")

def build_sheet_rows(parsed_json):
    for r in parsed_json:
        yield [
            r.get("original", ""),
            r.get("need_anonymization", ""),
            r.get("anonymized") or "",
            ", ".join(r.get("pii_identifiers", [])),
            r.get("anonymization_technique", ""),
            r.get("improved_prompt", ""),
            datetime.datetime.utcnow().isoformat()  # ✅ better: use UTC
        ]
