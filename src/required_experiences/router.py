from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

import src.required_experiences.service as experience_service
from src.required_experiences.schemas import RequiredExperienceResponse

router = APIRouter(prefix="/experiences", tags=["experiences"])


@cbv(router)
class ExperiencesCBV:
    _experience_service: experience_service.RequiredExperiencesService = Depends(
        experience_service.get_experience_service
    )

    @router.get("/", response_model=list[RequiredExperienceResponse])
    async def get_all(self) -> list[RequiredExperienceResponse]:
        return await self._experience_service.get_all()
