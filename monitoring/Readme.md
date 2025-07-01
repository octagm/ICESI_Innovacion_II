# Monitoreo con Streamlit, Prometheus y Grafana

Este entorno está diseñado para correr de forma aislada en un entorno virtual creado con `uv`.

## Estructura del proyecto

- `app/main.py`: Código de la aplicación Streamlit con métricas Prometheus.
- `prometheus/prometheus.yml`: Configuración para el recolector Prometheus.
- `venv_monitoring/`: Entorno virtual creado con `uv`.
- `run_app.bat`: Script para lanzar la app en Windows.

## Requisitos previos

- Python 3.8+
- [uv (Universal Virtualenv Manager)](https://github.com/astral-sh/uv)
- Prometheus y Grafana instalados localmente (manual o vía Docker más adelante)

## Instrucciones de uso

### 1. Crear el entorno virtual
Desde el directorio `monitoring/`:

```bash
uv venv venv_monitoring
