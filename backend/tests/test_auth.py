from datetime import timedelta

from app.core.security import create_token, decode_token, hash_password, verify_password


def test_password_hash_roundtrip() -> None:
    hashed = hash_password("correct-horse-battery")
    assert verify_password("correct-horse-battery", hashed)
    assert not verify_password("wrong-password", hashed)


def test_jwt_roundtrip() -> None:
    token = create_token("7", "access", timedelta(minutes=15), "session-1")
    payload = decode_token(token)
    assert payload["sub"] == "7"
    assert payload["typ"] == "access"
