import json
import os
from datetime import datetime

MOOD_FILE = "data/mood_log.json"
os.makedirs("data", exist_ok=True)

def log_mood(mood):
    try:
        if os.path.exists(MOOD_FILE):
            with open(MOOD_FILE, "r") as f:
                mood_log = json.load(f)
        else:
            mood_log = []

        mood_entry = {
            "mood": mood,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        mood_log.append(mood_entry)
        with open(MOOD_FILE, "w") as f:
            json.dump(mood_log, f, indent=4)

        if mood == "joy":
            return "✅ Recorded: Joy - You’re glowing with happiness!"
        elif mood == "sadness":
            return "✅ Recorded: Sadness - I’m here to lift you up."
        else:
            return f"✅ Recorded: {mood.capitalize()} - Thanks for sharing how you feel!"
    except Exception as e:
        return f"❌ ERROR: Failed to log mood - {e}"

def get_mood_log():
    try:
        if os.path.exists(MOOD_FILE):
            with open(MOOD_FILE, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        return [{"error": str(e)}]
