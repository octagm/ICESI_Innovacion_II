import pandas as pd
import streamlit as st

from api.ml import get_runners_configs_map
from api.entities import MLRunnerConfig


def map_to_record(runner: MLRunnerConfig) -> dict:
    record = runner.dict()
    if record["connection"] is None or record["connection"] == "":
        record["connection"] = "(default)"

    return record


def render():
    records = map(map_to_record, get_runners_configs_map().values())
    df = pd.DataFrame(records).set_index("id")
    st.table(df)
