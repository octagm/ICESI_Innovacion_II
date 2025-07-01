import time
import streamlit as st
from prometheus_client import start_http_server, Summary

# Inicializar métricas y servidor solo una vez
if 'metrics_initialized' not in st.session_state:
    st.session_state.REQUEST_TIME = Summary(
        'request_processing_seconds',
        'Tiempo de procesamiento de solicitud'
    )
    start_http_server(8050)  # Inicia Prometheus en http://localhost:8050/metrics
    st.session_state.metrics_initialized = True

# Decorador para medir tiempo de ejecución
@st.session_state.REQUEST_TIME.time()
def process_request():
    time.sleep(1)  # Simula una tarea

# Interfaz de usuario
st.title("App de Monitoreo con Prometheus")
if st.button("Ejecutar tarea"):
    process_request()
    st.success("¡Tarea completada!")
st.write("Métricas disponibles en: [http://localhost:8050/metrics](http://localhost:8050/metrics)")