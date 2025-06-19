import json

import httpx

import api.demo as demo
from api.entities import MLModelConfig, MLServiceConfig, MLRunnerConfig
from config import WEBAPP_DEMO_MOCK


def get_mlservices_config_map() -> dict[str, MLServiceConfig]:
    if WEBAPP_DEMO_MOCK:
        return demo.get_demo_mlservices_config_map()

    # llamar a API
    raise NotImplementedError()


def get_mlservice_config(service_id: str) -> MLServiceConfig:
    if WEBAPP_DEMO_MOCK:
        return demo.get_demo_mlservice_config(service_id)

    # llamar a API
    raise NotImplementedError()


def get_mlmodels_configs_map() -> dict[str, MLModelConfig]:
    if WEBAPP_DEMO_MOCK:
        return demo.get_demo_mlmodels_configs_map()

    # llamar a API
    raise NotImplementedError()

def get_runners_configs_map() -> dict[str, MLRunnerConfig]:
    if WEBAPP_DEMO_MOCK:
        return demo.get_demo_runners_configs_map()

    # llamar a API
    raise NotImplementedError()


def request_external_mlservice(service_url, resource_path="/predict", **kwargs) -> dict:
    if service_url.endswith("/"):
        service_url = service_url[:-1]

    if not service_url.endswith(resource_path):
        service_url = service_url + resource_path

    try:
        response = httpx.post(service_url, **kwargs).json()
    except json.JSONDecodeError as ex:
        raise RuntimeError("icesi: invalid JSON in response body", ex)
    except httpx.RequestError as ex:
        raise RuntimeError(f"icesi: HTTP request failed", ex)

    return response
