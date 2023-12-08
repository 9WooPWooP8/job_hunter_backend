from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import fetch_all, get_db
from src.notifications.models import Notification


class NotificationService:
    db: AsyncSession

    def __init__(
        self,
        db: Annotated[AsyncSession, Depends(get_db)],
    ):
        self.db = db

    async def create_notification(self, applicant_id: int, text: str) -> Notification:
        notification = Notification(text=text, applicant_id=applicant_id)

        self.db.add(notification)

        await self.db.commit()
        await self.db.refresh(notification)

        return notification

    async def get_notifications_by_applicant(self, applicant_id: int):
        stmt = select(Notification).where(Notification.applicant_id == applicant_id)

        return await fetch_all(self.db, stmt)


def get_notifiaction_service(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return NotificationService(db)
