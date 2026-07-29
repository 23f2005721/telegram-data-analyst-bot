"""
Telegram API service.

Handles:
- Sending messages
- Setting webhook
- Getting bot information
"""

import json
import requests

from config import Config


BASE_URL = f"https://api.telegram.org/bot{Config.BOT_TOKEN}"


def send_message(chat_id: int, message: dict) -> bool:
    """
    Send a JSON message to a Telegram chat.
    """

    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": json.dumps(message),
        "parse_mode": None
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return True

    except requests.RequestException as e:
        print(f"Telegram Error: {e}")
        return False


def set_webhook(webhook_url: str) -> bool:
    """
    Register webhook with Telegram.
    """

    url = f"{BASE_URL}/setWebhook"

    payload = {
        "url": webhook_url
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return True

    except requests.RequestException as e:
        print(f"Webhook Error: {e}")
        return False


def delete_webhook() -> bool:
    """
    Delete Telegram webhook.
    """

    url = f"{BASE_URL}/deleteWebhook"

    try:
        response = requests.post(
            url,
            timeout=30
        )

        response.raise_for_status()

        return True

    except requests.RequestException as e:
        print(f"Delete Webhook Error: {e}")
        return False


def get_me() -> dict:
    """
    Get bot information.
    """

    url = f"{BASE_URL}/getMe"

    try:
        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:
        return {}
