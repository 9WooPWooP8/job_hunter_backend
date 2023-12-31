from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from src.companies.schemas import CompanyResponse, ListCompanyResponse
from src.resumes.schemas import ResumeRequest

import src.search.service as search_service
from src.search.schemas import (
    CompaniesFilterSearchRequest,
    CompaniesFilterSearchResponse,
    ResumesSearchResponse,
    VacancySearchResponse,
)
from src.vacancies.schemas import VacancyRequest

router = APIRouter(prefix="/search", tags=["search"])

@cbv(router)
class SearchCBV:
    _search_service: search_service.SearchService = Depends(search_service.get_search_service)

    @router.post("/get_companies", response_model=CompaniesFilterSearchResponse)
    async def get_companies(
        self,
        filter_data: CompaniesFilterSearchRequest,
        limit: int = 10, 
        page: int = 1,
    ) -> CompaniesFilterSearchResponse:
        return await self._search_service.find_company(filter_data, limit, page)
    
    @router.post("/get_vacancies", response_model=VacancySearchResponse)
    async def get_vacancies(
        self,
        filter_data: VacancyRequest,
        limit: int = 10, 
        page: int = 1,
    ) -> VacancySearchResponse:
        return await self._search_service.find_vacancies(filter_data, limit, page)
    
    @router.post("/get_resumes", response_model=ResumesSearchResponse)
    async def get_resumes(
        self,
        filter_data: ResumeRequest,
        limit: int = 10, 
        page: int = 1,
    ) -> ResumesSearchResponse:
        print(await self._search_service.find_resumes(filter_data, limit, page))
        return await self._search_service.find_resumes(filter_data, limit, page)