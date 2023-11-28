from datetime import datetime

from sqlalchemy import ForeignKey, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.vacancies.models import Vacancy

from src.database import Base


class RequiredExperience(Base):
    __tablename__ = "required_experience"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str]

    vacancies: Mapped[list[Vacancy]] = relationship(back_populates="experience")


    def __repr__(self):
        return f"experience ({self.id}) {self.name}"
