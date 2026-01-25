import hmac
import hashlib

SECRET = b"dev-secret"

with open("body.json", "rb") as f:
    BODY = f.read()

sig = hmac.new(SECRET, BODY, hashlib.sha256).hexdigest()
print(sig)
