from pydantic import BaseModel, Field
from typing import Optional, Annotated
from pydantic import StringConstraints


Phone = Annotated[str, StringConstraints(pattern=r"^\+\d+$")]
Timestamp = Annotated[str, StringConstraints(pattern=r"^\d{4}-\d{2}-\d{2}T.*Z$")]


class MessageIn(BaseModel):
    message_id: str
    from_: Phone = Field(..., alias="from")
    to: Phone
    ts: Timestamp
    text: Optional[str] = Field(default=None, max_length=4096)
