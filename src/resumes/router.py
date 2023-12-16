from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi_restful.cbv import cbv

import src.resumes.service as resume_service

from src.resumes.schemas import ResumeResponse, ResumeRequest, Education, ResumeContact, PoluchitContact
from src.users.models import Applicant
from src.auth.dependencies import applicant_is_authenticated

router = APIRouter(prefix="/resumes", tags=["resumes"])


@cbv(router)
class ResumesCBV:
    _resumes_service: resume_service.ResumeService = Depends(resume_service.get_resume_service)

    @router.post("/", response_model=ResumeResponse)
    async def create_resume(
            self,
            resume_data: ResumeRequest,
            user: Applicant | None = Depends(applicant_is_authenticated),
    ) -> ResumeResponse:
        return await self._resumes_service.create_resume(resume_data)

    @router.get("/{id}", response_model=ResumeResponse)
    async def get_by_id(
            self,
            id: int,
    ) -> list[ResumeResponse]:
        print(await self._resumes_service.get_by_id(id))
        return await self._resumes_service.get_by_id(id)

    @router.delete("/{id}", response_model=None)
    async def delete_resume(
            self,
            id: int,
            user: Applicant | None = Depends(applicant_is_authenticated),
    ) -> list[ResumeResponse]:
        return await self._resumes_service.delete_resume(id)

    @router.get("/", response_model=list[ResumeResponse])
    async def get_all(
            self
    ) -> list[ResumeResponse]:
        return await self._resumes_service.get_all_res()

    @router.get("/edu/", response_model=list[Education])
    async def get_all_edu(
            self
    ) -> list[Education]:
        return await self._resumes_service.get_all_edu()

    @router.get("/contact/", response_model=list[PoluchitContact])
    async def get_all_contact(
            self
    ) -> list[PoluchitContact]:
        return await self._resumes_service.get_all_contact()

    @router.put("/{id}", response_model=ResumeResponse)
    async def update_resume(
            self,
            id: int,
            resume_data: ResumeRequest,
            user: Applicant | None = Depends(applicant_is_authenticated),
    ) -> ResumeResponse:
        return await self._resumes_service.update_resume(id, resume_data)

    @router.post("/{id}/photo", response_model=ResumeResponse)
    async def upload_photo(
            self,
            id: int,
            photo: UploadFile,
            user: Applicant | None = Depends(applicant_is_authenticated),
    ) -> ResumeResponse:
        return await self._resumes_service.upload_photo(id, photo)
