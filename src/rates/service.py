from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import fetch_all, get_db
from src.rates.models import Rate


class RatesService:
    db: AsyncSession

    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.db = db

    async def get_all(self) -> list[Rate] | None:
        select_query = select(Rate)

        return await fetch_all(self.db, select_query)


# TODO:
def get_rates_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return RatesService(db)
