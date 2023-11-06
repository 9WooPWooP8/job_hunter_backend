from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.passwords import get_password_hash
from src.database import fetch_one, fetch_all, get_db
from src.companies.models import Company
from src.companies.schemas import (
    CompanyRequest
)
from src.users.models import Recruiter


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
            name = company.name,
            owner_id = user.user_id,
            description = company.description
        )
        self.db.add(db_company)
        await self.db.commit()

        await self.db.refresh(db_company)

        return db_company
    
    async def delete_company(self, id) -> None:
        db_company = self.get_by_id(id)
        self.db.delete(db_company)
        await self.db.commit()

    async def update_company(
        self, company_id: int, company: CompanyRequest
    ) -> Company:
        db_company = await self.get_by_id(company_id)

        db_company.name = company.name
        db_company.description = company.description

        await self.db.commit()

        return db_company


# TODO:
def get_company_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return CompanyService(db)
