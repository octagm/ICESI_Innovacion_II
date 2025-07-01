import streamlit as st

from states import MLModelsState, MLRunnersState
from states.mappings import get_app_state_mapping


def get_mlmodels_state() -> MLModelsState:
    asm = get_app_state_mapping()
    value = st.session_state[asm.mlmodels]
    return MLModelsState(**value)


def get_mlmodel_config_mode_state_kv() -> tuple[str, str]:
    asm = get_app_state_mapping()
    key = asm.interaction_mlmodel_selection.mlmodel_config_mode
    value = st.session_state[key]
    return (key, value)


def get_mlmodel_id_state_kv() -> tuple[str, str]:
    asm = get_app_state_mapping()
    key = asm.interaction_mlmodel_selection.mlmodel_id
    value = st.session_state[key]
    return (key, value)


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


def get_mlrequest_body_sample_from_current_model_id() -> str | None:
    (_, mlmodel_id) = get_mlmodel_id_state_kv()
    mlmodels = get_mlmodels_state()
    mlmodel = mlmodels.get_mlmodel_config(mlmodel_id)
    if mlmodel is None:
        return None
    
    return mlmodel.request_config.body_sample


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
