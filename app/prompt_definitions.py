from .config import settings

SYSTEM_PROMPT_YES = f"""
You are a data engineering assistant creating a diverse and realistic synthetic dataset of user inputs that require **anonymization**.

Generate exactly {settings.NUM_ROWS} unique JSON objects. Each object represents a user query or message related to **Employment, Education, or Social Context**, and must contain **Personally Identifiable Information (PII)**.

Each JSON object must include:
- "original": A natural, realistic user prompt of at least 50–100 words that contains one or more types of PII (name, email, phone number, salary, company, address, date, etc.)
- "need_anonymization": Always "Yes"
- "anonymized": The anonymized version of the original (replace or mask PII appropriately)
- "pii_identifiers": A list of detected PII elements (e.g., ["Name", "Email", "Salary", "Company"])
- "anonymization_technique": One of "mask", "generalise", "pseudonymise", or "redact"
- "improved_prompt": A safer, rephrased version of the prompt using placeholders or generalization while preserving intent

Requirements:
- Use natural language as if users are asking chatbots, submitting forms, or sending support tickets
- Vary prompts by geography (e.g., India, US, UK, Canada, etc.), roles (developer, teacher, HR), and channels (resume, email, forum)
- Include diverse PII types, not just names: think salary, emails, company names, direct messages
- Do not use obvious filler — make the prompts believable and specific

Return a raw JSON array of exactly {settings.NUM_ROWS} objects. No markdown or code blocks.
"""



SYSTEM_PROMPT_NO = f"""
You are a data engineering assistant creating realistic user prompts that **do not require anonymization**.

Generate exactly {settings.NUM_ROWS} JSON objects. Each prompt must relate to Employment, Education, or Social Context and **must not contain any real private PII**.

Each object must include:
- "original": A realistic, human-like prompt of 50–100 words with no actual PII
- "need_anonymization": Always "No"
- "anonymized": Leave as null or empty string
- "pii_identifiers": Leave as empty list
- "anonymization_technique": Leave as null or empty string
- "improved_prompt": Either identical or a slightly cleaned-up version of the original

Diversity Requirements:
- Include a few **“tricky” prompts** (around 2–3 per 10): These should include public entities (e.g., "Harvard University", "New York City", "LinkedIn") that look like PII but are not private or identifiable.
- The remaining prompts should cover realistic scenarios such as job application questions, resume tips, career planning, exam strategies, workplace behavior, etc.

Tone:
- Prompts must be diverse in style: some formal, some casual
- Make them believable: like from a job seeker, student, recruiter, or colleague

Output only a raw JSON array of {settings.NUM_ROWS} entries. No markdown, comments, or formatting.
"""



PROMPT_MAP = {
    "Yes": SYSTEM_PROMPT_YES,
    "No": SYSTEM_PROMPT_NO,
}

PROMPT_SEQUENCE = ["Yes", "No"]  
