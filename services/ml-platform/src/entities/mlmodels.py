from pydantic import BaseModel


class MLContainerConfig(BaseModel):
    envs: dict[str, str] | None = None  # variables de ambiente; opcional
    image: str | None  # imagen del contenedor ML; requerido
    ports: list[int]  # puertos expuestos por el contenedor; requerido con al menos 1 puerto
    remove: bool = True  # eliminar el contenedor automáticamente después de detenerlo
    volumes: list[str] | None = None  # volúmenes para el contenedor; opcional; 


class MLModelRunningState(BaseModel):
    errors: list[str] | None = None  # errores de estado de ejecución; opcional
    hosts: list[str] | None = None  # hosts creados si está en ejecución; opcional
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
