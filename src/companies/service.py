from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.companies.models import Company
from src.companies.schemas import CompanyRequest
from src.database import fetch_all, fetch_one, get_db
from src.users.models import Recruiter
from fastapi import UploadFile
from pathlib import Path
import os
import stat


class CompanyService:
    db: AsyncSession

    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.db = db

    async def get_all(self) -> list[Company] | None:
        select_query = select(Company)
        return await fetch_all(self.db, select_query)

    async def get_by_id(self, id) -> Company | None:
        select_query = select(Company).where(Company.id == id)

        return await fetch_one(self.db, select_query)

    async def create_company(self, company: CompanyRequest, user: Recruiter) -> Company:
        db_company = Company(
            name=company.name, owner_id=user.user_id, description=company.description,
            population=company.population, address=company.address, phone=company.phone, email=company.email,
            logo_path=""
        )
        self.db.add(db_company)
        await self.db.commit()

        await self.db.refresh(db_company)

        return db_company

    async def delete_company(self, id) -> None:
        db_company = self.get_by_id(id)
        self.db.delete(db_company)
        await self.db.commit()

    async def update_company(self, company_id: int, company: CompanyRequest) -> Company:
        db_company = await self.get_by_id(company_id)

        db_company.name = company.name
        db_company.description = company.description

        await self.db.commit()

        return db_company
    
    async def upload_logo(self, company_id: int, file: UploadFile) -> Company:
        path = Path("./files/companies/"+str(company_id)+"/")
        path.mkdir(parents=True, exist_ok=True, mode=0o777)
        path = "./files/companies/"+str(company_id)+"/"
        
        for root, dirs, files in os.walk(path):
            for momo in dirs:
                os.chown(momo, 502, 20)
                os.chmod(momo, stat.S_IROTH)

        db_company = await self.get_by_id(company_id)

        with open("./files/companies/"+str(company_id)+"/"+file.filename, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
        file.file.close()
        db_company.logo_path = "./files/companies/"+str(company_id)+"/"+file.filename

        await self.db.commit()

        return db_company    


# TODO:
def get_company_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return CompanyService(db)
