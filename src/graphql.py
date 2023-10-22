from typing import Annotated

import strawberry
from fastapi import Depends
from strawberry.fastapi import BaseContext, GraphQLRouter

from src.users.service import UserService, get_user_service


class GrpahQLContext(BaseContext):
    def __init__(self, user_service: Annotated[UserService, Depends(get_user_service)]):
        self.user_service = user_service


async def get_context(
    custom_context=Depends(GrpahQLContext),
):
    return custom_context


@strawberry.type
class User:
    id: int
    username: str
    email: str
    first_name: str
    last_name: str


@strawberry.type
class Recruiter:
    user_id: int
    user: User


@strawberry.type
class ApplicantStatus:
    name: str
    id: int


@strawberry.type
class Applicant:
    user_id: int
    user: User
    status_id: int
    status: ApplicantStatus


@strawberry.type
class Query:
    @strawberry.field
    def user(
        self,
        info,
        id: int,
    ) -> User | None:
        return info.context.user_service.get_user_by_id(id)

    @strawberry.field
    def applicant(
        self,
        info,
        id: int,
    ) -> Applicant | None:
        return info.context.user_service.get_applicant_by_id(id)

    @strawberry.field
    def recruiter(
        self,
        info,
        id: int,
    ) -> Recruiter | None:
        return info.context.user_service.get_recruiter_by_id(id)


schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
