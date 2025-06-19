import httpx
import streamlit as st

from api.auth import login


def render():
    st.subheader("Login")
    with st.form("login_form"):
        username = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type="password")        
        if st.form_submit_button("Login"):
            try:
                login(username=username, password=password)
                st.rerun()
            except httpx.HTTPStatusError as ex:
                st.error(f"icesi: {ex}")
            except Exception as ex:
                st.error(f"icesi: {ex}")
