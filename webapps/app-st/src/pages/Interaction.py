import streamlit as st

from components.auth.authenticated import authenticated
import components.mlmodels_selector as mlmodel_selection
import components.ml as mlcomponents
from states.mappings import init_app_state_mapping
from states.ml import get_mlmodel_type_state_kv


st.set_page_config(
    layout="wide",
    page_title="ML Interacción con modelos",
    page_icon="🧠",
)


@authenticated
def render_protected():
    st.sidebar.header("Modelo")
    with st.sidebar:
        mlmodel_selection.render()

    (_, mlmodel_type) = get_mlmodel_type_state_kv()
    if mlmodel_type == "":
        st.write("Seleccione un modelo en el panel lateral")
        return

    try:
        component_module_name = mlmodel_type.replace("-", "_")
        mlcomponent = getattr(mlcomponents, component_module_name)
    except AttributeError:
        st.error(f"icesi: no se encontró el componente para el tipo de modelo: {mlmodel_type}")
        return
    except Exception as e:
        st.error(f"icesi: error cargando el componente del modelo: {mlmodel_type}: {e}")
        return

    mlcomponent.render()


@init_app_state_mapping
def render():
    st.title("Predicción, interacción y consumo de modelos")

    render_protected()


render()
