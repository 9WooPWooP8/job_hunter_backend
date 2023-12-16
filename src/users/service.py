from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.passwords import get_password_hash
from src.database import fetch_all, fetch_one, get_db
from src.exceptions import NotAuthenticated
from src.users.models import Applicant, ApplicantStatus, Recruiter, User
from src.users.schemas import (
    ApplicantCreate,
    ApplicantUpdate,
    RecruiterCreate,
    RecruiterUpdate,
    UserCreate,
)


class UserService:
    db: AsyncSession

    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.db = db

    async def get_user_by_username(self, username: str) -> User | None:
        select_query = select(User).where(User.username == username)

        return await fetch_one(self.db, select_query)

    async def get_user_by_id(self, id: int) -> User | None:
        select_query = select(User).where(User.id == id)

        return await fetch_one(self.db, select_query)

    async def get_user_by_email(self, email: str) -> User | None:
        select_query = select(User).where(User.email == email)

        return await fetch_one(self.db, select_query)

    async def get_applicant_by_id(self, id: int) -> Applicant | None:
        select_query = select(Applicant).where(Applicant.user_id == id)

        return await fetch_one(self.db, select_query)

    async def get_recruiter_by_id(self, id: int) -> Recruiter | None:
        select_query = select(Recruiter).where(Recruiter.user_id == id)

        return await fetch_one(self.db, select_query)

    async def create_base_user(self, user: UserCreate) -> User:
        user = User(
            email=user.email,
            password=get_password_hash(user.password),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        self.db.add(user)
        await self.db.commit()

        await self.db.refresh(user)

        return user

    async def create_applicant(self, applicant: ApplicantCreate) -> Applicant:
        base_user = await self.get_user_by_email(applicant.email)

        if not base_user:
            base_user = await self.create_base_user(user=applicant)

        applicant = Applicant(user_id=base_user.id, status_id=applicant.status_id.value)

        self.db.add(applicant)
        await self.db.commit()

        await self.db.refresh(applicant)

        return applicant

    async def create_recruiter(self, recruiter: RecruiterCreate) -> Recruiter:
        base_user = await self.get_user_by_email(recruiter.email)

        if not base_user:
            base_user = await self.create_base_user(user=recruiter)

        recruiter = Recruiter(user_id=base_user.id)

        self.db.add(recruiter)
        await self.db.commit()

        await self.db.refresh(recruiter)

        return recruiter

    async def update_recruiter(
        self, recruiter_id: int, recruiter: RecruiterUpdate, user: Recruiter
    ) -> Recruiter:
        if recruiter_id != user.user_id:
            raise NotAuthenticated()

        recruiter_db = await self.get_recruiter_by_id(recruiter_id)

        recruiter_db.user.first_name = recruiter.first_name
        recruiter_db.user.last_name = recruiter.last_name

        await self.db.commit()

        return recruiter_db

    async def update_applicant(
        self, applicant_id: int, applicant: ApplicantUpdate, user: Applicant
    ) -> Applicant:
        if applicant_id != user.user_id:
            raise NotAuthenticated()

        applicant_db = await self.get_applicant_by_id(applicant_id)

        applicant_db.user.first_name = applicant.first_name
        applicant_db.user.last_name = applicant.last_name
        applicant_db.status_id = applicant.status_id.value

        await self.db.commit()

        return applicant_db

    async def get_all_status(self) -> list[ApplicantStatus] | None:
        select_query = select(ApplicantStatus)

        return await fetch_all(self.db, select_query)


# TODO:
def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return UserService(db)
