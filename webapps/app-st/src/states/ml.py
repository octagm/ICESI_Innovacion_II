import streamlit as st

from states.app import get_app_state_mapping


def get_mlmodel_service_url_state_kv() -> tuple[str, str]:
    asm = get_app_state_mapping()
    key = asm.interaction_mlmodel_selection.mlservice_url
    value = st.session_state[key]
    return (key, value)


def get_mlmodel_type_state_kv() -> tuple[str, str]:
    asm = get_app_state_mapping()
    key = asm.interaction_mlmodel_selection.mlmodel_type
    value = st.session_state[key]
    return (key, value)

