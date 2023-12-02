from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

import src.resumes.service as resume_service

from src.resumes.schemas import ResumeResponse, ResumeRequest

router = APIRouter(prefix="/resumes", tags=["resumes"])


@cbv(router)
class ResumesCBV:
    _resumes_service: resume_service.ResumeService = Depends(resume_service.get_resume_service)

    @router.post("/", response_model=ResumeResponse)
    async def create_resume(
            self,
            resume_data: ResumeRequest,
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
    ) -> list[ResumeResponse]:
        return await self._resumes_service.delete_resume(id)

    @router.get("/", response_model=list[ResumeResponse])
    async def get_all(
            self
    ) -> list[ResumeResponse]:
        return await self._resumes_service.get_all()

    @router.put("/{id}", response_model=ResumeResponse)
    async def update_resume(
            self,
            id: int,
            resume_data: ResumeRequest,
    ) -> ResumeResponse:
        return await self._resumes_service.update_resume(id, resume_data)
