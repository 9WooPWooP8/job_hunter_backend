from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

import src.rates.service as rate_service
from src.rates.schemas import RatesResponse

router = APIRouter(prefix="/rates", tags=["rates"])


@cbv(router)
class RatesCBV:
    _rate_service: rate_service.RatesService = Depends(
        rate_service.get_rates_service
    )

    @router.get("/", response_model=list[RatesResponse])
    async def get_all(self) -> list[RatesResponse]:
        return await self._rate_service.get_all()
