from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from bot.handler import handle_update

app = FastAPI(
    title="Telegram Data Analyst Bot",
    version="1.0.0"
)


@app.get("/")
async def root():
    """
    Health check endpoint.
    """
    return {
        "status": "running",
        "service": "telegram-data-analyst-bot"
    }


@app.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Receives updates from Telegram and passes them to the bot handler.
    """
    try:
        update = await request.json()
        await handle_update(update)

        return JSONResponse(
            status_code=200,
            content={"ok": True}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
