from pydantic import BaseModel

from domain.ml import (
    MLModelConfig,
    MLRunnerConfig,
)
from domain.user import User


class AuthState(BaseModel):
    is_authenticated: bool = False
    jwt: str | None = None
    user: User | None = None


class MLModelsState(BaseModel):
    configs: dict[str, MLModelConfig] = {}

    def get_mlmodel_config(self, mlmodel_id: str) -> MLModelConfig:
        return self.configs.get(mlmodel_id)

    def get_mlmodels_configs(self) -> list[MLModelConfig]:
        return list(self.configs.values())

    def update_mlmodels_configs(self, mlmodels_configs: list[MLModelConfig]):
        for mlmodel in mlmodels_configs:
            self.configs[mlmodel.id] = mlmodel


class MLRunnersState(BaseModel):
    configs: dict[str, MLRunnerConfig] = {}

    def get_mlrunner_config(self, mlrunner_id: str) -> MLRunnerConfig:
        return self.configs.get(mlrunner_id)

    def get_mlrunners_configs(self) -> list[MLRunnerConfig]:
        return list(self.configs.values())

    def update_mlrunners_configs(self, mlrunners_configs: list[MLRunnerConfig]):
        for mlrunner in mlrunners_configs:
            self.configs[mlrunner.id] = mlrunner
