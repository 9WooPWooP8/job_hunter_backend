from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Identity, event, func, insert
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, execute


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
    applicant_account: Mapped[Optional["Applicant"]] = relationship(
        back_populates="user"
    )
    recruiter_account: Mapped[Optional["Recruiter"]] = relationship(
        back_populates="user"
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

    def __repr__(self):
        return f"users({self.id}) {self.first_name} {self.last_name}"


class Applicant(Base):
    __tablename__ = "applicants"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user: Mapped["User"] = relationship(
        back_populates="applicant_account", lazy="selectin"
    )
    status_id: Mapped[int] = mapped_column(ForeignKey("applicant_statuses.id"))
    status: Mapped["ApplicantStatus"] = relationship()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

    def __repr__(self):
        return f"applicants({self.user_id})"


class Recruiter(Base):
    __mapper_args__ = {"eager_defaults": True}
    __tablename__ = "recruiters"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user: Mapped["User"] = relationship(
        back_populates="recruiter_account", lazy="selectin"
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())
    companies: Mapped[list["Company"]] = relationship(back_populates="owner")

    def __repr__(self):
        return f"recruiters({self.user_id})"


class ApplicantStatus(Base):
    __tablename__ = "applicant_statuses"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str]

    def __repr__(self):
        return f"applicant_statuses({self.id}) {self.name}"


# insert default values (probably bad)
@event.listens_for(ApplicantStatus.__table__, "after_create")
async def insert_initial_values(*args, **kwargs):
    default_statuses = ["looking for job", "accepting offers", "not looking for job"]

    for status in default_statuses:
        insert_query = insert(ApplicantStatus).values({"name": status})

        await execute(insert_query)
