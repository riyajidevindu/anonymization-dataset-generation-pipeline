# Anonymization Dataset Pipeline

Generate realistic Employment, Education & Social-Context prompts, anonymize sensitive ones, and stream everything straight into Google Sheets. This project also includes a pipeline to extract PII values from the generated dataset.

---

## 📁 Folder Structure

```
anonymization-pipeline/
│
├─ app/                      ← all Python code
│   ├─ __init__.py
│   ├─ config.py             ← loads secrets from .env
│   ├─ prompt_definitions.py ← system prompts (Yes / No)
│   ├─ gemini_client.py      ← calls Gemini API
│   ├─ sheets_client.py      ← Google Sheets helper
│   ├─ generate_dataset.py   ← rotates prompts, pushes rows
│   ├─ extract_pii_values.py ← extracts PII values from the dataset
│   └─ state.json            ← remembers last prompt mode
│
├─ credentials/              ← **keep out of Git!**
│   └─ service_account.json  ← Google service-account key
│
├─ .env                      ← real secrets (not committed)
├─ .env.example              ← template with dummy values
├─ .gitignore
├─ requirements.txt
├─ run.py                    ← entry point: `python run.py`
└─ README.md                 ← you are here
```

---

## ✨ What the Pipeline Does

### Dataset Generation
1. **Rotates prompts**: first run → PII-heavy (*Yes*), second run → safe / tricky (*No*), then repeats.
2. **Calls Gemini-Pro** (or Flash) to generate `settings.NUM_ROWS` dataset rows.
3. **Cleans & parses** the JSON returned by Gemini.
4. **Appends** new rows to the chosen Google Sheet/tab.
5. **Logs** the API response and remembers which prompt type was last used.

### PII Value Extraction
1.  **Processes each sheet tab in parallel.**
2.  **Identifies rows** where "Need Anonymization" is "yes" and "PII Value" is empty.
3.  **Calls the Gemini API** to extract PII values from the "Orginal" text.
4.  **Cleans the API response** to ensure only comma-separated values are stored.
5.  **Updates the "PII Value" column** for each row.
6.  **Allows graceful stopping** with Ctrl+C.

---

## 🔧 Prerequisites

| Requirement               | Notes                                                                                     |
| ------------------------- | ----------------------------------------------------------------------------------------- |
| **Python 3.9+**           | Any modern CPython works                                                                  |
| Google **Gemini API key** | Create in [Google AI Studio](https://aistudio.google.com/app/apikey)                      |
| **Google Cloud project**  | Enable **Google Sheets API**                                                              |
| **Service Account JSON**  | Give the service account *Editor* access to your target Sheet                             |
| **Google Sheet**          | Create a sheet; add a tab named `Employment, Education & Social Context`; row 1 = headers |

---

## 🚀 Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/<you>/anonymization-pipeline.git
   cd anonymization-pipeline
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   # macOS/Linux
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Add secrets**

   ```bash
   cp .env.example .env        # then open .env in an editor
   mkdir -p credentials
   mv <downloaded-key>.json credentials/service_account.json
   ```

   Edit `.env` and fill in:

   ```ini
   GEMINI_API_KEY=AIzaSy...
   GOOGLE_SHEET_ID=1AbCdefGhij...        # spreadsheet ID from the URL
   SERVICE_ACCOUNT_FILE=credentials/service_account.json
   NUM_ROWS=10                           # rows generated per run
   SHEET_TAB_NAME=Employment, Education & Social Context
   SHEET_TABS=Sheet1,Sheet2,Sheet3,Sheet4 # tabs for PII extraction
   ```

5. **Share the Sheet with your service account**

   - Open the Sheet → **Share** → add `your-service@project.iam.gserviceaccount.com` → **Editor**.

6. **Initial test**

   ```bash
   # Generate dataset
   python run.py generate

   # Extract PII values
   python run.py extract_pii
   ```

   You should see `📤 Writing 10 rows...` and a successful API response for generation, and the PII extraction process should start.

---

## 🏃 Running Regularly

### Dataset Generation (Linux / macOS - cron)

```
# run every hour at minute 0
0 * * * * /full/path/venv/bin/python /full/path/anonymization-pipeline/run.py generate >> /full/path/pipeline.log 2>&1
```

### Dataset Generation (Windows Task Scheduler)

1. Create Basic Task → Trigger: Daily / Hourly.
2. Action: *Start a Program* → `python.exe`.
3. Arguments: `C:\...\anonymization-pipeline\run.py generate`.
4. Start in: `C:\...\anonymization-pipeline`.

### PII Value Extraction

Run this command manually when you need to update the "PII Value" column:
```bash
python run.py extract_pii
```
You can stop the process at any time by pressing **Ctrl+C**.

---

## 🔄 Changing Prompt Behaviour

- **Rows per run** → edit `NUM_ROWS` in `.env`.
- **Prompt content** → edit `app/prompt_definitions.py`.
- **Rotation order** → change `PROMPT_SEQUENCE` list.

---

## 🧰 Troubleshooting

| Symptom            | Fix                                                                                       |
| ------------------ | ----------------------------------------------------------------------------------------- |
| `JSON Parse Error` | Gemini wrapped output in markdown - cleanup handled in code. Check `clean_gemini_json()`. |
| Rows not written   | Ensure service account has *Editor* rights and `SHEET_TAB_NAME` matches tab exactly.      |
| Quota errors       | Check AI Studio quota dashboard or upgrade plan.                                          |
| Duplicate rows     | Use timestamp column (already included) or add logic to skip if identical.                |
| Dirty PII values   | The `clean_pii_values` function in `extract_pii_values.py` should handle this. You can improve the cleaning logic there if needed. |
