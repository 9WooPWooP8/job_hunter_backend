from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.config import app_configs, settings
from src.graphql import graphql_app
from src.users.router import router as users_router

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(auth_router)
app.include_router(users_router)

app.include_router(graphql_app, prefix="/graphql")
