from typing import Union

from fastapi import FastAPI, Query

from dto import PredictBatchRequest, PredictBatchResponse, PredictInstance
from model import ModelService


app = FastAPI()
model_service = ModelService()


@app.on_event("startup")
async def startup_event():
    model_service.load_model()


@app.get("/_health")
def check_health():
    return {"status": "ok", "message": "API is healthy"}


@app.post("/predict", description="Predicción de múltiples instancias")
def predict_batch(request: PredictBatchRequest) -> PredictBatchResponse:
    predictions = model_service.predict(request.instances)
    return PredictBatchResponse(predictions=predictions)


@app.get("/predict", description="Predicción de una única instancia a través de query params")
def predict_item(
    blood_pressure: int = Query(..., description="Presión arterial"),
    heart_rate: int = Query(..., description="Ritmo cardiaco"),
    temperature: float = Query(..., description="Temperatura"),
) -> PredictBatchResponse:
    instance = PredictInstance(blood_pressure=blood_pressure, heart_rate=heart_rate, temperature=temperature)
    predictions = model_service.predict([instance])
    return PredictBatchResponse(predictions=predictions)
