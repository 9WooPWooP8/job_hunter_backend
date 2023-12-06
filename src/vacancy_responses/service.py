from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import fetch_all, fetch_one, get_db
from src.notifications.service import NotificationService, get_notifiaction_service
from src.resumes.models import Resume
from src.users.models import Applicant
from src.vacancies.models import Vacancy
from src.vacancy_responses.enums import VacancyResponseStatusEnum
from src.vacancy_responses.models import VacancyResponse, VacancyResponseStatus
from src.vacancy_responses.schemas import VacancyResponseCreate


class VacancyResponseService:
    db: AsyncSession
    notification_service: NotificationService

    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
        notification_service: Annotated[
            NotificationService, Depends(get_notifiaction_service)
        ],
    ):
        self.db = db
        self.notification_service = notification_service

    async def create_vacancy_response(
        self, vacancy_response_data: VacancyResponseCreate
    ) -> VacancyResponse:
        vacancy_response = VacancyResponse(
            vacancy_id=vacancy_response_data.vacancy_id,
            resume_id=vacancy_response_data.resume_id,
            status_id=VacancyResponseStatusEnum.WAITING_FOR_REVIEW.value,
        )

        self.db.add(vacancy_response)

        await self.db.commit()
        await self.db.refresh(vacancy_response)

        return vacancy_response

    async def get_by_id(
        self, resume_id: int, vacancy_id: int
    ) -> VacancyResponse | None:
        stmt = (
            select(VacancyResponse)
            .where(VacancyResponse.vacancy_id == vacancy_id)
            .where(VacancyResponse.resume_id == resume_id)
        )

        print(await fetch_all(self.db, stmt))

        vacancy_response = await fetch_one(self.db, stmt)

        return vacancy_response

    async def get_vacancy_responses_by_company(
        self, company_id: int
    ) -> list[VacancyResponse] | None:
        stmt = (
            select(VacancyResponse)
            .join(VacancyResponse.vacancy)
            .join(VacancyResponse.resume)
            .join(Resume.applicant)
            .join(Applicant.user)
            .where(Vacancy.company_id == company_id)
        )

        vacancy_responses = await fetch_all(self.db, stmt)

        print(vacancy_responses)

        return vacancy_responses

    async def get_vacancy_responses_by_applicant(
        self, applicant_id: int
    ) -> list[VacancyResponse] | None:
        stmt = (
            select(VacancyResponse)
            .join(VacancyResponse.resume)
            .where(VacancyResponse.resume.applicant_id == applicant_id)
        )

        vacancy_responses = await fetch_all(self.db, stmt)

        return vacancy_responses

    async def update_vacancy_response_status(
        self, vacancy_id: int, resume_id: int, status_id: int
    ) -> VacancyResponse:
        vacancy_response = await self.get_by_id(resume_id, vacancy_id)

        if vacancy_response.status_id != status_id:
            if status_id == 2:
                notification_text = (
                    f"Ваше резюме {vacancy_response.resume.job_title} "
                    f"просмотрела компания {vacancy_response.vacancy.company.description}."
                )
            elif status_id == 3:
                notification_text = (
                    f"Вы получили отказ на отклик с резюме {vacancy_response.resume.job_title} "
                    f"от компании {vacancy_response.vacancy.company.description}."
                )
            await self.notification_service.create_notification(
                vacancy_response.resume.applicant_id, notification_text
            )

        vacancy_response.status_id = status_id

        await self.db.commit()
        await self.db.refresh(vacancy_response)

        return vacancy_response

    async def get_vacancy_response_statuses(self) -> VacancyResponse:
        stmt = select(VacancyResponseStatus)

        return await fetch_all(self.db, stmt)


def get_vacancy_response_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    ns = NotificationService(db)
    return VacancyResponseService(db, ns)
