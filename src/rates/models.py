from datetime import datetime

from sqlalchemy import ForeignKey, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.vacancies.models import Vacancy
from src.database import Base


class Rate(Base):
    __tablename__ = "rates"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str]

    vacancies: Mapped[list[Vacancy]] = relationship(back_populates="rate")


    def __repr__(self):
        return f"rate ({self.id}) {self.name}"
