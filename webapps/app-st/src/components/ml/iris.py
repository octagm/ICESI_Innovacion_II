import os

import streamlit as st

from components.ml.common.json import render as render_json


def render():
    mode_name = os.path.basename(__file__).rstrip('.py')
    render_json(mode_name)
