from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

import src.vacancies.service as vacancy_service
from src.auth.dependencies import recruiter_is_authenticated
from src.users.models import Recruiter
from src.vacancies.schemas import VacancyRequest, VacancyResponse

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@cbv(router)
class VacanciesCBV:
    _vacancy_service: vacancy_service.VacancyService = Depends(
        vacancy_service.get_vacancy_service
    )

    @router.get("/", response_model=list[VacancyResponse])
    async def get_all(self) -> list[VacancyResponse]:
        return await self._vacancy_service.get_all()

    @router.get("/{id}", response_model=VacancyResponse)
    async def get_by_id(
        self,
        id: int,
    ) -> list[VacancyResponse]:
        return await self._vacancy_service.get_by_id(id)

    @router.post("/", response_model=VacancyResponse)
    async def create_vacancy(
        self,
        vacancy_data: VacancyRequest,
        user: Recruiter | None = Depends(recruiter_is_authenticated),
    ) -> list[VacancyResponse]:
        return await self._vacancy_service.create_vacancy(vacancy_data, user)

    @router.put("/{id}", response_model=VacancyResponse)
    async def update_vacancy(
        self,
        id: int,
        vacancy_data: VacancyRequest,
    ) -> VacancyResponse:
        return await self._vacancy_service.update_vacancy(id, vacancy_data)

    @router.delete("/{id}", response_model=None)
    async def delete_vacancy(
        self,
        id: int,
    ) -> VacancyResponse:
        return await self._vacancy_service.delete_vacancy(id)

    @router.put("/{id}/activate", response_model=None)
    async def activate_vacancy(
        self,
        id: int,
    ) -> VacancyResponse:
        return await self._vacancy_service.activate_vacancy(id)

    @router.put("/{id}/disable", response_model=None)
    async def delete_vacancy(
        self,
        id: int,
    ) -> VacancyResponse:
        return await self._vacancy_service.disable_vacancy(id)
