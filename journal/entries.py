import os
import json
from datetime import datetime

JOURNAL_FILE = "data/journal_entries.json"
os.makedirs("data", exist_ok=True)

def save_entry(entry):
    try:
        if os.path.exists(JOURNAL_FILE):
            with open(JOURNAL_FILE, "r") as f:
                journal = json.load(f)
        else:
            journal = []

        new_entry = {
            "entry": entry,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        journal.append(new_entry)

        with open(JOURNAL_FILE, "w") as f:
            json.dump(journal, f, indent=4)

        return "✍️ Your thoughts are saved—safe and sound. What else is on your heart?"
    except Exception as e:
        return f"❌ ERROR: Failed to save journal entry - {e}"
