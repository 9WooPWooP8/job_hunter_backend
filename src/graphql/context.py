from typing import Annotated

from fastapi import Depends, Header
from starlette.requests import Request
from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from src.auth.jwt import parse_jwt_access_token
from src.users.service import UserService, get_user_service


class GrpahQLContext(BaseContext):
    def __init__(
        self,
        user_service: Annotated[UserService, Depends(get_user_service)],
        request: Request = None,
        authorization: Annotated[str | None, Header()] = None,
    ):
        self.user_service = user_service
        self.request = request
        self.user = None

        if authorization:
            self.user = parse_jwt_access_token(authorization[7:])


Info = _Info[GrpahQLContext, RootValueType]


async def get_context(
    custom_context=Depends(GrpahQLContext),
):
    return custom_context
