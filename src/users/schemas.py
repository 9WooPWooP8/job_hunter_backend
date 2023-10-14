from pydantic import constr

from src.models import CustomModel
from src.users.enums import ApplicantStatus


class UserCreate(CustomModel):
    username: constr(pattern="^[A-Za-z0-9-_]+$", to_lower=True, strip_whitespace=True)
    password: str
    email: str
    first_name: str
    last_name: str


class ApplicantCreate(UserCreate):
    status_id: ApplicantStatus


class ApplicantCreateResponse(CustomModel):
    user_id: int


class RecruiterCreate(UserCreate):
    pass


class RecruiterCreateResponse(CustomModel):
    user_id: int


class UserResponse(CustomModel):
    id: int
    username: constr(pattern="^[A-Za-z0-9-_]+$", to_lower=True, strip_whitespace=True)
    email: str
    first_name: str
    last_name: str


class TokenData(CustomModel):
    username: str | None = None
