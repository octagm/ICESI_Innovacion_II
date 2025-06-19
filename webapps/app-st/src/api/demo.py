import os
from datetime import datetime

import streamlit as st

from api.entities import (
    AppConfig,
    MLContainerConfig,
    MLModelConfig,
    MLModelRunningState,
    MLRunnerConfig,
    MLRunnerState,
    MLServiceConfig,
)



@st.cache_data
def _get_app_config() -> AppConfig:
    mlservices = {
        "iris": MLServiceConfig(
            id="iris",
            request_body_samples=[
                '{"instances": [[1, 2, 3, 4], [1, 2, 3, 4]]}'
            ],
            service_url=os.environ.get("ML_IRIS_SERVICE_URL")
        ),
        "mnist": MLServiceConfig(id="mnist", service_url=os.environ.get("ML_MNIST_SERVICE_URL")),
        "tiempo_clima": MLServiceConfig(id="tiempo_clima"),
        "imagenes_satelitales": MLServiceConfig(id="imagenes_satelitales"),
    }

    mlmodels_configs = {
        "iris": MLModelConfig(
            id="iris",
            name="Iris Model",
            runner_id="docker",
            version="",
            container_config=MLContainerConfig(
                envs={
                    "GREETING": "hellooo"
                },
                image="ml-iris:latest",
                ports=[8000],
            ),
            state=MLModelRunningState(
                last_updated=datetime.now().isoformat(),
                status="running",
            ),
        ),
    }

    runners = {
        "docker": MLRunnerConfig(
            id="docker",
            state=MLRunnerState(
                connected=True,
                last_updated=datetime.now().isoformat(),
            ),
            type="docker",
        ), 
        "docker_1": MLRunnerConfig(
            id="docker_1",
            connection="https://external",
            state=MLRunnerState(
                connected=False,
                last_updated=datetime.now().isoformat(),
            ),
            type="docker",
        ), 
    }
    
    return AppConfig(
        mlmodels_configs=mlmodels_configs,
        mlservices=mlservices,
        runners=runners,
    )


def get_demo_mlservices_config_map() -> dict[str, MLServiceConfig]:
    return _get_app_config().mlservices


def get_demo_mlservice_config(service_id: str) -> MLServiceConfig:
    svcs = _get_app_config().mlservices
    if service_id not in svcs:
        raise RuntimeError(f'icesi: app config missing service config for id="{service_id}"')

    return svcs[service_id]


def get_demo_mlmodels_configs_map() -> dict[str, MLRunnerConfig]:
    return _get_app_config().mlmodels_configs


def get_demo_runners_configs_map() -> dict[str, MLRunnerConfig]:
    return _get_app_config().runners
