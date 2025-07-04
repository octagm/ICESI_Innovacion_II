from enum import Enum

from pydantic import BaseModel


class MLSelectionMode(Enum):
    EXTERNAL = "URL externa"
    MANAGED = "manejada"


class MLServiceConfig(BaseModel):
    id: str
    request_body_samples: list[str] = []
    service_url: str | None = None


class MLContainerConfig(BaseModel):
    envs: dict[str, str] | None = None  # variables de ambiente; opcional
    image: str | None  # imagen del contenedor ML; requerido
    ports: list[int]  # puertos expuestos por el contenedor; requerido con al menos 1 puerto
    volumes: list[str] | None = None  # volúmenes para el contenedor; opcional; 


class MLModelRunningState(BaseModel):
    endpoints: list[str] | None = None  # endpoints creados si está en ejecución; opcional
    errors: list[str] | None = None  # errores de estado de ejecución; opcional
    last_updated: str  # fecha en formato ISO
    runner_metadata: dict | None = None  # metadata del ejecutor; opcional
    status: str = "unknown"  # "running", "stopped", "unknown"


class MLRequestConfig(BaseModel):
    body_sample: str | None = None  # ejemplo muestra del cuerpo de solicitud soportado
    body_uses_request_model: bool = False  # si la solicitud sigue el modelo PredictRequest={config: dict, instances: list[Any] | None}


class MLModelConfig(BaseModel):
    container_config: MLContainerConfig
    id: str
    name: str
    runner_id: str
    request_config: MLRequestConfig
    state: MLModelRunningState
    version: str


class MLRunnerState(BaseModel):
    connected: bool = False
    errors: list[str] | None = None  # errores de estado de ejecución; opcional
    last_updated: str  # fecha en formato ISO


class MLRunnerConfig(BaseModel):
    id: str
    connection: str | None = None  # URI de conexión; si es None o str vacío entonces el controlador de ejecutor intentará conexión por defecto
    state: MLRunnerState | None = None
    type: str  # "docker", "kubernetes", "kserve"
