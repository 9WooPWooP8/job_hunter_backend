import re
from typing import Annotated
from datetime import datetime
from src.companies.schemas import CompanyRequest, CompanyResponse, CompanySearchRequest

from src.models import BaseModel
from src.vacancies.schemas import VacancyResponse

class CompaniesFilterSearchRequest(BaseModel):
    filter_company: CompanySearchRequest

class VacancySearchResponse(BaseModel):
    vacancies: list[VacancyResponse]
    total: int
    limit: int
    page: int

class CompaniesFilterSearchResponse(BaseModel):
    companies: list[CompanyResponse]
    total: int
    limit: int
    page: int