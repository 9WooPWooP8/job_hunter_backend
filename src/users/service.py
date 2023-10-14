from typing import Any

from sqlalchemy import insert, select

from src.auth import service as auth_service
from src.database import fetch_one
from src.users.models import Applicant, Recruiter, User
from src.users.schemas import ApplicantCreate, RecruiterCreate, UserCreate


async def get_user_by_username(username: str) -> dict[str, Any] | None:
    select_query = select(User).where(User.username == username)

    return await fetch_one(select_query)


async def get_user_by_id(id: int) -> dict[str, Any] | None:
    select_query = select(User).where(User.id == id)

    return await fetch_one(select_query)


async def get_user_by_email(email: str) -> dict[str, Any] | None:
    select_query = select(User).where(User.email == email)

    return await fetch_one(select_query)


async def create_base_user(user: UserCreate) -> dict[str, Any] | None:
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


async def create_applicant(applicant: ApplicantCreate) -> dict[str, Any] | None:
    created_base_user = await create_base_user(user=applicant)

    insert_query = (
        insert(Applicant)
        .values(
            {"user_id": created_base_user["id"], "status_id": applicant.status_id.value}
        )
        .returning(Applicant.user_id)
    )

    applicant = await fetch_one(insert_query)

    return applicant


async def create_recruiter(recruiter: RecruiterCreate) -> dict[str, Any] | None:
    created_base_user = await create_base_user(user=recruiter)

    insert_query = (
        insert(Recruiter)
        .values({"user_id": created_base_user["id"]})
        .returning(Recruiter.user_id)
    )

    recruiter = await fetch_one(insert_query)

    return recruiter
