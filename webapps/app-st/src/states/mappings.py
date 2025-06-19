"""
Mapeos de llaves de estados de la aplicación en `st.session_state`
"""

from typing import Any

import streamlit as st
from pydantic import BaseModel

from states import AuthState


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

    def get_default_state_values(self):
        return {
            "auth": AuthState()
        }


def map_session_state(sm: StateMap):
    defaults: dict[str, Any] = sm.get_default_state_values()
    for field, mapping in sm:
        print(f"field={field}, mapping={mapping}")
        if isinstance(mapping, StateMap):
            map_session_state(mapping)
        elif field in defaults:
            st.session_state[mapping] = defaults[field]
