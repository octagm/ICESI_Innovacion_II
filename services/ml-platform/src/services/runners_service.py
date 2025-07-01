import logging
import os

from datetime import datetime
from typing import Any, List

from config import settings
from dependencies.runners import BaseRunner, DockerRunner
from entities.mlmodels import MLModelConfig, MLModelRunningState
from entities.mlrunners import MLRunnerConfig, MLRunnerState


logger = logging.getLogger(__name__)


class RunnersService:
    # TODO: connect to database instead of hard-coding configs map
    configs = {}
    runners = {}


    def connect_from_env(self) -> List[str]:
        """
        Connects to the runners using environment variables.
        """

        if settings["runners"]["docker"]["enabled"]:
            runner_id = "docker"
            self.runners[runner_id] = DockerRunner()
            state = self.runners[runner_id].connect()

            self.configs[runner_id] = MLRunnerConfig(
                id=runner_id,
                state=state,
                type="docker",
            )


    def get_runner(self, runner_id: str, raise_error_if_none=False) -> BaseRunner:
        runner = self.runners.get(runner_id)
        if raise_error_if_none and not runner:
            raise ValueError(f"Runner ID '{runner_id}' is not configured.")

        return runner


    def get_runners_configs(self) -> List[MLRunnerConfig]:
        """
        Retrieves the configurations of all runners.
        Returns a list of MLRunnerConfig objects.
        """
        return list(self.configs.values())


    def refresh_runners_states(self) -> List[MLRunnerConfig]:
        for runner_id, runner in self.runners.items():
            if runner_id not in self.configs:
                raise ValueError(f"Inconsistent state: runner_id='{runner_id}' is not configured.")

            self.configs[runner_id].state = runner.refresh_state()

        return self.get_runners_configs()


    def run_model(self, mlmodel: MLModelConfig) -> MLModelConfig:
        if mlmodel.container_config is None:
            raise ValueError("Unsupported mlmodel config missing container config.")

        runner = self.get_runner(mlmodel.runner_id, raise_error_if_none=True)
        state = runner.run_container(mlmodel)       
        if state is None:
            raise RuntimeError(f"Failed to run model '{mlmodel.id}' using runner '{mlmodel.runner_id}'.")

        # TODO update database with the new state
        mlmodel.state = state

        return mlmodel


    def stop_model(self, mlmodel: MLModelConfig) -> MLModelConfig:
        runner = self.get_runner(mlmodel.runner_id, raise_error_if_none=True)
        state = runner.stop_container(mlmodel)       
        if state is None:
            raise RuntimeError(f"Failed to run model '{mlmodel.id}' using runner '{mlmodel.runner_id}'.")

        # TODO update database with the new state
        mlmodel.state = state

        return mlmodel
