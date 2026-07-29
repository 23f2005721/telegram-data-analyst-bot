"""
bot/handler.py

Handles incoming Telegram updates.
"""

from bot.response import build_response
from services.logger import logger
from services.telegram_service import send_message
from services.storage import storage


async def handle_update(update: dict):
    """
    Process an incoming Telegram update.
    """

    try:
        # Ignore updates without a message
        if "message" not in update:
            return

        message = update["message"]

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        # Start a fresh log for this request
        logger.clear()

        # Log the incoming message
        logger.log_request(
            message=text,
            chat_id=chat_id
        )

        # ------------------------------------------------------------------
        # TODO:
        # Later we will:
        # 1. Save conversation memory
        # 2. Call Gemini
        # 3. Download datasets
        # 4. Analyze data
        # ------------------------------------------------------------------


        response = build_response(
            answer=answer,
            log_url=storage.get_public_log_url()
        )
        logger.log_response(response)

        send_message(
            chat_id=chat_id,
            message=response
        )

    except Exception as e:
        logger.log_exception(e)

        error_response = build_response(
            answer="Internal Server Error",
            log_url=""
        )

        try:
            send_message(
                chat_id=chat_id,
                message=error_response
            )
        except Exception:
            pass
