import uuid
import time
from fastapi import Request
from app.core.logger import logger


async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.time()

    response = await call_next(request)

    latency_ms = int((time.time() - start) * 1000)

    logger.info(
        "request",
        extra={
            "extra": {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "latency_ms": latency_ms,
            }
        },
    )

    response.headers["X-Request-ID"] = request_id
    return response
