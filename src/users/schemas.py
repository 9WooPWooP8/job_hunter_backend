from pydantic import constr

from src.models import CustomModel


class UserCreate(CustomModel):
    username: constr(pattern="^[A-Za-z0-9-_]+$", to_lower=True, strip_whitespace=True)
    password: str
    email: str
    first_name: str
    last_name: str


class TokenData(CustomModel):
    username: str | None = None
