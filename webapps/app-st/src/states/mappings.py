"""
Mapeos de llaves de estados de la aplicación en `st.session_state`
"""

from typing import Callable, Any

import streamlit as st
from pydantic import BaseModel

from states import AuthState, MLModelsState, MLRunnersState


class StateMap(BaseModel):
    def get_default_state_values(self)-> dict[str, Any]:
        raise NotImplementedError()


class MLModelSelectionMap(StateMap):
    mlmodel_type: str = "interaction.mlmodel_selection.mlmodel_type"
    mlservice_url: str = "interaction.mlmodel_selection.mlservice_url"

    def get_default_state_values(self):
        return {
            "mlmodel_type": "",
            "mlservice_url": ""
        }


class AppMap(StateMap):
    auth: str = "auth"
    interaction_mlmodel_selection: MLModelSelectionMap = MLModelSelectionMap()
    mlmodels: str = "mlmodels"
    mlrunners: str = "mlrunners"

    def get_default_state_values(self):
        return {
            "auth": AuthState().model_dump(),
            "mlmodels": MLModelsState().model_dump(),
            "mlrunners": MLRunnersState().model_dump(),
        }



def _map_session_state(sm: StateMap):
    defaults: dict[str, Any] = sm.get_default_state_values()
    for field, mapping in sm:
        if isinstance(mapping, StateMap):
            _map_session_state(mapping)
        elif field in defaults:
            st.session_state[mapping] = defaults[field]


@st.cache_data
def get_app_state_mapping() -> AppMap:
    return AppMap()


def init_app_state_mapping(fn: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if 'app' not in st.session_state:
            _map_session_state(get_app_state_mapping())
            st.session_state['app'] = True

        return fn(*args, **kwargs)

    return wrapper

