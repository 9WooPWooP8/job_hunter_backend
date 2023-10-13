from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Identity,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class AuthRefreshToken(Base):
    __tablename__ = "auth_refresh_tokens"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    refresh_token: Mapped[str]
    expires_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

    def __repr__(self):
        return f"({self.id} {self.refresh_token})"
