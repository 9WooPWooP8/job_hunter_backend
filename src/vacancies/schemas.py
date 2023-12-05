from datetime import datetime

from src.models import CustomModel
from src.rates.schemas import RatesResponse


class VacancyResponse(CustomModel):
    id: int
    description: str
    created_at: datetime
    company_id: int
    status_id: int
    rate_id: int
    rate: RatesResponse
    experience_min: int
    experience_max: int
    salary_min: int
    salary_max: int


class VacancyRequest(CustomModel):
    name: str
    description: str
    company_id: int
    rate_id: int
    experience_min: int
    experience_max: int
    salary_min: int
    salary_max: int
