import time
from typing import Any

from jose import JWTError, jwt

from config import config


def encode_token(payload: dict[str, Any]) -> str:
    """
    Encode a JWT token with the given payload and return the token along with the expiration time.
    """
    # Set expiration time by adding the JWT_EXP value to the current timestamp
    exp = int(time.time()) + config.JWT_EXP
    payload["exp"] = exp
    token = jwt.encode(
        payload,
        config.JWT_SECRET,
        algorithm=config.JWT_ALGORITHM,
    )
    return token


def decode_token(token: str) -> dict:
    """
    Decode the JWT token and return the payload.
    Raises an exception if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM],
        )
        return payload
    except JWTError as e:
        raise ValueError("Invalid or expired token") from e
