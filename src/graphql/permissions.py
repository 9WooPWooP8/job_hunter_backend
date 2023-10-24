from __future__ import annotations

from typing import Any

from strawberry.permission import BasePermission

from src.graphql.context import Info


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        return bool(info.context.user)


class IsRecruiter(IsAuthenticated):
    message = "Recruiter is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        is_authenticated = super().has_permission(source, info, **kwargs)
        if is_authenticated:
            recruiter = await info.context.user_service.get_recruiter_by_id(
                info.context.user.user_id
            )

            return bool(recruiter)
        else:
            return False


class IsApplicant(IsAuthenticated):
    message = "Recruiter is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        is_authenticated = super().has_permission(source, info, **kwargs)

        if is_authenticated:
            applicant = await info.context.user_service.get_applicant_by_id(
                info.context.user.user_id
            )

            return bool(applicant)
        else:
            return False
