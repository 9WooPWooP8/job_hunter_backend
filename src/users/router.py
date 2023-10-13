from fastapi import APIRouter, Depends

from src.auth.dependencies import user_authenticated
from src.users import service as user_service
from src.users.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def register_user(user: UserCreate):
    return await user_service.create_user(user)


@router.get("/me", response_model=UserResponse)
async def get_my_account(
    user: dict[str, any] = Depends(user_authenticated)
) -> UserResponse:
    return user
