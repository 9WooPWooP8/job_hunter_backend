from datetime import datetime
from typing import Any

from fastapi import Cookie, Depends

from src.auth import jwt
from src.auth import service as auth_service
from src.auth.exceptions import RefreshTokenNotValid
from src.auth.schemas import JWTClaims
from src.users import service as user_service


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> dict[str, Any]:
    db_refresh_token = await auth_service.get_refresh_token(refresh_token)

    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> dict[str, Any]:
    user = await user_service.get_user_by_id(refresh_token["user_id"])

    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: dict[str, Any]) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]


async def user_is_authenticated(
    jwt_claims: JWTClaims = Depends(jwt.parse_jwt_user_data),
) -> dict[str, any]:
    user = await user_service.get_user_by_id(jwt_claims.user_id)

    return user
