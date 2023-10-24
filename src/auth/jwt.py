from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.config import auth_config
from src.auth.exceptions import AuthRequired, InvalidToken
from src.auth.schemas import JWTClaims
from src.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/tokens/", auto_error=False)

DEFAULT_ACCESS_TOKEN_LIFETIME = timedelta(minutes=auth_config.JWT_EXP)


def create_access_token(
    user: User,
    expires_delta: timedelta = DEFAULT_ACCESS_TOKEN_LIFETIME,
):
    jwt_claims = {"sub": str(user.id), "exp": datetime.utcnow() + expires_delta}

    encoded_jwt = jwt.encode(
        jwt_claims, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG
    )

    return encoded_jwt


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTClaims | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )
    except JWTError:
        raise InvalidToken()

    return JWTClaims(**payload)


async def parse_jwt_user_data(
    token: JWTClaims | None = Depends(parse_jwt_user_data_optional),
) -> JWTClaims:
    if not token:
        raise AuthRequired()

    return token


def parse_jwt_access_token(token: str = None) -> JWTClaims | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )
    except JWTError:
        return None

    return JWTClaims(**payload)
