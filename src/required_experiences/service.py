from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import fetch_all, get_db
from src.required_experiences.models import RequiredExperience


class RequiredExperiencesService:
    db: AsyncSession

    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.db = db

    async def get_all(self) -> list[RequiredExperience] | None:
        select_query = select(RequiredExperience)

        return await fetch_all(self.db, select_query)

# TODO:
def get_experience_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return RequiredExperiencesService(db)
