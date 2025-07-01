import logging

import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from entities.mlmodels import MLModelConfig, MLModelRunningState
from routers import models_router, runners_router
from services import models_service, runners_service


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="ml-platform",
    description="A FastAPI application to serve as an easy PaaS + Gateway to AI/ML models",
    version="1.0.0"
)
app.include_router(models_router, prefix="/models", tags=["models"])
app.include_router(runners_router, prefix="/runners", tags=["runners"])


@app.get("/_health")
def check_health():
    return {"status": "ok", "message": "API is healthy"}


@app.on_event("startup")
async def startup_event():
    logger.info("icesi: starting up...")

    models_service.connect_from_env()
    runners_service.connect_from_env()

    # TODO: validate mlmodels_containers_map from database
