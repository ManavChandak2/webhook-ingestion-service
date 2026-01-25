import hmac
import hashlib
from app.core.config import settings


def verify_signature(raw_body: bytes, signature: str) -> bool:
    secret = settings.WEBHOOK_SECRET.encode()
    computed = hmac.new(secret, raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, signature)
