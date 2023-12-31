from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.companies.router import router as companies_router
from src.config import app_configs, settings
from src.notifications.router import router as notifications_router
from src.rates.router import router as rates_router
from src.resumes.router import router as resumes_router
from src.search.router import router as search_router
from src.users.router import router as users_router
from src.vacancies.router import router as vacancies_router
from src.vacancy_responses.router import router as vacancy_responses_router

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
app.include_router(companies_router)
app.include_router(vacancies_router)
app.include_router(search_router)
app.include_router(resumes_router)
app.include_router(rates_router)
app.include_router(vacancy_responses_router)
app.include_router(notifications_router)

Path("./files").mkdir(parents=True, exist_ok=True)
app.mount("/files", StaticFiles(directory="files"), name="files")
