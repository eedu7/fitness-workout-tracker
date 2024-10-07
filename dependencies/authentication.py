from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from utils.jwt_handler import decode_token


class AuthenticationRequired:
    """
    A class to handle authentication using bearer tokens.
    If the token is missing or invalid, a 401 Unauthorized error is raised.
    """

    def __init__(
        self,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=True)),
    ):
        """
        Initializes the authentication dependency by checking the provided token.

        Args:
            token (HTTPAuthorizationCredentials): Bearer token from the Authorization header.

        Raises:
            HTTPException: If the token is missing or invalid.
        """
        self.token = token.credentials
        try:
            self.user_payload = decode_token(self.token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
            )
