from typing import Annotated

import strawberry
from fastapi import Depends
from strawberry.fastapi import BaseContext, GraphQLRouter

from src.users.service import UserService, get_user_service


class CustomContext(BaseContext):
    def __init__(self, user_service: Annotated[UserService, get_user_service]):
        print("WHY DO I LOVE FASDF")
        self.user_service = user_service


async def get_context(
    custom_context=Depends(CustomContext),
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
class Query:
    @strawberry.field
    def user(
        self,
        info,
        id: int,
    ) -> User:
        return info.context.user_service.get_user_by_id(id)


schema = strawberry.Schema(query=Query)


graphql_app = GraphQLRouter(schema, context_getter=get_context)
