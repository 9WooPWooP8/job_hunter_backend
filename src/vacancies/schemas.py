import re
from typing import Annotated
from datetime import datetime

from src.models import CustomModel


class VacancyResponse(CustomModel):
    id:int
    description:str
    created_at:datetime
    company_id:int
    status_id:int

class VacancyRequest(CustomModel):
    name:str
    description:str
    company_id:int