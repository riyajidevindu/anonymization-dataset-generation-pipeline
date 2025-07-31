import requests, json, time
from .config import settings

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def fetch_rows(system_prompt: str) -> str:
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_prompt}]}
        ]
    }
    retries = 0
    while retries < 5:
        try:
            r = requests.post(
                f"{URL}?key={settings.GEMINI_API_KEY}",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=60
            )
            r.raise_for_status()
            response_json = r.json()
            # Check if structure is valid
            try:
                return response_json["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError) as e:
                print("❌ Gemini API structure unexpected")
                print("🔎 Full Response:\n", json.dumps(response_json, indent=2))
                return ""
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed ({e}), retrying in {2**retries} seconds...")
            time.sleep(2**retries)
            retries += 1
        except ValueError as e:
            print("❌ Failed to parse JSON response:", e)
            print("🔎 Raw response text:", r.text)
            return ""
    print("❌ Failed to fetch from Gemini API after multiple retries.")
    return ""
