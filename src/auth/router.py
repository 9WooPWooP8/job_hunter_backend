from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from fastapi.exceptions import HTTPException

from src.auth import jwt, service, utils
from src.auth.dependencies import valid_refresh_token, valid_refresh_token_user
from src.auth.schemas import AuthData, AuthTokens

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=AuthTokens)
async def auth_user(auth_data: AuthData, response: Response) -> AuthTokens:
    user = await service.authenticate_user(auth_data.username, auth_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    refresh_token_value = await service.create_refresh_token(user_id=user["id"])
    access_token = jwt.create_access_token(user=user)

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AuthTokens(
        access_token=access_token,
        refresh_token=refresh_token_value,
    )


@router.put("/tokens", response_model=AuthTokens)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
    user: dict[str, Any] = Depends(valid_refresh_token_user),
) -> AuthTokens:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, refresh_token["id"])

    access_token = jwt.create_access_token(user=user)

    return AuthTokens(
        access_token=access_token,
        refresh_token=refresh_token_value,
    )


# @router.get("/items")
# async def read_items(user: Annotated[dict, Depends(get_current_user)]):
#     return user
