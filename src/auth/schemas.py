from pydantic import Field

from src.models import CustomModel


class AuthTokens(CustomModel):
    access_token: str
    refresh_token: str


class TokenData(CustomModel):
    username: str | None = None


class JWTClaims(CustomModel):
    user_id: int = Field(alias="sub")


class AuthData(CustomModel):
    username: str
    password: str = Field(min_length=6, max_length=128)
