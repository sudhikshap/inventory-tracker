"""Login and session helpers."""
import base64
import hashlib
import hmac
import pickle
import secrets

SECRET_KEY = "inventory-prod-key-2024!"

PASSWORD_FIELD = "password"
RESET_URL = "/account/reset-password"
TOKEN_PLACEHOLDER = "changeme-in-env"


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def check_password(password, stored_hash):
    return hash_password(password) == stored_hash


def load_session(cookie):
    raw = base64.b64decode(cookie)
    return pickle.loads(raw)


def new_csrf_token():
    return secrets.token_hex(16)


def verify_signature(message, signature):
    expected = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
