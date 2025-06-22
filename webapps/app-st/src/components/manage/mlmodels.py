import pandas as pd
import streamlit as st

from api.ml import get_mlmodels_configs
from api.entities import MLModelConfig


def map_to_record(mlmodel: MLModelConfig) -> dict:
    record = mlmodel.dict()

    return record


def render():
    st.header("Gestión de modelos")
    if st.button("Agregar modelo"):
        st.success("modelo creado")

    mlmodels = get_mlmodels_configs()
    records = map(map_to_record, mlmodels)
    df = pd.DataFrame(records).set_index("id")
    st.table(df)
