from datetime import datetime
from datetime import timedelta
from uuid import UUID

import jwt

from src.settings import token_authorization
from src.exceptions.authentication import InvalidTokenException, TokenExpiredException


def encode_jwt_token(user_id: UUID) -> str:
    """
    Генерирует JWT токен

    Входящие параметры:
    :params user_id: uuid пользователя

    Исходящие параметры:
    JWT токен
    """

    try:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=token_authorization.token_ttl),
            "iat": datetime.now(),
            "sub": str(user_id),
        }

        return jwt.encode(
            payload, token_authorization.secret_key, algorithm=token_authorization.algorithms
        )
    except Exception as error:
        raise Exception(error)


def decode_jwt_token(token: bytes) -> tuple[bool, UUID]:
    """
    Декодирует JWT токен

    Входные параметры:
    :params token: токен

    Исходящие параметры:
    uuid пользователя
    """
    payload = None
    try:
        payload = jwt.decode(
            token,
            token_authorization.secret_key,
            algorithms=token_authorization.algorithms,
            options={"verify_signature": False},
        )
        
        if datetime.now() > datetime.fromtimestamp(payload["exp"]):
            return False, UUID(payload["sub"])

        return True, UUID(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException(status_code=400, message="Signature expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise InvalidTokenException(status_code=400, message="Invalid token. Please relogin")
