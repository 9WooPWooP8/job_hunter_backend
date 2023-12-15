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
    name: str
    rate: RatesResponse
    experience_min: int
    experience_max: int
    salary_min: int
    salary_max: int
    responses_count: int
    personal_qualities: str


class VacancyRequest(CustomModel):
    description: str
    name: str
    company_id: int | None
    rate_id: int | None
    experience_min: int | None
    experience_max: int | None
    salary_min: int | None
    salary_max: int | None
    personal_qualities: str
