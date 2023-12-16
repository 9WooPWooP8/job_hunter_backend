from __future__ import annotations
from operator import or_

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.passwords import get_password_hash
from src.companies.models import Company
from src.companies.schemas import CompanyRequest
from src.database import fetch_one, fetch_all, get_count, get_db
from src.resumes.models import Resume
from src.resumes.schemas import ResumeRequest
from src.search.schemas import CompaniesFilterSearchRequest, CompaniesFilterSearchResponse, ResumesSearchResponse, VacancySearchResponse
from src.vacancies.models import Vacancy
from src.vacancies.schemas import VacancyRequest

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

    async def find_company(self, filter: CompaniesFilterSearchRequest, limit, page) -> CompaniesFilterSearchResponse | None:
        pagination = self.calculate_pagination(limit, page)

        company_name_search = "%{}%".format(filter.filter_company.name)
        company_name_description = "%{}%".format(filter.filter_company.description)

        select_query = select(Company).filter(or_(Company.name.like(company_name_search), 
                                                  Company.description.like(company_name_description)))\
                                        .offset(pagination["start"])\
                                        .limit(pagination["end"])
        
        total = await fetch_all(self.db, select(Company))
        total = len(total)

        return { "companies": await fetch_all(self.db, select_query), "limit": limit, "page": page, "total": total }

    async def find_vacancies(self, filter: VacancyRequest, limit, page) -> VacancySearchResponse | None:
        pagination = self.calculate_pagination(limit, page)

        vacancies_name_description = "%{}%".format(filter.description)

        select_query = select(Vacancy).filter(or_(Vacancy.description.like(vacancies_name_description),
                                                  Vacancy.company_id == filter.company_id))
        
        if filter.experience_min > 0:
             select_query = select_query.filter(filter.experience_min >= Vacancy.experience_min)

        if filter.experience_max > 0:
            select_query = select_query.filter(filter.experience_max <= Vacancy.experience_max)

        if filter.salary_min > 0:
            select_query = select_query.filter(filter.salary_min >= Vacancy.salary_min)

        if filter.salary_max > 0:
            select_query = select_query.filter(filter.salary_max < Vacancy.salary_max)

        if filter.rate_id >= 0:
            select_query = select_query.filter(filter.rate_id == Vacancy.rate_id)

        select_query = select_query.offset(pagination["start"]).limit(pagination["end"])
        total = await fetch_all(self.db, select(Company))
        total = len(total)

        return { "resumes": await fetch_all(self.db, select_query), "limit": limit, "page": page, "total": total }
    
    async def find_resumes(self, filter: ResumeRequest, limit, page) -> ResumesSearchResponse | None:
        pagination = self.calculate_pagination(limit, page)

        resumes_description = "%{}%".format(filter.description)
        job_title = "%{}%".format(filter.job_title)

        select_query = select(Resume).filter(or_(Resume.description.like(resumes_description),
                                                  Resume.job_title.like(job_title)))
        
        if filter.applicant_id:
             select_query = select_query.filter(filter.applicant_id == Vacancy.applicant_id)

        select_query = select_query.offset(pagination["start"]).limit(pagination["end"])
        total = await fetch_all(self.db, select(Company))
        total = len(total)

        return { "vacancies": await fetch_all(self.db, select_query), "limit": limit, "page": page, "total": total }

def get_search_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return SearchService(db)
