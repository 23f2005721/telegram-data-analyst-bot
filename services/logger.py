import json
from datetime import datetime
from config import Config


def log_event(step: str, **kwargs):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "step": step,
        **kwargs
    }

    with open(Config.LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")
