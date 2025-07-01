from fastapi import APIRouter, HTTPException, status

from entities.mlrunners import MLRunnerConfig, MLRunnerState
from services import models_service, runners_service


router = APIRouter()


@router.get("/",
        summary="",
        tags=["runners"])
async def get_runners():
    return runners_service.get_runners_configs()


@router.post("/refresh",
        summary="",
        tags=["runners"])
async def refresh_runners_states() -> list[MLRunnerConfig]:
    return runners_service.refresh_runners_states()
