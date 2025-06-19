import streamlit as st

from api.entities import MLServiceConfig
from api.ml import get_mlservices_config_map
from states.ml import get_mlmodel_type_state_kv, get_mlmodel_service_url_state_kv


def on_selectbox():
    next_service_url = ""

    services = get_mlservices_config_map()
    (_, mtype) = get_mlmodel_type_state_kv()
    if mtype in services and services[mtype].service_url:
        next_service_url = services[mtype].service_url
    
    (skey, _) = get_mlmodel_service_url_state_kv()
    st.session_state[skey] = next_service_url


def render():
    services = get_mlservices_config_map()
    (skey, _) = get_mlmodel_type_state_kv()
    st.selectbox('Seleccione el tipo de modelo:', services.keys(), key=skey, on_change=on_selectbox)

    config_type = st.radio("Tipo de configuración:", ["manejada", "URL externa"], index=0)

    if config_type is None:
        return
    elif config_type == "manejada":
        st.success("manejada")
    else:
        (skey, url) = get_mlmodel_service_url_state_kv()
        st.text_input("Ingrese la URL del modelo",  key=skey)
