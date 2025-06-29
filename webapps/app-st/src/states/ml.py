import streamlit as st

from states import MLModelsState, MLRunnersState
from states.mappings import get_app_state_mapping


def get_mlmodels_state() -> MLModelsState:
    asm = get_app_state_mapping()
    value = st.session_state[asm.mlmodels]
    return MLModelsState(**value)


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


def get_mlrunners_state() -> MLRunnersState:
    asm = get_app_state_mapping()
    value = st.session_state[asm.mlrunners]
    return MLRunnersState(**value)


def set_mlmodels_state(state: MLModelsState):
    asm = get_app_state_mapping()
    st.session_state[asm.mlmodels] = state.model_dump()


def set_mlrunners_state(state: MLRunnersState):
    asm = get_app_state_mapping()
    st.session_state[asm.mlrunners] = state.model_dump()
