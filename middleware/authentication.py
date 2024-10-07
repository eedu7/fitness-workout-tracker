from typing import Optional

from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import \
    AuthenticationMiddleware as BaseAuthenticationMiddleware
from starlette.requests import HTTPConnection

from schemas.user import CurrentUser
from utils.jwt_handler import decode_token


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self,
        conn: HTTPConnection,
    ) -> tuple[bool, Optional[CurrentUser]]:
        current_user: CurrentUser = CurrentUser()

        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, token = authorization.split(" ")
            if scheme.casefold() != "bearer":
                return False, current_user

        except ValueError:
            return False, current_user

        if not token:
            return False, current_user

        try:
            payload = decode_token(token)
            user_id = payload.get("user_id")
        except Exception:
            return False, current_user

        current_user.id = user_id
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
