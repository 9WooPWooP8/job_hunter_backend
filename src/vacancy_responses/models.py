from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.resumes.models import Resume
from src.vacancies.models import Vacancy


class VacancyResponseStatus(Base):
    __tablename__ = "vacancy_response_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class VacancyResponse(Base):
    __tablename__ = "vacancy_responses"

    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id"), primary_key=True
    )
    status_id: Mapped[int] = mapped_column(ForeignKey("vacancy_response_statuses.id"))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    vacancy: Mapped[Vacancy] = relationship(back_populates="responses", lazy="selectin")
    resume: Mapped[Resume] = relationship(back_populates="responses", lazy="selectin")
    status: Mapped[VacancyResponseStatus] = relationship(lazy="joined")

    def __repr__(self):
        return f"vacancy_response ({self.resume_id} {self.vacancy_id})"
