"""
JSONL Logger for the Telegram Data Analyst Bot.

Each line in run.jsonl is a valid JSON object.
"""

import json
import os
from datetime import datetime
from uuid import uuid4

from config import Config


class Logger:
    def __init__(self):
        self.log_file = Config.LOG_FILE

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def clear(self):
        """
        Start a fresh log for every request.
        """
        with open(self.log_file, "w", encoding="utf-8"):
            pass

    def log(self, step: str, **data):
        """
        Append one JSON object to the log file.
        """

        record = {
            "id": str(uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "step": step,
            "data": data,
        }

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record))
            f.write("\n")


logger = Logger()
