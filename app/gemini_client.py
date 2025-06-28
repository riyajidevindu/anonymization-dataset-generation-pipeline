import requests
from .config import settings

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

SYSTEM_PROMPT = f"""
You are a data engineering assistant. Generate {settings.NUM_ROWS} synthetic dataset rows related to Employment, Education, and Social Context.

Each row must be a JSON object with the following fields:
- "original": The original user prompt or text.
- "need_anonymization": One of "yes", "no", or "tricky".
  - "yes" means the text contains PII and requires anonymization.
  - "no" means the text contains no PII.
- "anonymized": The anonymized version of the prompt, if applicable. Leave as null or empty string for "no" rows.
- "pii_identifiers": A list of detected PII elements (e.g., Name, Phone, Location, Salary, Email, Company).
- "anonymization_technique": One of "mask", "generalise", "pseudonymise", or "redact". Choose the most appropriate for each case.
- "improved_prompt": An improved or safer version of the prompt using privacy-preserving techniques or prompt-enhancement.

Ensure:
- The total number of rows is exactly {settings.NUM_ROWS}.
- About 50% of rows have "need_anonymization": "yes"
- About 50% have "need_anonymization": "no"
- Use diverse examples across regions, job titles, education levels, and cultural contexts.

Output only a JSON array of objects with no explanations, comments, or markdown formatting. The output must be valid JSON.
"""

def fetch_rows():
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}
        ]
    }
    r = requests.post(f"{URL}?key={settings.GEMINI_API_KEY}",
                      headers={"Content-Type": "application/json"},
                      json=payload,
                      timeout=60)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
