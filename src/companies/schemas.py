import re
from datetime import datetime
from typing import List

from src.models import BaseModel
from src.vacancies.schemas import VacancyResponse

class CompanyResponse(BaseModel):
    id:int
    name:str
    owner_id:int
    description:str
    created_at:datetime
    vacancies: list[VacancyResponse]
    population: int
    address: str
    phone: str
    email: str
    logo_path: str  
    

class CompanyRequest(BaseModel):
    name:str
    owner_id:int
    description:str
    population: int
    address: str
    phone: str
    email: str

class CompanySearchRequest(BaseModel):
    name: str | None
    owner_id: int | None
    description: str | None

class ListCompanyResponse(BaseModel):
    notes: List[CompanyResponse]
