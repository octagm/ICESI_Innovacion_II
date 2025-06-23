import pandas as pd
import streamlit as st

from api.ml import get_mlmodels_configs
from domain.ml import MLModelConfig
from states.ml import get_mlmodels_state, set_mlmodels_state


def map_to_record(mlmodel: MLModelConfig) -> dict:
    record = mlmodel.dict()

    return record


def render():
    st.header("Gestión de modelos")
    if st.button("Agregar modelo"):
        st.success("modelo creado")

    state = get_mlmodels_state()
    with st.spinner("Cargando modelos..."):
        mlmodels = get_mlmodels_configs()
        state.update_mlmodels_configs(mlmodels)
        set_mlmodels_state(state)

    records = map(map_to_record, mlmodels)
    df = pd.DataFrame(records).set_index("id")
    st.table(df)
