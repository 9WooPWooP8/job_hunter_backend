import re
from typing import Annotated
from datetime import datetime

from src.models import CustomModel


class CompanyResponse(CustomModel):
    id:int
    name:str
    owner_id:int
    description:str
    created_at:datetime

class CompanyRequest(CustomModel):
    name:str
    owner_id:int
    description:str