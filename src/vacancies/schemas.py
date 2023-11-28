from datetime import datetime

from src.models import CustomModel
from src.rates.models import Rate
from src.required_experiences.models import RequiredExperience


class VacancyResponse(CustomModel):
    id: int
    description: str
    created_at: datetime
    company_id: int
    status_id: int
    experience_id: int
    rate_id: int
    rate: Rate
    experience: RequiredExperience


class VacancyRequest(CustomModel):
    name: str
    description: str
    company_id: int
    experience_id: int
    rate_id: int
