import json
import os

import streamlit as st

from api.ml import get_mlservice_config, request_external_mlservice
from states.ml import get_mlmodel_service_url_state_kv


SERVICE_ID = os.path.basename(__file__).rstrip('.py')


def render():
    # svc = get_mlservice_config(SERVICE_ID)

    st.title("Tiempo clima")
