from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.config import auth_config
from src.auth.schemas import JWTData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

DEFAULT_ACCESS_TOKEN_LIFETIME = timedelta(minutes=auth_config.JWT_EXP)


def create_access_token(
    user: dict[str, Any], expires_delta: timedelta = DEFAULT_ACCESS_TOKEN_LIFETIME
):
    jwt_claims = {"sub": str(user["id"]), "exp": datetime.utcnow() + expires_delta}

    encoded_jwt = jwt.encode(
        jwt_claims, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG
    )

    return encoded_jwt


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )
    except JWTError:
        raise ValueError()  # TODO: Change to invalid token exception

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise ValueError()  # TODO: Change to auth required exception

    return token
