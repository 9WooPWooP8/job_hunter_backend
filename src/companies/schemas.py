import re
from datetime import datetime
from typing import List

from src.models import BaseModel
from src.users.schemas import UserResponse

class CompanyResponse(BaseModel):
    id:int
    name:str
    owner_id:int
    description:str
    created_at:datetime
    

class CompanyRequest(BaseModel):
    name:str
    owner_id:int
    description:str

class CompanySearchRequest(BaseModel):
    name: str | None
    owner_id: int | None
    description: str | None

class ListCompanyResponse(BaseModel):
    notes: List[CompanyResponse]
