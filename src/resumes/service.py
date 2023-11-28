from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import fetch_one, fetch_all, get_db
from src.resumes.models import Resume, EmploymentRecord, Contact, ResumeContact, Education, PersonalQuality, \
    resume_personal_quality, ResumeEducation
from src.resumes.schemas import ResumeRequest, ResumeResponse


class ResumeService:
    db: AsyncSession

    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.db = db

    async def create_resume(self, resume: ResumeRequest) -> Resume:
        db_resume = Resume(
            job_title = resume.job_title,
            description = resume.description,
            applicant_id = resume.applicant_id
        )


        for record in resume.employment_records:
            new_record = EmploymentRecord(
                start_date = record.start_date,
                end_date = record.end_date,
                organization = record.organization,
                position = record.position,
                still_working = record.still_working
            )
            db_resume.employment_records.append(new_record)

        for quality in resume.personal_qualities:
            select_query = select(PersonalQuality).where(quality == PersonalQuality.id)
            one_query = await fetch_one(self.db, select_query)
            db_resume.personal_qualities.append(one_query)

        for education in resume.education:
            new_education = ResumeEducation(
                education_id = education.education_id,
                end_year = education.end_year
            )
            db_resume.educations.append(new_education)

        self.db.add(db_resume)
        await self.db.commit()

        await self.db.refresh(db_resume)

        return db_resume

    async def delete_resume(self, id) -> None:
        db_resume = self.get_by_id(id)
        self.db.delete(db_resume)
        await self.db.commit()

    async def get_by_id(self, id) -> Resume | None:
        select_query = select(Resume).where(Resume.id == id)

        return await fetch_one(self.db, select_query)

    async def get_all(self) -> list[Resume] | None:
        select_query = select(Resume)

        return await fetch_all(self.db, select_query)



def get_resume_service(
        db: Annotated[AsyncSession, Depends(get_db)],
):
    return ResumeService(db)