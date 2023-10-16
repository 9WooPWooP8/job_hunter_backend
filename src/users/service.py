from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.auth import service as auth_service
from src.database import execute, fetch_one, get_db
from src.users.models import Applicant, Recruiter, User
from src.users.schemas import (
    ApplicantCreate,
    RecruiterCreate,
    RecruiterUpdate,
    UserCreate,
)


class UserService:
    db: Session

    def __init__(self, db: Annotated[Session, Depends(get_db)]):
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
            password=auth_service.get_password_hash(user.password),
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

        applicant = Applicant(user_id=base_user.id, status_id=applicant.status_id)

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
        self, recruiter_id: int, recruiter: RecruiterUpdate
    ) -> Recruiter:
        insert_query = (
            update(User)
            .values(
                {"first_name": recruiter.first_name, "last_name": recruiter.last_name}
            )
            .where(User.id == recruiter_id)
        )

        await execute(insert_query)

        fetch_result = (
            select(Recruiter, User)
            .join(User, full=True)
            .filter(Recruiter.user_id == recruiter_id)
        )

        recruiter = await fetch_one(fetch_result)

        return recruiter
