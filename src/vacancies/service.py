from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import fetch_all, fetch_one, get_db
from src.vacancies.enums import VacancyStatus
from src.vacancies.models import Vacancy
from src.vacancies.schemas import VacancyRequest


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
            status_id=VacancyStatus.ACTIVE,
        )
        self.db.add(db_vacancy)
        await self.db.commit()

        await self.db.refresh(db_vacancy)

        return db_vacancy

    async def disable_vacancy(self, vacancy_id: int) -> Vacancy:
        db_vacancy = await self.get_by_id(vacancy_id)

        db_vacancy.status_id = VacancyStatus.NOT_ACTIVE

        await self.db.commit()

        return db_vacancy

    async def activate_vacancy(self, vacancy_id: int) -> Vacancy:
        db_vacancy = await self.get_by_id(vacancy_id)

        db_vacancy.status_id = VacancyStatus.ACTIVE

        await self.db.commit()

        return db_vacancy

    async def delete_vacancy(self, id) -> None:
        db_vacancy = self.get_by_id(id)
        self.db.delete(db_vacancy)
        await self.db.commit()

    async def update_vacancy(self, vacancy_id: int, vacancy: VacancyRequest) -> Vacancy:
        db_vacancy = await self.get_by_id(vacancy_id)

        db_vacancy.description = vacancy.description

        await self.db.commit()

        return db_vacancy


# TODO:
def get_vacancy_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return VacancyService(db)
