import logging

from fastapi import APIRouter, HTTPException, Request, status

from entities.mlmodels import MLModelConfig, MLModelRunningState
from entities.requests import PredictRequest
from entities.responses import PredictResponse
from exceptions.container import ContainerImageNotAccessible
from services import models_service, runners_service


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/",
        summary="Get an AI/ML models by criteria",
        tags=["models"])
async def get_models_by_criteria() -> list[MLModelConfig]:
    configs = models_service.get_models_by_criteria()
    return [config.dict() for config in configs]


@router.post("/",
        summary="Create an AI/ML Model configuration",
        tags=["models"])
async def create_model_config(model_id: str, config: MLModelConfig) -> MLModelConfig:
    pass


@router.get("/{model_id}",
        summary="Get an AI/ML model configuration",
        tags=["models"])
async def get_model_config(model_id: str) -> MLModelConfig:
    config = models_service.get_model_config(model_id)
    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{model_id}' not found."
        )

    return config.dict()


@router.get("/{model_id}/predict",
        summary="Invoke a deployed AI/ML model",
        tags=["inference", "models"])
@router.post("/{model_id}/predict",
        summary="Invoke a deployed AI/ML model",
        tags=["inference", "models"])
async def predict(model_id: str, request: Request, payload: PredictRequest | None = None) -> PredictResponse:

    # payload = request_data.dict(exclude_none=True) # Send only provided fields
    # payload = request_data  # Assuming request_data is already a dict

    query = dict(request.query_params)
    
    try:
        return await models_service.predict(model_id, payload, query)
    except ValueError as e:
        logger.error(f"Error predicting with model '{model_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"An unexpected error occurred while invoking model '{model_id}'.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post("/{model_id}/run",
        summary="Deploy an AI/ML model configuration",
        tags=["deployments", "models"])
async def run_model(model_id: str) -> MLModelConfig:
    config = models_service.get_model_config(model_id)

    # DEMO MOCK
    # config.state = MLModelRunningState(
    #     last_updated="2023-10-01T00:00:00Z",
    #     status="running",
    # )
    # return config

    try:
        return runners_service.run_model(config).dict()
    except (ValueError, ContainerImageNotAccessible) as e:
        logger.error(f"Error running model '{model_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        logger.error(f"Runtime error while running model '{model_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/{model_id}/stop",
        summary="Stop an AI/ML model",
        tags=["deployments", "models"])
async def stop_model(model_id: str) -> MLModelConfig:
    config = models_service.get_model_config(model_id)

    # DEMO MOCK
    # config.state = MLModelRunningState(
    #     last_updated="2023-10-01T00:00:00Z",
    #     status="stopped",
    # )
    # return config

    try:
        return runners_service.stop_model(config).dict()
    except (ValueError, ContainerImageNotAccessible) as e:
        logger.error(f"Error running model '{model_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        logger.error(f"Runtime error while running model '{model_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
