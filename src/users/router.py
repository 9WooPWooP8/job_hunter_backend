from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.dependencies import user_is_authenticated
from src.users import service as user_service
from src.users.dependencies import valid_applicant_create, valid_recruiter_create
from src.users.schemas import (
    ApplicantCreate,
    ApplicantCreateResponse,
    RecruiterCreate,
    RecruiterCreateResponse,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_my_account(
    user: dict[str, any] = Depends(user_is_authenticated)
) -> UserResponse:
    return user


@router.post("/recruiters", response_model=RecruiterCreateResponse)
async def register_as_recruiter(
    recruiter_data: Annotated[RecruiterCreate, Depends(valid_recruiter_create)],
) -> RecruiterCreateResponse:
    return await user_service.create_recruiter(recruiter_data)


@router.post("/applicants", response_model=ApplicantCreateResponse)
async def register_as_applicant(
    applicant_data: Annotated[ApplicantCreate, Depends(valid_applicant_create)],
) -> ApplicantCreateResponse:
    return await user_service.create_applicant(applicant_data)
