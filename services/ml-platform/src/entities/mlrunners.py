from pydantic import BaseModel


class MLRunnerState(BaseModel):
    connected: bool = False
    errors: list[str] | None = None  #  errores de estado de ejecución; opcional
    last_updated: str  # fecha en formato ISO


class MLRunnerConfig(BaseModel):
    id: str
    connection: str | None = None  # URI de conexión; si es None o str vacío entonces el controlador de ejecutor intentará conexión por defecto
    state: MLRunnerState | None = None
    type: str  # "docker", "kubernetes", "kserve"
