from typing import Any

from pydantic import BaseModel


class PredictResponse(BaseModel):
    model_id: str
    metadata: dict[str, Any] = {}
    predictions: list[Any]
