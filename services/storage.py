"""
services/storage.py

Provides access to the JSONL execution log.
"""

from pathlib import Path

from config import Config


class Storage:
    """
    Handles log file storage and public URL generation.
    """

    def __init__(self):
        self.log_file = Path(Config.LOG_FILE)

    def get_log_path(self) -> str:
        """
        Returns the local path of run.jsonl.
        """
        return str(self.log_file)

    def log_exists(self) -> bool:
        """
        Check whether the log file exists.
        """
        return self.log_file.exists()

    def get_log_filename(self) -> str:
        """
        Returns run.jsonl.
        """
        return self.log_file.name

    def get_public_log_url(self) -> str:
        """
        Returns the public URL of the log.

        During local development:
            http://localhost:8000/logs/run.jsonl

        On Render:
            https://your-app.onrender.com/logs/run.jsonl
        """

        if Config.APP_URL:
            return f"{Config.APP_URL.rstrip('/')}/logs/{self.get_log_filename()}"

        return ""


# Singleton
storage = Storage()
