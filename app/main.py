from fastapi import FastAPI
from app.api.webhook import router as webhook_router
from app.api.messages import router as messages_router
from app.db.models import init_db
from app.core.config import settings
from app.api.stats import router as stats_router

app = FastAPI(title="Webhook Ingestion Service")

# Register routers
app.include_router(webhook_router)
app.include_router(messages_router)
app.include_router(stats_router)


@app.on_event("startup")
def startup_event():
    if not settings.WEBHOOK_SECRET:
        raise RuntimeError("WEBHOOK_SECRET is not set")
    init_db()


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    try:
        init_db()
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}
