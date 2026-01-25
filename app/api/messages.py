from fastapi import APIRouter, Query
from app.db.repository import get_messages

router = APIRouter()


@router.get("/messages")
def list_messages(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_filter: str | None = Query(None, alias="from"),
    since: str | None = None,
    q: str | None = None,
):
    data, total = get_messages(limit, offset, from_filter, since, q)

    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
