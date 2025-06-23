import pandas as pd
import streamlit as st

from api.ml import get_runners_configs
from domain.ml import MLRunnerConfig
from states.ml import get_mlrunners_state, set_mlrunners_state


def map_to_record(runner: MLRunnerConfig) -> dict:
    record = runner.dict()
    if record["connection"] is None or record["connection"] == "":
        record["connection"] = "(default)"

    return record


def render():
    st.header("Gestión de runners")
    if st.button("Agregar runner"):
        st.success("runner creado")

    state = get_mlrunners_state()
    with st.spinner("Cargando runners..."):
        runners = get_runners_configs()
        state.update_mlrunners_configs(runners)
        set_mlrunners_state(state)

    records = map(map_to_record, runners)
    df = pd.DataFrame(records).set_index("id")
    st.table(df)
