import json
import logging

import httpx

import api.demo as demo
from api.dto import PredictRequest, PredictResponse
from config import API_URL, WEBAPP_DEMO_MOCK
from domain.ml import MLModelConfig, MLServiceConfig, MLRunnerConfig


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def get_mlmodels_configs() -> list[MLModelConfig]:
    if WEBAPP_DEMO_MOCK:
        return demo.get_demo_mlmodels_configs_map().values()

    url = API_URL + "/models/"
    try:
        response = httpx.get(url).json()
    except json.JSONDecodeError as ex:
        raise RuntimeError("icesi: invalid JSON in response body", ex)
    except httpx.RequestError as ex:
        raise RuntimeError(f"icesi: HTTP request failed", ex)
    
    mlmodels = [MLModelConfig(**mlmodel) for mlmodel in response]
    return mlmodels


def get_runners_configs() -> list[MLRunnerConfig]:
    if WEBAPP_DEMO_MOCK:
        return demo.get_demo_runners_configs_map().values()

    url = API_URL + "/runners/"
    try:
        response = httpx.get(url).json()
    except json.JSONDecodeError as ex:
        raise RuntimeError("icesi: invalid JSON in response body", ex)
    except httpx.RequestError as ex:
        raise RuntimeError(f"icesi: HTTP request failed", ex)
    
    runners = [MLRunnerConfig(**runner) for runner in response]
    return runners


def run_mlmodel(mlmodel_id: str) -> MLModelConfig:
    # TODO support WEBAPP_DEMO_MOCK

    url = API_URL + "/models/" + mlmodel_id + "/run"
    try:
        response = httpx.post(url)
        response.raise_for_status()
        response_body = response.json()
        mlmodel = MLModelConfig(**response_body)
    except json.JSONDecodeError as ex:
        raise RuntimeError("icesi: invalid JSON in response body", ex)
    except (httpx.HTTPStatusError, httpx.RequestError) as ex:
        raise RuntimeError("icesi: request error", ex)
    except Exception as ex:
        logger.error(f"icesi: exception: {ex}", exc_info=True)
        logger.error(ex, exc_info=True)
        raise Exception("icesi: exception", ex)

    return mlmodel


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


def request_mlmodel(mlmodel_id, request: PredictRequest, resource_path="/predict", **kwargs) -> PredictResponse:
    url = API_URL + "/models/" + mlmodel_id + "/predict"
    try:
        response_body = (
            httpx.post(url, json=request.dict(), timeout=20, **kwargs)
            .raise_for_status()
            .json()
        )
        # response_http = httpx.post(url, json=request.dict(), timeout=20, **kwargs)
        # response_http.raise_for_status()
        # response_body = response_http.json()
        response = PredictResponse(**response_body)
    except json.JSONDecodeError as ex:
        raise RuntimeError("icesi: managed: invalid JSON in response body", ex)
    except httpx.HTTPStatusError as ex:
        try:
            detail = ex.response.json().get("detail")
        except json.JSONDecodeError:
            detail = ex.response.text
        raise RuntimeError(f"icesi:managed: request status error: detail: {detail}", ex)
    except httpx.RequestError as ex:
        raise RuntimeError(f"icesi:managed: request error: {ex}", ex)
    except Exception as ex:
        logger.error(f"icesi:managed: exception: {ex}", exc_info=True)
        raise Exception("icesi:managed: exception", ex)

    return response


def stop_mlmodel(mlmodel_id: str) -> MLModelConfig:
    # TODO support WEBAPP_DEMO_MOCK
    
    url = API_URL + "/models/" + mlmodel_id + "/stop"
    try:
        response = httpx.post(url, timeout=20)
        response.raise_for_status()
        response_body = response.json()
        mlmodel = MLModelConfig(**response_body)
    except json.JSONDecodeError as ex:
        raise RuntimeError("icesi: invalid JSON in response body", ex)
    except (httpx.HTTPStatusError, httpx.RequestError) as ex:
        raise RuntimeError("icesi: request error", ex)
    except Exception as ex:
        logger.error(f"icesi: exception: {ex}", exc_info=True)
        logger.error(ex, exc_info=True)
        raise Exception("icesi: exception", ex)

    return mlmodel
