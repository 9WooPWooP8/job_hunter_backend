from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

import src.vacancy_responses.service as vacancy_response_service
from src.auth.dependencies import applicant_is_authenticated, recruiter_is_authenticated
from src.users.models import Applicant, Recruiter
from src.vacancy_responses.schemas import (
    VacancyResponseCreate,
    VacancyResponseListResponse,
    VacancyResponseResponse,
    VacancyResponseStatus,
    VacancyResponseStatusUpdate,
)

router = APIRouter(prefix="/vacancy_responses", tags=["vacancy_responses"])


@cbv(router)
class VacancyResponseCBV:
    _vacancy_response_service: vacancy_response_service.VacancyResponseService = (
        Depends(vacancy_response_service.get_vacancy_response_service)
    )

    @router.get("/", response_model=list[VacancyResponseListResponse])
    async def get_by_company(
        self,
        company_id: int,
    ) -> list[VacancyResponseListResponse]:
        vacancy_responses = (
            await self._vacancy_response_service.get_vacancy_responses_by_company(
                company_id
            )
        )

        vacancy_responses_schema = []

        for vacancy_response in vacancy_responses:
            vacancy_responses_schema.append(
                VacancyResponseListResponse(
                    applicant_name=vacancy_response.resume.applicant.user.first_name
                    + vacancy_response.resume.applicant.user.last_name,
                    applicant_description=vacancy_response.resume.description,
                    resume_id=vacancy_response.resume_id,
                    vacancy_title=vacancy_response.vacancy.description,
                )
            )

        return vacancy_responses_schema

    # @router.get("/", response_model=list[VacancyResponseListResponse])
    # async def get_by_resume(
    #     self,
    #     applicant_id: int,
    # ) -> list[VacancyResponseListResponse]:
    #     return await self._vacancy_response_service.get_vacancy_responses_by_applicant(
    #         applicant_id
    #     )

    @router.post("/", response_model=VacancyResponseResponse)
    async def create(
        self,
        vacancy_response_data: VacancyResponseCreate,
        applicant: Applicant | None = Depends(applicant_is_authenticated),
    ) -> VacancyResponseResponse:
        return await self._vacancy_response_service.create_vacancy_response(
            vacancy_response_data
        )

    @router.put(
        "/{vacancy_id}/{resume_id}/status", response_model=VacancyResponseResponse
    )
    async def update_status(
        self,
        vacancy_id: int,
        resume_id: int,
        status_data: VacancyResponseStatusUpdate,
        recruiter: Recruiter | None = Depends(recruiter_is_authenticated),
    ) -> VacancyResponseResponse:
        return await self._vacancy_response_service.update_vacancy_response_status(
            vacancy_id, resume_id, status_data.status_id.value
        )

    @router.get("/statuses", response_model=list[VacancyResponseStatus])
    async def get_vacancy_response_statuses(
        self,
    ) -> VacancyResponseResponse:
        return await self._vacancy_response_service.get_vacancy_response_statuses()
