import re

from pydantic import Field

from src.models import CustomModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class AuthTokens(CustomModel):
    access_token: str
    refresh_token: str


class TokenData(CustomModel):
    username: str | None = None


class JWTData(CustomModel):
    user_id: int = Field(alias="sub")


class AuthData(CustomModel):
    username: str
    password: str = Field(min_length=6, max_length=128)

    # @field_validator("password", mode="after")
    # @classmethod
    # def valid_password(cls, password: str) -> str:
    #     if not re.match(STRONG_PASSWORD_PATTERN, password):
    #         raise ValueError(
    #             "Password must contain at least "
    #             "one lower character, "
    #             "one upper character, "
    #             "digit or "
    #             "special symbol"
    #         )

    #     return password
