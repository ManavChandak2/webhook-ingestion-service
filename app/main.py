from fastapi import FastAPI

app = FastAPI(title="WebHook Ingestion Service")
@app.get("/health/live")
def live():
    return {"status": "alive"}

@app.get("/health/ready")
def ready():
    return {"status": "ready"}
