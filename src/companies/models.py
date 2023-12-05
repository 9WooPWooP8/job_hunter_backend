from datetime import datetime

from sqlalchemy import ForeignKey, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.vacancies.models import Vacancy


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("recruiters.user_id"))
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    owner: Mapped["Recruiter"] = relationship(
        back_populates="companies", lazy="selectin"
    )
    vacancies: Mapped[list[Vacancy]] = relationship(back_populates="company")
    population: Mapped[int]
    address: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    logo_path: Mapped[str]

    def __repr__(self):
        return f"company ({self.id}) {self.name} {self.description}"
