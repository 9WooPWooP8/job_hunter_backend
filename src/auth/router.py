from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response
from fastapi_restful.cbv import cbv

import src.auth.service as auth_service
from src.auth import jwt, utils
from src.auth.dependencies import valid_refresh_token, valid_refresh_token_user
from src.auth.exceptions import ApplicantNotExists, RecruiterNotExists
from src.auth.models import AuthRefreshToken
from src.auth.schemas import AuthData, AuthTokens

router = APIRouter(prefix="/auth", tags=["auth"])


@cbv(router)
class AuthCBV:
    _auth_service: auth_service.AuthService = Depends(auth_service.get_auth_service)

    @router.post("/tokens/recruiters", response_model=AuthTokens)
    async def auth_recruiter(
        self, auth_data: AuthData, response: Response
    ) -> AuthTokens:
        recruiter = await self._auth_service.authenticate_recruiter(
            auth_data.username, auth_data.password
        )

        if not recruiter:
            raise RecruiterNotExists

        refresh_token_value = await self._auth_service.create_refresh_token(
            user_id=recruiter.user_id
        )
        access_token = jwt.create_access_token(user=recruiter.user)

        response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

        return AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token_value,
        )

    @router.post("/tokens/applicants", response_model=AuthTokens)
    async def auth_applicant(
        self, auth_data: AuthData, response: Response
    ) -> AuthTokens:
        applicant = await self._auth_service.authenticate_applicant(
            auth_data.username, auth_data.password
        )

        if not applicant:
            raise ApplicantNotExists

        refresh_token_value = await self._auth_service.create_refresh_token(
            user_id=applicant.user_id
        )
        access_token = jwt.create_access_token(user=applicant.user)

        response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

        return AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token_value,
        )

    @router.put("/tokens", response_model=AuthTokens)
    async def refresh_tokens(
        self,
        worker: BackgroundTasks,
        response: Response,
        refresh_token: dict[str, Any] = Depends(valid_refresh_token),
        user: dict[str, Any] = Depends(valid_refresh_token_user),
    ) -> AuthTokens:
        refresh_token_value = await self._auth_service.create_refresh_token(
            user_id=refresh_token.user_id
        )
        response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

        worker.add_task(self._auth_service.expire_refresh_token, refresh_token.id)

        access_token = jwt.create_access_token(user=user)

        return AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token_value,
        )

    @router.delete("/tokens")
    async def logout_user(
        self,
        response: Response,
        refresh_token: AuthRefreshToken = Depends(valid_refresh_token),
    ) -> None:
        await self._auth_service.expire_refresh_token(refresh_token.id)

        response.delete_cookie(
            **utils.get_refresh_token_settings(
                refresh_token.refresh_token, expired=True
            )
        )
