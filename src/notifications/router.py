from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

import src.notifications.service as notification_service
from src.auth.dependencies import applicant_is_authenticated
from src.notifications.schemas import NotificationResponse
from src.users.models import Applicant

router = APIRouter(prefix="/notifications", tags=["notifications"])


@cbv(router)
class NotificationsCBV:
    _notification_service: notification_service.NotificationService = Depends(
        notification_service.get_notifiaction_service
    )

    @router.get("/", response_model=list[NotificationResponse])
    async def get_notifications_for_authed_applicant(
        self,
        applicant: Applicant | None = Depends(applicant_is_authenticated),
    ) -> list[NotificationResponse]:
        vacancy_responses = (
            await self._notification_service.get_notifications_by_applicant(
                applicant.user_id
            )
        )

        return vacancy_responses
