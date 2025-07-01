from entities.mlmodels import MLModelConfig, MLModelRunningState
from entities.mlrunners import MLRunnerState


class BaseRunner():
    state: MLRunnerState | None = None

    def refresh_state(self) -> str:
        """
        Returns the status of the runner.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class MLModelContainerMap:
    # TODO query database instead of using _map dict
    _map: dict[str, str] = {}    

    def add_entry(self, mlmodel_id: str, container_id: str) -> None:
        self._map[mlmodel_id] = container_id

    def get_container_by_mlmodel(self, mlmodel_id: str) -> str:
        return self._map.get(mlmodel_id)

    def remove_entry(self, mlmodel_id) -> None:
        del self._map[mlmodel_id]


class ContainerRunner(BaseRunner):
    mlmodels_containers_map: MLModelContainerMap

    def __init__(self):
        self.mlmodels_containers_map = MLModelContainerMap()

    def run_container(self, config: MLModelConfig) -> MLModelRunningState:
        raise NotImplementedError("Subclasses must implement this method.")

    def stop_container(self, config: MLModelConfig) -> MLModelRunningState:
        raise NotImplementedError("Subclasses must implement this method.")

    def validate_image_access(self, image_name: str) -> None:
        raise NotImplementedError("Subclasses must implement this method.")
