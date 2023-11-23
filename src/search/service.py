from __future__ import annotations
from operator import or_

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.passwords import get_password_hash
from src.companies.models import Company
from src.companies.schemas import CompanyRequest
from src.database import fetch_one, fetch_all, get_db
from src.search.schemas import CompaniesFilterSearchRequest

class SearchService:
    db: AsyncSession

    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.db = db

    def calculate_pagination(self, limit, page):
        start = (page - 1) * limit
        end = start + limit
        return { "start": start, "end": end }

    async def find_company(self, filter: CompaniesFilterSearchRequest, limit, page) -> list[Company] | None:
        pagination = self.calculate_pagination(limit, page)

        company_name_search = "%{}%".format(filter.filter_company.name)
        company_name_description = "%{}%".format(filter.filter_company.description)

        select_query = select(Company).filter(or_(Company.name.like(company_name_search), 
                                                  Company.description.like(company_name_description)))\
                                        .offset(pagination["start"])\
                                        .limit(pagination["end"])
        return await fetch_all(self.db, select_query)

def get_search_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return SearchService(db)
