from datetime import datetime

from src.models import CustomModel


class RatesResponse(CustomModel):
    id: int
    name: str
