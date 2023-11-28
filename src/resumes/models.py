from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Identity, event, func, insert
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, execute

from src.users.models import Applicant

resume_personal_quality = Table(
    "resume_personal_quality", Base.metadata,
    Column("resume_id", Integer, ForeignKey("resumes.id"), primary_key=True),
    Column("personal_quality_id", Integer, ForeignKey("personal_qualities.id"), primary_key=True)
)

class Resume(Base):
    __tablename__ = 'resumes'

    id: Mapped[int] = mapped_column(primary_key=True)
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.user_id"))
    photo: Mapped[str | None]
    job_title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    contacts: Mapped[list["ResumeContact"]] = relationship(
        back_populates="resume")

    applicant: Mapped[list["Applicant"]] = relationship(
        back_populates="resumes")

    employment_records: Mapped[list["EmploymentRecord"]] = relationship(
        back_populates="resume")

    personal_qualities: Mapped[list["PersonalQuality"]] = relationship(
        secondary=resume_personal_quality,
        back_populates="resumes")

    educations: Mapped[list["ResumeEducation"]] = relationship(
        back_populates="resume")

class PersonalQuality(Base):
    __tablename__ = "personal_qualities"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]

    resumes: Mapped[list["Resume"]] = relationship(
        secondary=resume_personal_quality,
        back_populates="personal_qualities"
    )

# organisation string
class EmploymentRecord(Base):
    __tablename__ = "employment_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    organization: Mapped[str]
    position: Mapped[str]
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    still_working: Mapped[bool]

    resume: Mapped["Resume"] = relationship(
        back_populates="employment_records"
    )

class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]

    resumes: Mapped[list["ResumeEducation"]] = relationship(
        back_populates="education")

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    contact: Mapped[str]

    resumes: Mapped[list["ResumeContact"]] = relationship(
        back_populates="contact")

class ResumeContact(Base):
    __tablename__ = "resume_contact"
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), primary_key=True)
    contact_id: Mapped[int] = mapped_column(
        ForeignKey("contacts.id"), primary_key=True
    )
    extra_data: Mapped[str]
    contact: Mapped["Contact"] = relationship(back_populates="resumes")
    resume: Mapped["Resume"] = relationship(back_populates="contacts")

class ResumeEducation(Base):
    __tablename__ = "resume_education"
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), primary_key=True)
    education_id: Mapped[int] = mapped_column(
        ForeignKey("educations.id"), primary_key=True
    )
    education: Mapped["Education"] = relationship(back_populates="resumes")
    resume: Mapped["Resume"] = relationship(back_populates="educations")
    end_year: Mapped[int]

@event.listens_for(Contact.__table__, "after_create")
async def insert_initial_contacts(*args, **kwargs):
    default_contacts = ["phone", "telegram", "email"]

    for contact in default_contacts:
        insert_query = insert(Contact).values({"contact": contact})

        await execute(insert_query)

@event.listens_for(PersonalQuality.__table__, "after_create")
async def insert_initial_personal_qualities(*args, **kwargs):
    default_qualities = ["python", "1c", "ABAP"]

    for quality in default_qualities:
        insert_query = insert(PersonalQuality).values({"description": quality})

        await execute(insert_query)

@event.listens_for(Education.__table__, "after_create")
async def insert_initial_personal_educations(*args, **kwargs):
    default_qualities = ["Полное высшее", "Среднее полное", "Неполное среднее"]

    for quality in default_qualities:
        insert_query = insert(Education).values({"type": quality})

        await execute(insert_query)