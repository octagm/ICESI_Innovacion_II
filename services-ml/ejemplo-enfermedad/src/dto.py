""" List of DTOs (Data Transfer Objects)"""

from pydantic import BaseModel


class PredictInstance(BaseModel):
    blood_pressure: int
    heart_rate: int
    temperature: float


class PredictBatchRequest(BaseModel):
    instances: list[PredictInstance]


class PredictBatchResponse(BaseModel):
    predictions: list[str]
