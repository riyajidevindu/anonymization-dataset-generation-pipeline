from .config import settings

SYSTEM_PROMPT_YES = f"""
You are a data engineering assistant creating realistic, real-world user prompts that require **anonymization**.

Generate exactly {settings.NUM_ROWS} JSON objects where:
- Each row represents a user input related to Employment, Education, or Social Context.
- These prompts should **contain Personally Identifiable Information (PII)** such as names, salaries, companies, phone numbers, email addresses, institutions, or specific locations.

Each JSON object must include:
- "original": A rich, natural user input (at least 20–30 words), similar to what users might type into a chatbot or search engine.
- "need_anonymization": Always set to "Yes"
- "anonymized": A properly anonymized version of the original prompt. Use appropriate anonymization strategy.
- "pii_identifiers": A list of detected PII elements (e.g., Name, Email, Salary, Company)
- "anonymization_technique": One of "mask", "generalise", "pseudonymise", or "redact"
- "improved_prompt": A privacy-enhanced version of the user prompt that keeps intent but removes PII (can use rephrasing, generalization, placeholders, etc.)

Ensure:
- Prompts are realistic, varied, and human-like in tone.
- Include multiple domains like hiring, college admissions, workplace interactions, HR data, social platforms, professional networking, etc.
- Use people’s names, cities, exact job titles, emails, salary figures, and company names in the "original".

Output only a JSON array of exactly {settings.NUM_ROWS} entries. Do not include explanations or markdown.
"""


SYSTEM_PROMPT_NO = f"""
You are a data engineering assistant creating realistic user prompts related to Employment, Education, and Social Context that **do not require anonymization**.

Generate exactly {settings.NUM_ROWS} JSON objects.

Each object must include:
- "original": A natural, human-like user prompt (minimum 20–30 words) that does **not contain real PII**.
- "need_anonymization": Always set to "No"
- "anonymized": Leave as null or empty string
- "pii_identifiers": Leave as an empty list
- "anonymization_technique": Leave as null or empty string
- "improved_prompt": Either same as original or a slightly enhanced version (optional)

### Prompt Diversity Requirements:
- **Include a few "tricky" prompts**: These look like they contain names, places, institutions, etc., but are either generic or public (e.g., “Harvard University”, “New York City”, “LinkedIn”).
- The tricky prompts must **not include private PII** but should **test anonymization models** by being confusing.
- The rest of the prompts can be typical HR, job search, education, resume, workplace, or social context queries **with no PII**.

Output only a JSON array of exactly {settings.NUM_ROWS} rows. No extra text or formatting.
"""


PROMPT_MAP = {
    "Yes": SYSTEM_PROMPT_YES,
    "No": SYSTEM_PROMPT_NO,
}

PROMPT_SEQUENCE = ["Yes", "No"]  
