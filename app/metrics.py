from prometheus_client import Counter, Histogram, generate_latest
from fastapi import APIRouter

REQUEST_COUNT = Counter("requests_total", "Total HTTP requests")
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency")

router = APIRouter()

@router.get("/metrics")
def metrics():
    return generate_latest()
