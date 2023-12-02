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
            job_title=resume.job_title,
            description=resume.description,
            applicant_id=resume.applicant_id
        )

        for record in resume.employment_records:
            new_record = EmploymentRecord(
                start_date=record.start_date,
                end_date=record.end_date,
                organization=record.organization,
                position=record.position,
                still_working=record.still_working
            )
            db_resume.employment_records.append(new_record)

        for quality in resume.personal_qualities:
            select_query = select(PersonalQuality).where(quality == PersonalQuality.id)
            one_query = await fetch_one(self.db, select_query)
            db_resume.personal_qualities.append(one_query)

        for education in resume.education:
            new_education = ResumeEducation(
                education_id=education.education_id,
                end_year=education.end_year
            )
            db_resume.educations.append(new_education)

        self.db.add(db_resume)
        await self.db.commit()

        await self.db.refresh(db_resume)

        return db_resume

    async def update_resume(self, resume_id: int, updated_resume: ResumeRequest) -> Resume:
        db_resume = await self.get_by_id(resume_id)

        db_resume.job_title = updated_resume.job_title
        db_resume.applicant_id = updated_resume.applicant_id
        db_resume.description = updated_resume.description

        for record in updated_resume.employment_records:
            existing_employment_records = list(filter(lambda x: x.id == record.id, db_resume.employment_records))
            if existing_employment_records:
                current_employment_record = existing_employment_records[0]
                current_employment_record.start_date = record.start_date
                current_employment_record.end_date = record.end_date
                current_employment_record.organization = record.organization
                current_employment_record.position = record.position ###
                current_employment_record.still_working = record.still_working
            else:
                new_record = EmploymentRecord(
                    start_date=record.start_date,
                    end_date=record.end_date,
                    organization=record.organization,
                    position=record.position,
                    still_working=record.still_working
                )
                db_resume.employment_records.append(new_record)
        deleted_employment_records = []
        for record in db_resume.employment_records:
            deleted_employment_record = list(filter(lambda x: x.id == record.id, updated_resume.employment_records))
            if not deleted_employment_record:
                deleted_employment_records.append(record)
                await self.db.delete(record)
        for delete_record in deleted_employment_records:
            db_resume.employment_records.remove(delete_record)


        for contact in updated_resume.contacts:
            existing_contacts = list(filter(lambda x: x.contact_id == contact.contact_id, db_resume.contacts))
            if existing_contacts:
                current_contact = existing_contacts[0]
                current_contact.extra_data = contact.extra_data
                current_contact.contact_id = contact.contact_id
            else:
                new_contact = ResumeContact(
                    extra_data=contact.extra_data,
                    contact_id=contact.contact_id
                )
                db_resume.contacts.append(new_contact)
        deleted_contacts = []
        for contact in db_resume.contacts:
            deleted_contact = list(filter(lambda x: x.contact_id == contact.contact_id, updated_resume.contacts))
            if not deleted_contact:
                deleted_contacts.append(contact)
                await self.db.delete(contact)
        for delete_contact in deleted_contacts:
            db_resume.contacts.remove(delete_contact)


        for personal_quality in updated_resume.personal_qualities:
            existing_quality = list(filter(lambda x: x.id == personal_quality, db_resume.personal_qualities))
            if not existing_quality:
                xuy = select(PersonalQuality).where(PersonalQuality.id == personal_quality)
                penis = await fetch_one(self.db, xuy)
                db_resume.personal_qualities.append(penis)
        deleted_qualities = []
        for quality in db_resume.personal_qualities:
            deleted_quality1 = list(filter(lambda x: x == quality.id, updated_resume.personal_qualities))
            if not deleted_quality1:
                deleted_qualities.append(quality)
        for deleted_quality in deleted_qualities:
            db_resume.personal_qualities.remove(deleted_quality)


        for education in updated_resume.education:
            existing_education = list(filter(lambda x: x.education_id == education.education_id, db_resume.educations))
            if existing_education:
                current_education = existing_education[0]
                current_education.education_id = education.education_id
                current_education.end_year = education.end_year

            else:
                new_education = ResumeEducation(
                    education_id=education.education_id,
                    end_year=education.end_year
                )
                db_resume.educations.append(new_education)
        deleted_educations = []
        for education in db_resume.educations:
            deleted_education = list(filter(lambda x: x.education_id == education.education_id, updated_resume.education))
            if not deleted_education:
                deleted_educations.append(education)
                await self.db.delete(education)
        for delete_education in deleted_educations:
            db_resume.educations.remove(delete_education)

        await self.db.commit()
        return await self.get_by_id(db_resume.id)

    async def get_by_id(self, id) -> Resume | None:
        select_query = select(Resume).where(Resume.id == id)
        return await fetch_one(self.db, select_query)

    async def delete_resume(self, id) -> None:
        stmt = await self.get_by_id(id);
        await self.db.delete(stmt)
        await self.db.commit()

    async def get_all(self) -> list[Resume] | None:
        select_query = select(Resume)

        return await fetch_all(self.db, select_query)


def get_resume_service(
        db: Annotated[AsyncSession, Depends(get_db)],
):
    return ResumeService(db)
