from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.users.models import Applicant


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.user_id"))
    photo: Mapped[str | None]
    job_title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    contacts: Mapped[list["ResumeContact"]] = relationship(
        back_populates="resume", cascade="all, delete", lazy="joined"
    )

    applicant: Mapped["Applicant"] = relationship(
        back_populates="resumes", lazy="joined"
    )

    employment_records: Mapped[list["EmploymentRecord"]] = relationship(
        back_populates="resume", cascade="all, delete", lazy="joined"
    )

    personal_qualities: Mapped[str | None]

    educations: Mapped[list["ResumeEducation"]] = relationship(
        back_populates="resume", cascade="all, delete", lazy="joined"
    )
    responses: Mapped[list["VacancyResponse"]] = relationship(
        back_populates="resume", lazy="joined", cascade="all, delete"
    )

    status_id: Mapped[int] = mapped_column(ForeignKey("search_statuses.id"), primary_key=True)
    status: Mapped["SearchStatus"] = relationship(
        back_populates="resumes", lazy="selectin"
    )

class SearchStatus(Base):
    __tablename__ = "search_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    resumes: Mapped[list[Resume]] = relationship(
        back_populates="status", lazy="joined"
    )

class EmploymentRecord(Base):
    __tablename__ = "employment_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    organization: Mapped[str]
    position: Mapped[str]
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    still_working: Mapped[bool]

    resume: Mapped["Resume"] = relationship(back_populates="employment_records")


class Education(Base):
    __mapper_args__ = {"eager_defaults": True}
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]

    resumes: Mapped[list["ResumeEducation"]] = relationship(back_populates="education")


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    contact: Mapped[str]

    resumes: Mapped[list["ResumeContact"]] = relationship(back_populates="contact")


class ResumeContact(Base):
    __tablename__ = "resume_contact"
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), primary_key=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"), primary_key=True)
    extra_data: Mapped[str]
    contact: Mapped["Contact"] = relationship(back_populates="resumes")
    resume: Mapped["Resume"] = relationship(back_populates="contacts")


class ResumeEducation(Base):
    __tablename__ = "resume_education"
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), primary_key=True)
    education_id: Mapped[int] = mapped_column(
        ForeignKey("educations.id"), primary_key=True
    )
    education: Mapped["Education"] = relationship(
        back_populates="resumes", lazy="selectin"
    )
    resume: Mapped["Resume"] = relationship(back_populates="educations")
    end_year: Mapped[int]

