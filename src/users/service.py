from typing import Any

from sqlalchemy import insert, select

from src.auth import service as auth_service
from src.database import fetch_one
from src.users.models import User
from src.users.schemas import UserCreate


async def get_user_by_username(username: str) -> dict[str, Any] | None:
    select_query = select(User).where(User.username == username)

    return await fetch_one(select_query)


async def get_user_by_id(id: int) -> dict[str, Any] | None:
    select_query = select(User).where(User.id == id)

    return await fetch_one(select_query)


async def get_user_by_email(email: str) -> dict[str, Any] | None:
    select_query = select(User).where(User.email == email)

    return await fetch_one(select_query)


async def create_user(user: UserCreate) -> dict[str, Any] | None:
    insert_query = (
        insert(User)
        .values(
            {
                "email": user.email,
                "password": auth_service.get_password_hash(user.password),
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
        .returning(User)
    )

    return await fetch_one(insert_query)
