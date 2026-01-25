from fastapi import APIRouter
from app.db.repository import get_stats

router = APIRouter()


@router.get("/stats")
def stats():
    return get_stats()
