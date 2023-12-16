from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import fetch_all, fetch_one, get_db
from src.vacancies.enums import VacancyStatus
from src.vacancies.models import Vacancy
from src.vacancies.schemas import VacancyRequest
from src.users.models import Recruiter
from src.exceptions import NotAuthenticated
from src.companies.models import Company


class VacancyService:
    db: AsyncSession

    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.db = db

    async def get_all(self) -> list[Vacancy] | None:
        select_query = select(Vacancy)

        return await fetch_all(self.db, select_query)

    async def get_by_id(self, id) -> Vacancy | None:
        select_query = select(Vacancy).where(Vacancy.id == id)

        return await fetch_one(self.db, select_query)

    async def create_vacancy(self, vacancy: VacancyRequest) -> Vacancy:
        db_vacancy = Vacancy(
            description=vacancy.description,
            company_id=vacancy.company_id,
            name=vacancy.name,
            status_id=VacancyStatus.ACTIVE.value,
            rate_id=vacancy.rate_id,
            experience_max=vacancy.experience_max,
            experience_min=vacancy.experience_min,
            plug="",
            salary_min=vacancy.salary_min,
            salary_max=vacancy.salary_max,
            personal_qualities=vacancy.personal_qualities,
        )
        self.db.add(db_vacancy)
        await self.db.commit()

        await self.db.refresh(db_vacancy)

        return db_vacancy

    async def disable_vacancy(self, vacancy_id: int, user: Recruiter) -> Vacancy:
        db_vacancy = await self.get_by_id(vacancy_id)

        select_query = select(Company).where(Company.id == db_vacancy.company_id)

        db_company = await fetch_one(self.db, select_query)

        if db_company is  None or db_company.owner_id != user.user_id:
           raise NotAuthenticated()                

        db_vacancy.status_id = VacancyStatus.NOT_ACTIVE.value

        await self.db.commit()

        return db_vacancy

    async def activate_vacancy(self, vacancy_id: int, user: Recruiter) -> Vacancy:
        db_vacancy = await self.get_by_id(vacancy_id)

        select_query = select(Company).where(Company.id == db_vacancy.company_id)

        db_company = await fetch_one(self.db, select_query)

        if db_company is  None or db_company.owner_id != user.user_id:
           raise NotAuthenticated()

        db_vacancy.status_id = VacancyStatus.ACTIVE.value

        await self.db.commit()

        return db_vacancy

    async def delete_vacancy(self, id, user: Recruiter) -> None:
        db_vacancy = self.get_by_id(id)

        select_query = select(Company).where(Company.id == db_vacancy.company_id)

        db_company = await fetch_one(self.db, select_query)

        if db_company is  None or db_company.owner_id != user.user_id:
           raise NotAuthenticated()
        
        self.db.delete(db_vacancy)
        await self.db.commit()

    async def update_vacancy(self, vacancy_id: int, vacancy: VacancyRequest, user: Recruiter) -> Vacancy:
        db_vacancy = await self.get_by_id(vacancy_id)

        select_query = select(Company).where(Company.id == db_vacancy.company_id)

        db_company = await fetch_one(self.db, select_query)

        if db_company is  None or db_company.owner_id != user.user_id:
           raise NotAuthenticated()

        db_vacancy.description = vacancy.description
        db_vacancy.name = vacancy.name
        db_vacancy.rate_id = vacancy.rate_id
        db_vacancy.experience_min = vacancy.experience_min
        db_vacancy.experience_max = vacancy.experience_max
        db_vacancy.salary_min = vacancy.salary_min
        db_vacancy.salary_max = vacancy.salary_max
        db_vacancy.personal_qualities = vacancy.personal_qualities

        await self.db.commit()

        return db_vacancy


# TODO:
def get_vacancy_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return VacancyService(db)
