import streamlit as st

from components.auth.authenticated import authenticated
from states.app import init_app_state_mapping
from states.auth import get_user


st.set_page_config(
    page_title="App",
    page_icon="🤖",
)



@authenticated
def render_protected():
    user = get_user()
    st.subheader(f"¡Hola {user.username}!")
    st.markdown("""
        Esto es contenido protegido
    """)


@init_app_state_mapping
def render():
    st.title("MLIcesiP")
    render_protected()


render()
