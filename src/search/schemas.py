import re
from typing import Annotated
from datetime import datetime
from src.companies.schemas import CompanyRequest, CompanyResponse, CompanySearchRequest

from src.models import BaseModel

class CompaniesFilterSearchRequest(BaseModel):
    filter_company: CompanySearchRequest

class CompaniesFilterSearchResponse(BaseModel):
    companies: list[CompanyResponse]
    total: int
    limit: int
    page: int