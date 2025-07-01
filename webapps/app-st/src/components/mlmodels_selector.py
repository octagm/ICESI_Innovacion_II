import streamlit as st

from api.ml import get_mlservices_config_map
from components.api.request_mlmodels_configs import render as request_mlmodels_configs
from domain.ml import MLSelectionMode, MLServiceConfig
from states.ml import (
    get_mlmodel_id_state_kv,
    get_mlmodel_config_mode_state_kv,
    get_mlmodel_type_state_kv,
    get_mlmodel_service_url_state_kv,
)


def on_external_selectbox():
    next_service_url = ""

    services = get_mlservices_config_map()
    (_, mtype) = get_mlmodel_type_state_kv()
    if mtype in services and services[mtype].service_url:
        next_service_url = services[mtype].service_url

    (skey, _) = get_mlmodel_service_url_state_kv()
    st.session_state[skey] = next_service_url


def render_external():
    services = get_mlservices_config_map()
    (skey, _) = get_mlmodel_type_state_kv()
    st.selectbox('Seleccione el tipo de modelo:', services.keys(), key=skey, on_change=on_external_selectbox)
    st.text_input("Ingrese la URL del modelo",  key=skey)


def render_managed():
    models_configs = request_mlmodels_configs()

    (skey, _) = get_mlmodel_type_state_kv()
    mlmodels_names = sorted(set([m.name for m in models_configs]))
    mlmodel_name = st.selectbox('Seleccione el nombre del modelo:', mlmodels_names, key=skey)
    if mlmodel_name is None:
        ids = []
        disabled = True
    else:
        ids = [m.id for m in models_configs if m.name == mlmodel_name]
        disabled = len(ids) == 0

    (skey, _) = get_mlmodel_id_state_kv()
    st.selectbox('Seleccione la versión del modelo:', ids, disabled=disabled, key=skey)


def render():
    (skey, _) = get_mlmodel_config_mode_state_kv()
    values = [MLSelectionMode.MANAGED.value, MLSelectionMode.EXTERNAL.value]
    config_mode = st.radio("Tipo de configuración:", values, index=0, key=skey)
    if config_mode is None:
        pass
    elif config_mode == MLSelectionMode.EXTERNAL.value:
        render_external()
    elif config_mode == MLSelectionMode.MANAGED.value:
        render_managed()
    else:
        st.error(f"selector: valor no soportado: MLSelectionMode={config_mode}")
