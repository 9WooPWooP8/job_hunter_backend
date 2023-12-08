from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.users.models import Applicant


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    text: Mapped[str]

    applicant_id: Mapped[int] = mapped_column(
        ForeignKey("applicants.user_id"), primary_key=True
    )

    applicant: Mapped["Applicant"] = relationship(back_populates="notifications")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
