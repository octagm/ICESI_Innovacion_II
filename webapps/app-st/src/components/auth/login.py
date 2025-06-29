import streamlit as st
from api.auth import login, register_user, user_exists


def render():
    st.subheader("Iniciar sesión")

    # Mostrar login solo si no está en modo registro
    if not st.session_state.get("show_register", False):
        username = st.text_input("Usuario", key="login_user")
        password = st.text_input("Contraseña", type="password", key="login_pass")

        if st.button("Ingresar"):
            try:
                login(username=username, password=password)
                st.success("Inicio de sesión exitoso.")
                st.rerun()
            except Exception as e:
                if str(e) == "no_user":
                    st.warning("⚠️ El usuario no existe.")
                    st.session_state.show_register = True
                elif str(e) == "invalid_password":
                    st.error("❌ Contraseña incorrecta.")
                else:
                    st.error(f"Error inesperado: {e}")

    # Mostrar formulario de registro si está activado
    if st.session_state.get("show_register", False):
        show_registration()


def show_registration():
    st.subheader("Registrar nuevo usuario")

    new_user = st.text_input("Nuevo usuario", key="reg_user")
    new_pass = st.text_input("Contraseña", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirmar contraseña", type="password", key="reg_confirm")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Crear cuenta"):
            if not new_user or not new_pass:
                st.warning("Todos los campos son obligatorios.")
            elif new_pass != confirm_pass:
                st.warning("Las contraseñas no coinciden.")
            elif user_exists(new_user):
                st.warning("El usuario ya existe.")
            else:
                register_user(new_user, new_pass)
                st.success("✅ Usuario registrado. Ahora puede iniciar sesión.")
                st.session_state.show_register = False
                st.rerun()

    with col2:
        if st.button("Cancelar"):
            st.session_state.show_register = False
            st.rerun()
