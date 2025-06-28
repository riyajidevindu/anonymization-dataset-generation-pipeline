import json, os
from .config import settings
from .gemini_client import fetch_rows
from .sheets_client import build_sheet_rows, push_rows
from .prompt_definitions import PROMPT_MAP, PROMPT_SEQUENCE

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

def get_next_prompt_key():
    # Load current state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = {"last_used": None}

    # Rotate to the next type
    last = state.get("last_used")
    next_index = (PROMPT_SEQUENCE.index(last) + 1) % len(PROMPT_SEQUENCE) if last else 0
    next_key = PROMPT_SEQUENCE[next_index]

    # Save new state
    with open(STATE_FILE, "w") as f:
        json.dump({"last_used": next_key}, f)

    return next_key

def run():
    mode = get_next_prompt_key()
    prompt = PROMPT_MAP[mode]

    print(f"🔄 Generating rows in '{mode}' mode...")

    raw = fetch_rows(prompt)
    raw = clean_gemini_json(raw)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print("❌ JSON Parse Error:", e)
        print("🔎 Cleaned response:\n", raw)
        return

    rows = list(build_sheet_rows(data))
    push_rows(rows)
    print(f"✅ {len(rows)} rows written in mode: {mode}")

def clean_gemini_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        # Remove markdown fence and optional language specifier
        parts = raw.split("```")
        if len(parts) > 1:
            body = parts[1].strip()
            # Remove the first line if it's a language tag like 'json'
            lines = body.splitlines()
            if lines and lines[0].strip().lower() == "json":
                return "\n".join(lines[1:]).strip()
            return body
    return raw
