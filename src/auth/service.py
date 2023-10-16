from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from src import utils
from src.auth.config import auth_config
from src.auth.models import AuthRefreshToken
from src.database import fetch_one, get_db
from src.users import service as user_service
from src.users.models import Applicant, Recruiter, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    db: Session

    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str) -> User | bool:
        user = await user_service.get_user_by_username(username)
        if not user:
            return False

        if not self.verify_password(password, user.password):
            return False

        return user

    async def authenticate_applicant(
        self, username: str, password: str
    ) -> Applicant | bool:
        user = await self.authenticate_user(username, password)

        if not user:
            return False

        applicant = await user_service.get_applicant_by_id(user.id)

        if not applicant:
            return False

        return user

    async def authenticate_recruiter(
        self, username: str, password: str
    ) -> Recruiter | bool:
        user = await self.authenticate_user(username, password)

        if not user:
            return False

        recruiter = await user_service.get_recruiter_by_id(user.id)

        if not recruiter:
            return False

        return user

    async def create_refresh_token(
        self, *, user_id: int, refresh_token: str | None = None
    ) -> str:
        if not refresh_token:
            refresh_token = utils.generate_random_alphanum(64)

        new_refresh_token = AuthRefreshToken(
            refresh_token=refresh_token,
            expires_at=datetime.utcnow()
            + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
            user_id=user_id,
        )
        self.db.add(new_refresh_token)
        await self.db.commit()

        self.db.refresh(new_refresh_token)

        return new_refresh_token.refresh_token

    async def expire_refresh_token(self, refresh_token_id: int) -> None:
        select_query = select(AuthRefreshToken).where(
            AuthRefreshToken.id == refresh_token_id
        )

        refresh_token = await fetch_one(self.db, select_query)

        refresh_token.expires_at = datetime.utcnow() - timedelta(days=1)

        await self.db.commit()

    async def get_refresh_token(self, refresh_token: str) -> AuthRefreshToken | None:
        select_query = select(AuthRefreshToken).where(
            AuthRefreshToken.refresh_token == refresh_token
        )

        return await fetch_one(self.db, select_query)
