from fastapi import APIRouter, Request, Header, HTTPException
from app.schemas.message import MessageIn
from app.core.security import verify_signature
from app.db.repository import insert_message
from app.core.logger import logger


router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request, x_signature: str = Header(None)):
    raw_body = await request.body()

    if not x_signature or not verify_signature(raw_body, x_signature):
        logger.info("webhook_invalid_signature")
        raise HTTPException(status_code=401, detail="invalid signature")

    data = await request.json()
    msg = MessageIn(**data)

    inserted = insert_message(msg)

    logger.info(
        "webhook_processed",
        extra={
            "extra": {
                "message_id": msg.message_id,
                "from": msg.from_,
                "result": "created" if inserted else "duplicate",
            }
        },
    )

    return {"status": "ok"}
