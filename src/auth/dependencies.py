from datetime import datetime
from typing import Annotated, Any

from fastapi import Cookie, Depends

import src.auth.service as auth_service
import src.users.service as user_service
from src.auth import jwt
from src.auth.exceptions import RefreshTokenNotValid
from src.auth.schemas import JWTClaims


async def valid_refresh_token(
    user_service: Annotated[
        auth_service.AuthService, Depends(auth_service.get_auth_service)
    ],
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> dict[str, Any]:
    db_refresh_token = await auth_service.get_refresh_token(refresh_token)

    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    user_service: Annotated[
        user_service.UserService, Depends(user_service.get_user_service)
    ],
    refresh_token: Annotated[dict[str, Any], Depends(valid_refresh_token)],
) -> dict[str, Any]:
    user = await user_service.get_user_by_id(refresh_token["user_id"])

    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: dict[str, Any]) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]


async def user_is_authenticated(
    user_service: Annotated[
        user_service.UserService, Depends(user_service.get_user_service)
    ],
    jwt_claims: Annotated[JWTClaims, Depends(jwt.parse_jwt_user_data)],
) -> dict[str, any]:
    user = await user_service.get_user_by_id(jwt_claims.user_id)

    return user
