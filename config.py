import os
from dotenv import load_dotenv

# Load variables from .env (ignored on Render if environment variables are set)
load_dotenv()


class Config:
    # Telegram
    BOT_TOKEN = os.getenv("8725034188:AAE2RBuSn2PsDAoz7blzZNF20Xk7ml9QZjc")

    # LLM API
    GEMINI_API_KEY = os.getenv("AQ.Ab8RN6JtouKoI9UkjJwp1cLWS93zsgZ0bdFI7MNFRlKSi00KsQ")

    # Public URL of your deployed app
    APP_URL = os.getenv("APP_URL")

    # Base URL where run.jsonl will be publicly accessible
    LOG_BASE_URL = os.getenv("LOG_BASE_URL")

    # Environment
    ENV = os.getenv("ENV", "development")

    # Logging
    LOG_FILE = os.getenv("LOG_FILE", "logs/run.jsonl")

    @classmethod
    def validate(cls):
        """
        Validate required configuration values.
        Raises an error if something important is missing.
        """
        required = {
            "BOT_TOKEN": cls.BOT_TOKEN,
            "GEMINI_API_KEY": cls.GEMINI_API_KEY,
            "APP_URL": cls.APP_URL,
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
