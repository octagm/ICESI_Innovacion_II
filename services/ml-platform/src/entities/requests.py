from typing import Any

from pydantic import BaseModel


class PredictRequest(BaseModel):
    config: dict | None = None
    instances: list[Any] | None = None
