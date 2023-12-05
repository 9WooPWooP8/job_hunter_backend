from datetime import datetime

from src.models import CustomModel
from src.vacancy_responses.enums import VacancyResponseStatus


class VacancyResponseStatusUpdate(CustomModel):
    status_id: VacancyResponseStatus


class VacancyResponseCreate(CustomModel):
    resume_id: int
    vacancy_id: int


class VacancyResponseStatus(CustomModel):
    id: int
    name: str


class VacancyResponseResponse(CustomModel):
    resume_id: int
    vacancy_id: int
    created_at: datetime
    status: VacancyResponseStatus


class VacancyResponseApplicant(CustomModel):
    id: int
    name: str


class VacancyResponseVacancy(CustomModel):
    id: int
    name: str


class VacancyResponseListResponse(CustomModel):
    applicant_name: str
    applicant_description: str
    resume_id: int
    vacancy_title: str
