from datetime import datetime

from src.models import CustomModel


class NotificationResponse(CustomModel):
    id: int
    text: str
    created_at: datetime
