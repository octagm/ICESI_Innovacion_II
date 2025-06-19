from pydantic import BaseModel


class MLServiceConfig(BaseModel):
    id: str
    request_body_samples: list[str] = []
    service_url: str | None = None


class MLContainerConfig(BaseModel):
    envs: dict[str, str] | None = None  # Environment variables for the container, if applicable
    image: str | None = None  # Container image for the model, if applicable
    ports: list[int] | None = None  # Ports exposed by the container, if applicable


class MLModelRunningState(BaseModel):
    endpoints: list[str] | None = None  # Endpoints for the model, if applicable
    error_message: str | None = None  # Optional error message if the model is unavailable
    last_updated: str  # ISO format datetime string
    runner_metadata: dict | None = None  # Metadata about the runner, if applicable
    status: str = "unknown"  # "running", "stopped", "unknown"


class MLModelConfig(BaseModel):
    container_config: MLContainerConfig | None = None  # Container image for the model, if applicable
    id: str
    name: str
    runner_id: str
    state: MLModelRunningState
    version: str


class MLRunnerState(BaseModel):
    connected: bool = False
    error_message: str | None = None  # Optional error message if the model is unavailable
    last_updated: str  # ISO format datetime string


class MLRunnerConfig(BaseModel):
    id: str
    connection: str | None = None
    state: MLRunnerState | None = None
    type: str  # e.g., "docker", "kubernetes", etc.


class AppConfig(BaseModel):
    mlmodels_configs: dict[str, MLModelConfig]
    mlservices: dict[str, MLServiceConfig]
    runners: dict[str, MLRunnerConfig]
