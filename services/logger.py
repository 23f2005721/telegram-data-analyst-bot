"""
services/logger.py

JSONL Logger for the Telegram Data Analyst Bot.

Each line in run.jsonl is a valid JSON object.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from config import Config


class Logger:
    """
    Handles logging agent execution to a JSONL file.
    """

    def __init__(self):
        self.log_file = Path(Config.LOG_FILE)

        # Create logs directory if it doesn't exist
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def clear(self):
        """
        Start a new log for every request.
        """
        self.log_file.write_text("", encoding="utf-8")

    def log(self, step: str, **data):
        """
        Append a single JSON object to the log.

        Example:
            logger.log(
                "message_received",
                message="Hello"
            )
        """

        record = {
            "id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step,
            "data": data
        }

        with self.log_file.open(
            "a",
            encoding="utf-8"
        ) as file:
            json.dump(
                record,
                file,
                ensure_ascii=False
            )
            file.write("\n")

    def read(self):
        """
        Read the log file.

        Returns:
            list[dict]
        """

        if not self.log_file.exists():
            return []

        logs = []

        with self.log_file.open(
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return logs

    def exists(self):
        """
        Returns True if log file exists.
        """
        return self.log_file.exists()

    def get_path(self):
        """
        Returns the absolute path of the log file.
        """
        return str(self.log_file.resolve())

    def get_filename(self):
        """
        Returns only the filename.
        """
        return self.log_file.name

    def delete(self):
        """
        Delete the log file.
        """

        if self.exists():
            self.log_file.unlink()

    def size(self):
        """
        Returns log file size in bytes.
        """

        if not self.exists():
            return 0

        return self.log_file.stat().st_size

    def log_exception(self, exception: Exception):
        """
        Convenience method for logging exceptions.
        """

        self.log(
            "exception",
            error=str(exception),
            exception_type=type(exception).__name__
        )

    def log_request(self, message: str, chat_id: int):
        """
        Log incoming Telegram message.
        """

        self.log(
            "request_received",
            chat_id=chat_id,
            message=message
        )

    def log_response(self, response):
        """
        Log outgoing response.
        """

        self.log(
            "response_sent",
            response=response
        )


# Singleton logger
logger = Logger()
