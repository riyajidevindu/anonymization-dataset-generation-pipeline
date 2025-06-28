import requests
import json
from .config import settings

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def fetch_rows(system_prompt: str) -> str:
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_prompt}]}
        ]
    }
    try:
        r = requests.post(
            f"{URL}?key={settings.GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        r.raise_for_status()
        response_json = r.json()
    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        return ""
    except ValueError as e:
        print("❌ Failed to parse JSON response:", e)
        print("🔎 Raw response text:", r.text)
        return ""

    # Check if structure is valid
    try:
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        print("❌ Gemini API structure unexpected")
        print("🔎 Full Response:\n", json.dumps(response_json, indent=2))
        return ""

