from datetime import datetime
from typing import Annotated, Any

from fastapi import Cookie, Depends, HTTPException, status
from jose import JWTError, jwt

from src.auth import service as auth_service
from src.auth.constants import ALGORITHM, SECRET_KEY
from src.auth.jwt import oauth2_scheme
from src.auth.schemas import AuthData, TokenData
from src.users import service as user_service
from src.users.service import get_user_by_username

# TODO: change all exceptions to custom


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await get_user_by_username(username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def valid_user_create(user: AuthData) -> AuthData:
    if await user_service.get_user_by_email(user.username):
        raise Exception()

    return user


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> dict[str, Any]:
    db_refresh_token = await auth_service.get_refresh_token(refresh_token)

    if not db_refresh_token:
        raise Exception()

    if not _is_valid_refresh_token(db_refresh_token):
        raise Exception()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> dict[str, Any]:
    user = await user_service.get_user_by_id(refresh_token["user_id"])

    if not user:
        raise Exception()

    return user


def _is_valid_refresh_token(db_refresh_token: dict[str, Any]) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]
