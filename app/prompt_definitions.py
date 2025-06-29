from .config import settings

SYSTEM_PROMPT_YES = f"""
You are a data engineering assistant creating a rich, diverse synthetic dataset of realistic user prompts that contain Personally Identifiable Information (PII) and therefore require **anonymization**.

Generate exactly {settings.NUM_ROWS} unique JSON objects. Each object must relate to Employment, Education, or Social Context.

---

Each object must include:
- "original": A detailed, natural, human-like prompt of 50–100 words that includes one or more types of PII.
- "need_anonymization": Always "Yes"
- "anonymized": The anonymized version of the original (PII removed or replaced appropriately)
- "pii_identifiers": A list of identified PII types (e.g., ["Name", "Email", "Phone", "Company", "Salary", "Location", "Institution"])
- "anonymization_technique": One of:
    - "mask": Replace PII with placeholders like [NAME], [EMAIL], etc.
    - "generalise": Replace PII with **meaningful non-identifying descriptions** (e.g., "a top-tier university", "a large software company")
    - "pseudonymise": Replace with realistic but **fictional** values (e.g., "John Carter", "brightfuture@example.com")
    - "redact": Remove the PII completely without replacing it
- "improved_prompt": A privacy-preserving version of the prompt using rephrasing, placeholders, or generalization — ensure the original meaning is preserved

---

Requirements:
- Use varied and realistic scenarios: chatbot queries, support messages, job applications, admissions, work-related complaints, HR data, resumes, etc.
- Include prompts from different regions (e.g., India, US, UK, Canada, etc.), sectors (IT, teaching, marketing, health), and demographics (students, employees, HR staff)
- Mix tone: some formal, some casual, some professional
- Avoid repetitive phrasing and obvious filler — keep the prompts natural and purposeful

---

Important:
- **Generalisation must NOT use placeholders. It must preserve meaning while hiding identity.**
- Vary the **anonymization_technique** across rows where appropriate.
- Do NOT return explanations or markdown — just a raw JSON array of {settings.NUM_ROWS} objects.

---

Examples:

Original:  
"I’m Jane Smith and I just got a job offer from Amazon in Seattle with a $120,000 salary. Should I negotiate or accept it?"

→ pii_identifiers: ["Name", "Company", "Location", "Salary"]  
→ anonymization_technique: "generalise"  
→ anonymized: "I recently received a job offer from a major tech company in the Pacific Northwest with a six-figure salary. Should I negotiate or accept it?"

---

Original:  
"My phone number is 415-555-9876 and email is rachel@careerboost.com. I’m applying for a marketing analyst role at BrightEdge."

→ pii_identifiers: ["Phone", "Email", "Company"]  
→ anonymization_technique: "mask"  
→ anonymized: "My phone number is [PHONE] and email is [EMAIL]. I’m applying for a marketing analyst role at [COMPANY]."

---

Return only a JSON array of {settings.NUM_ROWS} rows. No markdown, code blocks, or explanations.
"""




SYSTEM_PROMPT_NO = f"""
You are a data engineering assistant generating a synthetic dataset of user prompts that **do not contain any private or identifiable PII**.

Generate exactly {settings.NUM_ROWS} unique JSON objects. Each object should simulate a user query related to **Employment, Education, or Social Context** that is completely safe and does not include sensitive personal information.

Each object must include:
- "original": A realistic user query or message (at least 50–100 words) that may mention **public entities** like companies, universities, or cities (e.g., "Google", "Harvard", "New York City") — but **must not contain actual private identifiers**
- "need_anonymization": Always "No"
- "anonymized": Leave as null or empty string
- "pii_identifiers": Empty list
- "anonymization_technique": Leave as null or empty string
- "improved_prompt": Can be the same or a slightly clearer version

Instructions:
- About 20–30% of prompts should **look like they contain PII** (e.g., names or places), but are **clearly public or generic**
- The rest should cover a broad range of real-world questions: resume advice, workplace tips, exam stress, interview prep, online courses, HR policies, etc.
- Vary tone: some formal (emails, reports), some casual (chat queries, student discussions)
- Include different speaker roles: job seekers, students, employees, HR reps, mentors

Return only a valid JSON array of {settings.NUM_ROWS} entries. No markdown or extra output.
"""


PROMPT_MAP = {
    "Yes": SYSTEM_PROMPT_YES,
    "No": SYSTEM_PROMPT_NO,
}

PROMPT_SEQUENCE = ["Yes", "No"]  
