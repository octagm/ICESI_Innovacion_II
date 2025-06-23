import streamlit as st


from components.auth.authenticated import authenticated
from components.manage import mlmodels, runners
from states.mappings import init_app_state_mapping


st.set_page_config(
    layout="wide",
    page_icon="⚙",
    page_title="Gestión de ejecución",
)


@authenticated
def render_protected():
    runners.render()
    st.markdown("---")
    mlmodels.render()


@init_app_state_mapping
def render():
    st.title("Gestión de ejecución")
    st.markdown("---")
    render_protected()


render()
