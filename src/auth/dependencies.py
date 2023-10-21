from datetime import datetime
from typing import Annotated

from fastapi import Cookie, Depends

import src.auth.service as auth_service
import src.users.service as user_service
from src.auth import jwt
from src.auth.exceptions import (
    ApplicantNotAuthenticated,
    RecruiterNotAuthenticated,
    RefreshTokenNotValid,
)
from src.auth.models import AuthRefreshToken
from src.auth.schemas import JWTClaims
from src.users.models import Applicant, Recruiter, User


def _is_valid_refresh_token(db_refresh_token: AuthRefreshToken) -> bool:
    return datetime.utcnow() <= db_refresh_token.expires_at


async def valid_refresh_token(
    auth_service: Annotated[
        auth_service.AuthService, Depends(auth_service.get_auth_service)
    ],
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> AuthRefreshToken:
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
    refresh_token: Annotated[AuthRefreshToken, Depends(valid_refresh_token)],
) -> User:
    user = await user_service.get_user_by_id(refresh_token.user_id)

    if not user:
        raise RefreshTokenNotValid()

    return user


async def recruiter_is_authenticated(
    user_service: Annotated[
        user_service.UserService, Depends(user_service.get_user_service)
    ],
    jwt_claims: Annotated[JWTClaims, Depends(jwt.parse_jwt_user_data)],
) -> Recruiter | None:
    user = await user_service.get_recruiter_by_id(jwt_claims.user_id)

    if not user:
        raise RecruiterNotAuthenticated

    return user


async def applicant_is_authenticated(
    user_service: Annotated[
        user_service.UserService, Depends(user_service.get_user_service)
    ],
    jwt_claims: Annotated[JWTClaims, Depends(jwt.parse_jwt_user_data)],
) -> Applicant | None:
    user = await user_service.get_applicant_by_id(jwt_claims.user_id)

    if not user:
        raise ApplicantNotAuthenticated

    return user
