import strawberry
from strawberry.fastapi import GraphQLRouter

from src.graphql.context import Info, get_context
from src.graphql.permissions import IsApplicant, IsRecruiter


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
        info: Info,
        id: int,
    ) -> User | None:
        return info.context.user_service.get_user_by_id(id)

    @strawberry.field(permission_classes=[IsRecruiter, IsApplicant])
    def applicant(
        self,
        info: Info,
        id: int,
    ) -> Applicant | None:
        return info.context.user_service.get_applicant_by_id(id)

    @strawberry.field
    def recruiter(
        self,
        info: Info,
        id: int,
    ) -> Recruiter | None:
        return info.context.user_service.get_recruiter_by_id(id)


schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
