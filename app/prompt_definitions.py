from .config import settings

SYSTEM_PROMPT_YES = f"""
You are a data engineering assistant creating a rich, diverse synthetic dataset of realistic user prompts that contain Personally Identifiable Information (PII) and therefore require **anonymization**.

Generate exactly {settings.NUM_ROWS} unique JSON objects. Each object must relate to **Location or Contact Information**.

---

Each object must include:
- "original": A detailed, natural, human-like prompt of 50–100 words that includes one or more types of PII.
- "need_anonymization": Always "Yes"
- "anonymized": The anonymized version of the original (PII removed or replaced appropriately)
- "pii_identifiers": A list of identified PII types (e.g., ["Address", "Phone", "Email", "Location", "GPS", "SocialMediaHandle"])
- "anonymization_technique": One of:
    - "mask": Replace PII with placeholders like [PHONE], [EMAIL], [ADDRESS], etc.
    - "generalise": Replace PII with **meaningful non-identifying descriptions** (e.g., "a southern neighborhood", "a business email", "a city in western India")
    - "pseudonymise": Replace with realistic but **fictional** values (e.g., "jacksonville@emailhub.com", "+1-303-456-7890", "123 Maple Avenue")
    - "redact": Remove the PII completely without replacing it
- "improved_prompt": A privacy-preserving version of the prompt using rephrasing, placeholders, or generalization — ensure the original meaning is preserved

---

Requirements:
- Use varied and realistic scenarios: delivery instructions, customer support, service signups, registration forms, real estate inquiries, navigation help, email exchanges, or feedback forms
- Include prompts from different regions (e.g., US, UK, India, Canada, etc.), settings (urban, rural, institutional), and tones (personal, formal, professional)
- Mix tones: some casual, some official, some technical
- Avoid repetitive phrasing and obvious filler — keep the prompts natural and purposeful

---

Important:
- **Generalisation must NOT use placeholders. It must preserve meaning while hiding identity.**
- Vary the **anonymization_technique** across rows where appropriate.
- Do NOT return explanations or markdown — just a raw JSON array of {settings.NUM_ROWS} objects.

---

Examples:

Original:  
"Hi, my name is Ravi and I live at 43 Rajiv Gandhi Street, Chennai. Please send the courier there before 6 PM."

→ pii_identifiers: ["Name", "Address", "Location"]  
→ anonymization_technique: "pseudonymise"  
→ anonymized: "Hi, my name is Karan and I live at 17 Greenfield Avenue, Mumbai. Please send the courier there before 6 PM."

---

Original:  
"You can reach me at james.rosen@outlook.com or call me on 917-555-2048 if you need to verify my account address."

→ pii_identifiers: ["Email", "Phone"]  
→ anonymization_technique: "mask"  
→ anonymized: "You can reach me at [EMAIL] or call me on [PHONE] if you need to verify my account address."

---

Return only a JSON array of {settings.NUM_ROWS} rows. No markdown, code blocks, or explanations.
"""


SYSTEM_PROMPT_NO = f"""
You are a data engineering assistant generating a synthetic dataset of user prompts that **do not contain any private or identifiable PII**.

Generate exactly {settings.NUM_ROWS} unique JSON objects. Each object should simulate a user query related to **Location or Contact Information** that is completely safe and does not include sensitive personal information.

Each object must include:
- "original": A realistic user query or message (at least 50–100 words) that may mention **public entities** like cities, regions, platforms, or tech tools — but **must not contain actual private identifiers**
- "need_anonymization": Always "No"
- "anonymized": Leave as null or empty string
- "pii_identifiers": Empty list
- "anonymization_technique": Leave as null or empty string
- "improved_prompt": Can be the same or a slightly clearer version

Instructions:
- About 20–30% of prompts should **look like they contain PII** (e.g., names or addresses), but are **clearly public or generic**
- The rest should include location-related help, contact preferences, UI questions, delivery zones, timezone queries, routing errors, etc.
- Vary tone: some formal (support tickets, platform FAQs), some casual (chat questions, informal help)
- Include different roles: customers, developers, drivers, admins, travelers, business users

Return only a valid JSON array of {settings.NUM_ROWS} entries. No markdown or extra output.
"""


PROMPT_MAP = {
    "Yes": SYSTEM_PROMPT_YES,
    "No": SYSTEM_PROMPT_NO,
}

PROMPT_SEQUENCE = ["Yes", "No"]
