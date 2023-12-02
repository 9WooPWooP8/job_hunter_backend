from datetime import datetime

from sqlalchemy import ForeignKey, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    status_id: Mapped[int]
    description: Mapped[str]
    plug: Mapped[str]
    experience_min: Mapped[int]
    experience_max: Mapped[int]
    salary_min: Mapped[int]
    salary_max: Mapped[int]
    rate_id: Mapped[int] = mapped_column(ForeignKey("rates.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    company: Mapped["Company"] = relationship(
        back_populates="vacancies", lazy="selectin"
    )
    rate: Mapped["Rate"] = relationship(
        back_populates="vacancies", lazy="selectin"
    )        


    def __repr__(self):
        return f"vacancy ({self.id}) {self.description}"
