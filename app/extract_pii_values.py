import json
import time
import threading
import re
from .config import settings
from .gemini_client import fetch_rows
from .sheets_client import get_all_rows, update_rows

def col_to_letter(col_idx):
    """Convert a 0-based column index to a column letter."""
    if col_idx < 0:
        return None
    
    letters = ""
    while col_idx >= 0:
        letters = chr(ord('A') + col_idx % 26) + letters
        col_idx = col_idx // 26 - 1
    return letters

def clean_pii_values(raw_text: str) -> str:
    """
    Cleans the raw output from the Gemini API to extract only the PII values.
    """
    # Remove markdown list characters and asterisks
    cleaned_text = re.sub(r'[\*\-`]', '', raw_text).strip()
    
    # Split by lines and process each line
    lines = cleaned_text.split('\n')
    
    # Attempt to extract values after a colon, if present
    values = []
    for line in lines:
        if ':' in line:
            # Take the part after the colon
            value = line.split(':', 1)[1].strip()
            values.append(value)
        else:
            # Assume the line itself is the value
            values.append(line.strip())
            
    # Join the cleaned values with a comma
    return ", ".join(values)

def process_tab(tab_name, stop_event):
    """
    Processes a single sheet tab to extract and update PII values row by row.
    """
    print(f"[*] Starting processing for tab: {tab_name}")
    try:
        rows = get_all_rows(tab_name)
        if not rows:
            print(f"[*] No data found in tab: {tab_name}. Exiting thread.")
            return

        header = rows[0]
        pii_value_col_index = -1
        try:
            pii_value_col_index = header.index("PII Value")
        except ValueError:
            print(f"[*] 'PII Value' column not found in '{tab_name}'. Adding it now.")
            header.append("PII Value")
            update_rows(tab_name, "A1", [header])
            rows = get_all_rows(tab_name)
            header = rows[0]
            pii_value_col_index = len(header) - 1

        pii_value_col_letter = col_to_letter(pii_value_col_index)
        if not pii_value_col_letter:
            print(f"[!] Could not determine column letter for 'PII Value' in '{tab_name}'.")
            return

        for i, row in enumerate(rows[1:]):
            if stop_event.is_set():
                print(f"[*] Stop signal received in '{tab_name}'. Exiting thread.")
                return
                
            row_index = i + 2
            if len(row) > 1 and row[1].strip().lower() == 'yes':
                if len(row) > pii_value_col_index and row[pii_value_col_index]:
                    continue

                original_text = row[0]
                pii_identifiers = row[3]

                if original_text and pii_identifiers:
                    print(f"  -> Processing row {row_index} in '{tab_name}'...")
                    prompt = (
                        f"From the text below, extract the values for the following PII identifiers: {pii_identifiers}.\n\n"
                        f"Text: \"{original_text}\"\n\n"
                        "IMPORTANT: Your response must be a single line of text containing only the extracted values, separated by commas, in the exact same order as the identifiers. Do not include the identifier keys, markdown, or any other formatting."
                    )
                    raw_pii_values = fetch_rows(prompt)
                    cleaned_pii_values = clean_pii_values(raw_pii_values)
                    
                    update_range = f"{pii_value_col_letter}{row_index}"
                    update_rows(tab_name, update_range, [[cleaned_pii_values]])
                    print(f"  <- Updated row {row_index} in '{tab_name}' with values: {cleaned_pii_values}")
                    
                    time.sleep(1) 
        
        print(f"[*] Finished processing for tab: {tab_name}")

    except Exception as e:
        print(f"[!] An error occurred in thread for tab '{tab_name}': {e}")


def run(stop_event):
    """
    Extracts PII values by processing each sheet tab in a separate thread.
    """
    print("🔄 Starting PII value extraction process in parallel... Press Ctrl+C to stop.")
    
    threads = []
    for tab in settings.SHEET_TABS:
        thread = threading.Thread(target=process_tab, args=(tab, stop_event))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
        
    if not stop_event.is_set():
        print("\n✅ All tabs processed. PII value extraction process completed.")
