@echo off
echo ================================
echo Activando entorno virtual...
echo ================================
call venv_monitoring\Scripts\activate

echo ================================
echo Iniciando aplicación Streamlit
echo ================================
streamlit run app\main.py