from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response

from src.auth import jwt, service, utils
from src.auth.dependencies import valid_refresh_token, valid_refresh_token_user
from src.auth.schemas import AuthData, AuthTokens

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/tokens/recruiters", response_model=AuthTokens)
async def auth_recruiter(auth_data: AuthData, response: Response) -> AuthTokens:
    user = await service.authenticate_recruiter(auth_data.username, auth_data.password)

    refresh_token_value = await service.create_refresh_token(user_id=user["id"])
    access_token = jwt.create_access_token(user=user)

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AuthTokens(
        access_token=access_token,
        refresh_token=refresh_token_value,
    )


@router.post("/tokens/applicants", response_model=AuthTokens)
async def auth_applicant(auth_data: AuthData, response: Response) -> AuthTokens:
    user = await service.authenticate_applicant(auth_data.username, auth_data.password)

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


@router.delete("/tokens")
async def logout_user(
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> None:
    await service.expire_refresh_token(refresh_token["id"])

    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
    )
