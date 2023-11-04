from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Identity, event, func, insert
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, execute

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("recruiters.user_id"))
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    owner: Mapped["Recruiter"] = relationship(back_populates="companies", lazy="selectin")

    def __repr__(self):
        return f"company ({self.id}) {self.name} {self.description}"