import json
import requests
from services.telegram_service import send_message

from config import Config


async def handle_update(update: dict):
    """
    Process incoming Telegram update.
    """

    try:
        # Ignore updates without a message
        if "message" not in update:
            return

        message = update["message"]

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        print(f"Received message: {text}")

        # Temporary response
        response = {
            "answer": "Bot is working!",
            "log_url": ""
        }

        send_message(chat_id, response)

    except Exception as e:
        print(f"Handler Error: {e}")


def send_message(chat_id: int, response: dict):
    """
    Send message back to Telegram.
    """

    url = f"https://api.telegram.org/bot{Config.BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": json.dumps(response)
    }

    requests.post(url, json=payload)
