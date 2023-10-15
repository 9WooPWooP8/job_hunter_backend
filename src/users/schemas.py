import re
from typing import Annotated

from pydantic import EmailStr, StringConstraints, field_validator

from src.models import CustomModel
from src.users.enums import ApplicantStatus

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class UserCreate(CustomModel):
    username: Annotated[
        str,
        StringConstraints(
            pattern="^[A-Za-z0-9-_]+$", to_lower=True, strip_whitespace=True
        ),
    ]
    password: str
    email: EmailStr
    first_name: str
    last_name: str

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password


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
    username: str
    email: str
    first_name: str
    last_name: str


class TokenData(CustomModel):
    username: str | None = None
