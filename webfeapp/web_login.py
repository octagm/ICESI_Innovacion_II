import streamlit as st
import sqlite3
import hashlib
import secrets
from streamlit_extras.mention import mention

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Portal de Acceso", page_icon="🔐", layout="centered")

# --- BASE DE DATOS ---
def get_conn():
    return sqlite3.connect("users.db", check_same_thread=False)

def create_users_table():
    conn = get_conn()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_user(username, password):
    conn = get_conn()
    cur = conn.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    return row and row[0] == hash_password(password)

def update_password(username, new_password):
    conn = get_conn()
    cur = conn.execute("UPDATE users SET password = ? WHERE username = ?", (hash_password(new_password), username))
    conn.commit()
    return cur.rowcount > 0

def user_exists(username):
    conn = get_conn()
    cur = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    return cur.fetchone() is not None

# --- VALIDACIÓN DE CONTRASEÑAS ---
def validar_contrasena(password):
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not any(c.isupper() for c in password):
        return "La contraseña debe contener al menos una letra mayúscula."
    if not any(c.islower() for c in password):
        return "La contraseña debe contener al menos una letra minúscula."
    if not any(c.isdigit() for c in password[1:]):
        return "La contraseña debe contener al menos un número (no en la primera posición)."
    if not any(c in "!@#$%^&()_-+=[]{};:,.<>?/|\\~`" for c in password):
        return "La contraseña debe incluir al menos un carácter especial (que no sea '*')."
    if password[0].isdigit():
        return "La contraseña no puede comenzar con un número."
    if "*" in password:
        return "La contraseña no puede contener el carácter '*'."
    return None

# --- INICIALIZACIÓN DE TABLA ---
create_users_table()

# --- INTERFAZ ---
st.title("🔐 Portal de Acceso Plataforma Servicios ML")
st.markdown("Bienvenido al sistema. Por favor inicia sesión o regístrate si aún no tienes cuenta.")

# Sidebar con menú
menu = st.sidebar.radio("Navegación", ["Iniciar sesión", "Registrarse", "Olvidé mi contraseña"])

# --- INICIAR SESIÓN ---
if menu == "Iniciar sesión":
    st.subheader("👤 Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if validate_user(username, password):
            st.success(f"✅ ¡Bienvenido, {username}!")
            st.session_state.token = secrets.token_hex(16)
            st.markdown("[👉 Ir a la aplicación principal](https://TU_APP.com)", unsafe_allow_html=True)
        else:
            st.error("❌ Usuario o contraseña incorrectos.")

# --- REGISTRO DE USUARIO ---
elif menu == "Registrarse":
    st.subheader("📝 Crear nuevo usuario")
    new_user = st.text_input("Nuevo usuario")
    new_pass = st.text_input("Contraseña", type="password")
    confirm_pass = st.text_input("Confirmar contraseña", type="password")
    if st.button("Registrar"):
        if not new_user or not new_pass:
            st.warning("⚠️ Todos los campos son obligatorios.")
        elif new_pass != confirm_pass:
            st.warning("⚠️ Las contraseñas no coinciden.")
        else:
            error_msg = validar_contrasena(new_pass)
            if error_msg:
                st.warning(f"⚠️ {error_msg}")
            elif add_user(new_user, new_pass):
                st.success("✅ Usuario creado exitosamente.")
            else:
                st.error("⚠️ El usuario ya existe.")

# --- RECUPERAR CONTRASEÑA ---
elif menu == "Olvidé mi contraseña":
    st.subheader("🔁 Recuperación de contraseña")
    user = st.text_input("Usuario")
    new_pass = st.text_input("Nueva contraseña", type="password")
    confirm_new_pass = st.text_input("Confirmar nueva contraseña", type="password")
    if st.button("Actualizar contraseña"):
        if not user_exists(user):
            st.error("❌ El usuario no existe.")
        elif new_pass != confirm_new_pass:
            st.warning("⚠️ Las contraseñas no coinciden.")
        else:
            error_msg = validar_contrasena(new_pass)
            if error_msg:
                st.warning(f"⚠️ {error_msg}")
            elif update_password(user, new_pass):
                st.success("🔐 Contraseña actualizada correctamente.")
            else:
                st.error("❌ No se pudo actualizar la contraseña.")

# --- PIE DE PÁGINA ---
st.divider()