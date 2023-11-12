from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

import src.companies.service as company_service
from src.auth.dependencies import recruiter_is_authenticated
from src.companies.schemas import CompanyRequest, CompanyResponse
from src.users.models import Recruiter

router = APIRouter(prefix="/companies", tags=["companies"])


@cbv(router)
class CompaniesCBV:
    _company_service: company_service.CompanyService = Depends(
        company_service.get_company_service
    )

    @router.get("/", response_model=list[CompanyResponse])
    async def get_all(self) -> list[CompanyResponse]:
        return await self._company_service.get_all()

    @router.get("/{id}", response_model=CompanyResponse)
    async def get_by_id(
        self,
        id: int,
    ) -> CompanyResponse:
        return await self._company_service.get_by_id(id)

    @router.post("/", response_model=CompanyResponse)
    async def create_company(
        self,
        company_data: CompanyRequest,
        user: Recruiter | None = Depends(recruiter_is_authenticated),
    ) -> CompanyResponse:
        return await self._company_service.create_company(company_data, user)

    @router.put("/{id}", response_model=CompanyResponse)
    async def update_company(
        self,
        id: int,
        company_data: CompanyRequest,
    ) -> CompanyResponse:
        return await self._company_service.update_company(id, company_data)

    @router.delete("/{id}", response_model=None)
    async def delete_company(
        self,
        id: int,
    ) -> CompanyResponse:
        return await self._company_service.delete_company(id)
