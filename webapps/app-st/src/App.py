import streamlit as st
from api.auth import logout

from components.auth.authenticated import authenticated
from states.auth import get_user
from states.mappings import init_app_state_mapping


st.set_page_config(
    page_title="App",
    page_icon="🤖",
)


@authenticated
def render_protected():
    user = get_user()
    st.subheader(f"¡Hola {user.username}!")

    if st.button("Cerrar sesión 🔒"):
        logout()
        st.success("Sesión cerrada.")
        st.rerun()

    st.markdown("""
                Esto es contenido protegido
                """)

@init_app_state_mapping
def render():
    st.title("MLIcesiP")
    render_protected()


render()
