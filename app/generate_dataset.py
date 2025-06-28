import json, sys
from .gemini_client import fetch_rows
from .sheets_client import push_rows, build_sheet_rows

def run():
    raw = fetch_rows()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit("❌ Gemini returned invalid JSON")

    rows = list(build_sheet_rows(data))
    push_rows(rows)
    print(f"✅ Wrote {len(rows)} rows to Google Sheets")

if __name__ == "__main__":
    run()
