import pandas as pd
import streamlit as st

from api.ml import get_mlmodels_configs_map
from api.entities import MLModelConfig


def map_to_record(mlmodel: MLModelConfig) -> dict:
    record = mlmodel.dict()

    return record


def render():
    records = map(map_to_record, get_mlmodels_configs_map().values())
    df = pd.DataFrame(records).set_index("id")
    st.table(df)
