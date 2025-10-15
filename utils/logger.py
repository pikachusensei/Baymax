# utils/logger.py
import json
from datetime import datetime

def log_conversation(user, reply, logfile="conversation_log.jsonl"):
    """
    Save user input + reply to a JSONL file.
    """
    record = {
        "time": datetime.now().isoformat(),
        "user": user,
        "baymax": reply
    }
    with open(logfile, "a") as f:
        f.write(json.dumps(record) + "\n")
