from fastapi import APIRouter

from src.users.schemas import UserCreate
from src.users.service import create_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def register_user(user: UserCreate):
    return await create_user(user)
