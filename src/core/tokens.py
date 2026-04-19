import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jose import jwt

from .settings import get_settings

settings = get_settings


class TokenHelper:
    def generate_session_token(self) -> tuple[str, str]:
        token = secrets.token_urlsafe(32)
        return token, self.hash_session_token(token)

    def hash_session_token(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create_access_token(self, user_id: int) -> str:
        return self._create_token(
            user_id, "access", settings.access_token_expires_minutes
        )

    def create_refresh_token(self) -> str:
        return secrets.token_urlsafe(48)

    def decode_token(self, token: str, expected_type: str) -> dict:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        if payload.get("type") != expected_type:
            raise jwt.InvalidTokenError("Invalid token type")
        return payload

    def _create_token(self, user_id: int, token_type: str, expires_minutes: int) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "type": token_type,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
            "iss": settings.app_name,
        }
        return jwt.encode(
            payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )


tokens = TokenHelper()
