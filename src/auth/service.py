from datetime import datetime, timedelta
from typing import Any

from passlib.context import CryptContext
from sqlalchemy import insert, select, update

from src import utils
from src.auth.config import auth_config
from src.auth.models import AuthRefreshToken
from src.database import execute, fetch_one
from src.users.service import get_user_by_username

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> dict | bool:
    user = await get_user_by_username(username)
    if not user:
        return False

    if not verify_password(password, user["password"]):
        return False

    return user


async def create_refresh_token(
    *, user_id: int, refresh_token: str | None = None
) -> str:
    if not refresh_token:
        refresh_token = utils.generate_random_alphanum(64)

    insert_query = insert(AuthRefreshToken).values(
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        user_id=user_id,
    )
    await execute(insert_query)

    return refresh_token


async def expire_refresh_token(refresh_token_id: int) -> None:
    update_query = (
        update(AuthRefreshToken)
        .values(expires_at=datetime.utcnow() - timedelta(days=1))
        .where(AuthRefreshToken.id == refresh_token_id)
    )

    await execute(update_query)


async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
    select_query = select(AuthRefreshToken).where(
        AuthRefreshToken.refresh_token == refresh_token
    )

    return await fetch_one(select_query)
