import pandas as pd
import streamlit as st

from api.ml import get_runners_configs
from api.entities import MLRunnerConfig


def map_to_record(runner: MLRunnerConfig) -> dict:
    record = runner.dict()
    if record["connection"] is None or record["connection"] == "":
        record["connection"] = "(default)"

    return record


def render():
    st.header("Gestión de runners")
    if st.button("Agregar runner"):
        st.success("runner creado")

    runners = get_runners_configs()
    records = map(map_to_record, runners)
    df = pd.DataFrame(records).set_index("id")
    st.table(df)
