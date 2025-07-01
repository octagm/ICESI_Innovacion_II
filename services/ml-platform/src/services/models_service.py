import json
import logging
from typing import Any

import httpx

from fastapi import HTTPException, status

from entities.mlmodels import MLContainerConfig, MLModelConfig, MLModelRunningState, MLRequestConfig
from entities.requests import PredictRequest
from entities.responses import PredictResponse


logger = logging.getLogger(__name__)


class MLModelsService:
    # TODO: connect to database instead of hard-coding configs map
    configs = {}

    def connect_from_env(self):
        mlmodel_id = "deteccion-lanchas:20250623"
        self.configs[mlmodel_id] = MLModelConfig(
            id=mlmodel_id,
            name="deteccion-lanchas",
            runner_id="docker",
            use_predict_request=False,
            version="20250623",
            container_config=MLContainerConfig(
                envs={
                    "STORAGE_DIR": "/storage"
                },
                image="deteccion-lanchas:20250623",
                ports=[8000, 8501],
                volumes=["/storage"],
            ),
            request_config=MLRequestConfig(
                body_uses_request_model=False,
            ),
            state=MLModelRunningState(
                last_updated="2025-06-23T00:00:00Z",
                status="stopped",
            ),
        )

        mlmodel_id = "ejemplo-enfermedad:v1"
        self.configs[mlmodel_id] = MLModelConfig(
            id=mlmodel_id,
            name="ejemplo-enfermedad",
            runner_id="docker",
            use_predict_request=True,
            version="v1",
            container_config=MLContainerConfig(
                envs={
                    "GREETING": "hellooo"
                },
                image="ml-ejemplo-enfermedad:v1",
                ports=[8000],
            ),
            request_config=MLRequestConfig(
                body_sample=json.dumps({
                    "instances": [
                        {"blood_pressure": 90, "heart_rate": 120, "temperature": 36},
                        {"blood_pressure": 90, "heart_rate": 120, "temperature": 38}
                    ]
                }),
                body_uses_request_model=True,
            ),
            state=MLModelRunningState(
                last_updated="2000-01-01T00:00:00Z",
                status="stopped",
            ),
        )

        mlmodel_id = "iris:v1"
        self.configs[mlmodel_id] = MLModelConfig(
            id=mlmodel_id,
            name="iris",
            runner_id="docker",
            version="v1",
            container_config=MLContainerConfig(
                envs={
                    "MLMODEL_URI": "/models/iris_logreg_v1.onnx",
                    "PORT": "80",
                },
                image="ml-ejemplo-iris:v1",
                ports=[80],
                volumes=["/models"],
            ),
            request_config=MLRequestConfig(
                body_sample=json.dumps({"instances": [[6.1, 2.8, 4.7, 1.2], [5.7, 3.8, 1.7, 0.3]]}),
                body_uses_request_model=True,
            ),
            state=MLModelRunningState(
                last_updated="2000-01-01T00:00:00Z",
                status="stopped",
            ),
        )

        mlmodel_id = "mnist:latest"
        self.configs[mlmodel_id] = MLModelConfig(
            id=mlmodel_id,
            name="mnist",
            runner_id="docker",
            version="latest",
            container_config=MLContainerConfig(
                image="mnist:latest",
                ports=[8000]
            ),
            request_config=MLRequestConfig(
                body_uses_request_model=False,
            ),
            state=MLModelRunningState(last_updated="2000-01-01T00:00:00Z", status="stopped"),
        )


    def get_models_by_criteria(self, criteria: dict = None) -> list[MLModelConfig]:
        """
        Retrieves models based on specified criteria.
        Returns a list of MLModelConfig objects that match the criteria.
        """

        # matching_models = []
        # for model_id, config in self.configs.items():
        #     if all(getattr(config, key) == value for key, value in criteria.items()):
        #         matching_models.append(config)
        # return matching_models

        return self.configs.values()


    def get_model_config(self, model_id: str) -> MLModelConfig:
        """
        Retrieves the configuration for a given model ID.
        Raises an HTTPException if the model ID is not found.
        """
        return self.configs.get(model_id)


    def get_model_running_valid_endpoint(self, model_id: str) -> str:
        """
        Retrieves the running endpoint for a given model ID.
        Raises an HTTPException if the model ID is not found.
        """
        config = self.get_model_config(model_id)
        if not config:
            raise ValueError(f"icesi: no se encontró modelo: model_id='{model_id}'")

        if config.state.status != "running":
            raise ValueError(f"icesi: modelo no está en ejecución: model_id='{model_id}'")

        if len(config.state.endpoints) == 0:
            raise ValueError(f"icesi: modelo no tiene endpoints configurados: model_id='{model_id}'")

        return config.state.endpoints[0]


    async def predict(self, model_id: str, payload: PredictRequest | None, query: dict | None) -> PredictResponse:
        model_url = self.get_model_running_valid_endpoint(model_id)

        if payload is None:
            pass
        else:
            payload = payload.model_dump()

        # elif payload.config is None and payload.instances is None:
        #     payload = None
        # elif payload.config is None:
        #     payload = payload.instances
        # elif payload.instances is None:
        #     payload = payload.config

        async with httpx.AsyncClient(timeout=60.0) as client: # Increased timeout for potentially long inferences
            try:
                response = await client.send(
                    httpx.Request(
                        method="POST" if payload is not None else "GET",
                        url=model_url,
                        json=payload,
                        params=query
                    )
                )
                response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
                body = response.json()
                predictions = body if isinstance(body, list) else [body]
                return PredictResponse(model_id=model_id, predictions=predictions)
   
            except httpx.ReadTimeout:
                err = f"icesi: request to model '{model_id}' timed out"
                logger.error(f"{err}")
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail=err
                )
            except httpx.ConnectError:
                err = f"icesi: could not connect to model '{model_id}' at {model_url}."
                logger.error(err)
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=err
                )
            except httpx.HTTPStatusError as e:
                err = response.json()
                logger.error(f"icesi: error in model service model_id='{model_id}' error_code={e.response.status_code} error: {err}")
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=err
                )
