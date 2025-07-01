import streamlit as st

from api.ml import get_mlmodels_configs
from domain.ml import MLModelConfig
from states.ml import get_mlmodels_state, set_mlmodels_state


def render() -> list[MLModelConfig]:
    state = get_mlmodels_state()
    with st.spinner("Cargando modelos..."):
        mlmodels_fetched = get_mlmodels_configs()
        state.update_mlmodels_configs(mlmodels_fetched)
        set_mlmodels_state(state)


    mlmodels_all = state.get_mlmodels_configs()
    
    return mlmodels_all
