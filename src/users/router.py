from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

import src.users.service as user_service
from src.auth.dependencies import applicant_is_authenticated, recruiter_is_authenticated
from src.users.dependencies import valid_applicant_create, valid_recruiter_create
from src.users.models import Applicant, Recruiter
from src.users.schemas import (
    ApplicantCreate,
    ApplicantCreateResponse,
    ApplicantUpdate,
    RecruiterCreate,
    RecruiterCreateResponse,
    RecruiterUpdate,
    UserResponse, ApplicantStatusResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@cbv(router)
class UsersCBV:
    _user_service: user_service.UserService = Depends(user_service.get_user_service)

    @router.get("/recruiters/me", response_model=RecruiterCreateResponse)
    async def get_my_recruiter_account(
        self, user: Recruiter | None = Depends(recruiter_is_authenticated)
    ) -> UserResponse:
        return user

    @router.get("/applicants/me", response_model=ApplicantCreateResponse)
    async def get_my_applicant_account(
        self, user: Applicant | None = Depends(applicant_is_authenticated)
    ) -> UserResponse:
        return user
    
    @router.get("/applicants/{id}", response_model=ApplicantCreateResponse)
    async def get_applicant_by_id(
        self,
        id:int
    ) -> ApplicantCreateResponse:
        return await self._user_service.get_applicant_by_id(id)

    @router.post("/recruiters", response_model=RecruiterCreateResponse)
    async def register_as_recruiter(
        self,
        recruiter_data: Annotated[RecruiterCreate, Depends(valid_recruiter_create)],
    ) -> RecruiterCreateResponse:
        return await self._user_service.create_recruiter(recruiter_data)

    @router.post("/applicants", response_model=ApplicantCreateResponse)
    async def register_as_applicant(
        self,
        applicant_data: Annotated[ApplicantCreate, Depends(valid_applicant_create)],
    ) -> ApplicantCreateResponse:
        return await self._user_service.create_applicant(applicant_data)

    @router.put("/applicants/{id}", response_model=ApplicantCreateResponse)
    async def update_applicant(
        self,
        id: int,
        applicant_data: ApplicantUpdate,
    ) -> ApplicantCreateResponse:
        return await self._user_service.update_applicant(id, applicant_data)

    @router.put("/recruiters/{id}", response_model=RecruiterCreateResponse)
    async def update_recruiter(
        self,
        id: int,
        recruiter_data: RecruiterUpdate,
    ) -> dict:
        return await self._user_service.update_recruiter(id, recruiter_data)

    @router.get("/status/", response_model=list[ApplicantStatusResponse])
    async def get_all_status(
            self
    ) -> list[ApplicantStatusResponse]:
        return await self._user_service.get_all_status()
