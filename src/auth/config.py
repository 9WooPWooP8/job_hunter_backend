from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 300  # minutes

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True

    model_config = SettingsConfigDict(extra="ignore")


auth_config = AuthConfig(_env_file=".env")
