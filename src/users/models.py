from datetime import datetime

from sqlalchemy import (
    Identity,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    email: Mapped[str]
    username: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str | None]
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(server_default="false")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

    def __repr__(self):
        return f"({self.id} {self.first_name} {self.last_name})"
