from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from src.companies.schemas import CompanyResponse, ListCompanyResponse

import src.search.service as search_service
from src.search.schemas import (
    CompaniesFilterSearchRequest,
    CompaniesFilterSearchResponse,
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
        search_data = await self._search_service.find_company(filter_data, limit, page)
        return { "companies": search_data, "total": len(search_data), "limit": limit, "page": page }
    
    @router.post("/get_vacancies", response_model=VacancySearchResponse)
    async def get_vacancies(
        self,
        filter_data: VacancyRequest,
        limit: int = 10, 
        page: int = 1,
    ) -> VacancySearchResponse:
        search_data = await self._search_service.find_vacancies(filter_data, limit, page)
        return { "vacancies": search_data, "total": len(search_data), "limit": limit, "page": page }