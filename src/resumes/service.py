from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Annotated

from fastapi import Depends, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import fetch_one, fetch_all, get_db
from src.resumes.models import Resume, EmploymentRecord, ResumeContact, ResumeEducation, Education, Contact
from src.resumes.schemas import ResumeRequest
from src.users.models import Applicant
from src.exceptions import NotAuthenticated


class ResumeService:
    db: AsyncSession

    def __init__(
            self,
            db: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.db = db

    async def create_resume(self, resume: ResumeRequest, user: Applicant) -> Resume:
        db_resume = Resume(
            job_title=resume.job_title,
            description=resume.description,
            applicant_id=resume.applicant_id,
            personal_qualities=resume.personal_qualities,
           # status_id=resume.status,
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

    async def update_resume(self, resume_id: int, updated_resume: ResumeRequest, user: Applicant) -> Resume:
        db_resume = await self.get_by_id(resume_id)

        if db_resume.applicant_id != user.user_id:
           raise NotAuthenticated() 

        db_resume.job_title = updated_resume.job_title
        db_resume.applicant_id = updated_resume.applicant_id
        db_resume.description = updated_resume.description
        db_resume.personal_qualities = updated_resume.personal_qualities
        #db_resume.status_id = updated_resume.status

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

    async def delete_resume(self, id, user: Applicant) -> None:
        stmt = await self.get_by_id(id)
        if stmt.applicant_id != user.user_id:
           raise NotAuthenticated()
        await self.db.delete(stmt)
        await self.db.commit()

    async def get_all_res(self) -> list[Resume] | None:
        select_query = select(Resume)

        return await fetch_all(self.db, select_query)

    async def get_all_edu(self) -> list[Education] | None:
        select_query = select(Education)

        return await fetch_all(self.db, select_query)



    async def get_all_contact(self) -> list[Contact] | None:
        select_query = select(Contact)

        return await fetch_all(self.db, select_query)

    async def upload_photo(self, resume_id: int, file: UploadFile, user: Applicant) -> Resume:
        path = Path("./files/resumes/" + str(resume_id) + "/")
        path.mkdir(parents=True, exist_ok=True, mode=0o777)
        path = "./files/resumes/" + str(resume_id) + "/"

        for root, dirs, files in os.walk(path):
            for momo in dirs:
                os.chown(momo, 502, 20)
                os.chmod(momo, stat.S_IROTH)

        db_resume = await self.get_by_id(resume_id)

        if db_resume.applicant_id != user.user_id:
           raise NotAuthenticated()

        with open("./files/resumes/" + str(resume_id) + "/" + file.filename, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
        file.file.close()
        db_resume.photo = "./files/resumes/" + str(resume_id) + "/" + file.filename

        await self.db.commit()

        return db_resume

def get_resume_service(
        db: Annotated[AsyncSession, Depends(get_db)],
):
    return ResumeService(db)
