from src.companies.schemas import CompanyResponse, CompanySearchRequest
from src.models import BaseModel
from src.resumes.schemas import ResumeResponse
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


class ResumesSearchResponse(BaseModel):
    resumes: list[ResumeResponse]
    total: int
    limit: int
    page: int
