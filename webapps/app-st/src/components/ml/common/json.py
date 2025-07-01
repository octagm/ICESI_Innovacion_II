import json

import streamlit as st

from api.dto import PredictRequest, PredictResponse
from api.ml import get_mlservice_config, request_external_mlservice, request_mlmodel
from domain.ml import MLSelectionMode
from states.ml import (
    get_mlmodel_config_mode_state_kv,
    get_mlmodel_id_state_kv,
    get_mlmodel_service_url_state_kv,
    get_mlrequest_body_sample_from_current_model_id,
)


def request_external() -> dict | None:
    (_, service_url) = get_mlmodel_service_url_state_kv()
    try:
        response = request_external_mlservice(service_url, json=request_body, timeout=10)
    except RuntimeError as e:
        st.error(f"icesi:{model_name}:request_external {e}")
        return None

    return response


def request_managed(model_name, request: PredictRequest) -> PredictResponse |  None:
    (_, mlmodel_id) = get_mlmodel_id_state_kv()
    try:
        response = request_mlmodel(mlmodel_id, request)
    except RuntimeError as e:
        st.error(f"icesi:{model_name}:request_managed {e}")
        return None

    return response


def _render_json_text_area() -> str:
    value = "{}"

    (_, config_mode) = get_mlmodel_config_mode_state_kv()
    if config_mode == MLSelectionMode.MANAGED.value:
        sample = get_mlrequest_body_sample_from_current_model_id()
        if sample:
            value = sample
    elif config_mode == MLSelectionMode.EXTERNAL.value:
        pass
        # TODO update external service request body sample
        # svc = get_mlservice_config(model_name)
        # if len(svc.request_body_samples) == 0:
        #     value = "{}"
        # else:
        #     value = svc.request_body_samples[0]
    else:
        st.error(f"{model_name}::json:value valor no soportado: MLSelectionMode={config_mode}")
        return

    st.subheader("Solicitud JSON")
    return st.text_area("Defina su solicitud JSON:", height=200, value=value)


@st.fragment
def render(model_name):
    input_json_text = _render_json_text_area()
    response = None
    if st.button("Ejecutar"):
        # validar correcta sintaxis del JSON
        try:
            request_kwargs = json.loads(input_json_text)
            request = PredictRequest(**request_kwargs)
        except json.JSONDecodeError:
            st.error(f"{model_name}:input:json JSON inválido")
            return

        (_, config_mode) = get_mlmodel_config_mode_state_kv()
        if config_mode == MLSelectionMode.EXTERNAL.value:
            response = request_external(model_name, request)
        elif config_mode == MLSelectionMode.MANAGED.value:
            response = request_managed(model_name, request)
        else:
            st.error(f"{model_name}:request valor no soportado: MLSelectionMode={config_mode}")
            return

    if response is None:
        return

    st.subheader("Respuesta JSON")
    st.json(response)
