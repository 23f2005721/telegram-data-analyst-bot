"""
bot/handler.py

Handles incoming Telegram updates.
"""

from agent.agent import agent
from bot.response import build_response

from services.logger import logger
from services.storage import storage
from services.telegram_service import send_message


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
        text = message.get("text", "").strip()

        # Ignore empty messages
        if not text:
            return

        # ---------------------------------------------------------
        # Logging
        # ---------------------------------------------------------

        logger.clear()

        logger.log_request(
            message=text,
            chat_id=chat_id
        )

        # ---------------------------------------------------------
        # Agent
        # ---------------------------------------------------------

        logger.log(
            "agent_started"
        )

        answer = await agent.solve(text)

        logger.log(
            "agent_completed",
            answer=answer
        )

        # ---------------------------------------------------------
        # Build Final Response
        # ---------------------------------------------------------

        response = build_response(
            answer=answer,
            log_url=storage.get_public_log_url()
        )

        logger.log_response(response)

        # ---------------------------------------------------------
        # Send Reply
        # ---------------------------------------------------------

        send_message(
            chat_id=chat_id,
            message=response
        )

    except Exception as e:

        logger.log_exception(e)

        error_response = build_response(
            answer={
                "error": "Internal Server Error"
            },
            log_url=storage.get_public_log_url()
        )

        try:

            send_message(
                chat_id=chat_id,
                message=error_response
            )

        except Exception:

            pass
