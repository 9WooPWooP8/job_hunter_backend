from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Identity, event, func, insert
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, execute

class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("recruiters.user_id"))
    status_id: Mapped[int]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    company: Mapped["Company"] = relationship(back_populates="vacancies", lazy="selectin")

    def __repr__(self):
        return f"vacancy ({self.id}) {self.description}"