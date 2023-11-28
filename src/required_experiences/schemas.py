from datetime import datetime

from src.models import CustomModel


class RequiredExperienceResponse(CustomModel):
    id: int
    name: str
