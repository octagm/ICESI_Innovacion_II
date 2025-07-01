import logging
import os

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from config import MLMODEL_URI
from entities import PredictRequest, PredictResponse
from mlmodel_service import MLModelService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Iris AI/ML model",
    version="1.0.0"
)
mlmodel_service = MLModelService()


@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando servicio Iris AI/ML...")
    mlmodel_service.load_model(MLMODEL_URI)


@app.get("/_health", tags=["healthcheck"])
def check_health():
    return {"status": "ok", "message": "API is healthy"}


@app.get("/_ready", tags=["healthcheck"])
def check_ready():
    if mlmodel_service.is_model_loaded():
        return {"status": "ok", "message": "API is ready"}
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded yet"
        )


@app.post("/predict", tags=["inference"])
def predict(input_request: PredictRequest) -> PredictResponse:
    try:
        return mlmodel_service.predict(input_request).dict()
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during prediction"
        )
