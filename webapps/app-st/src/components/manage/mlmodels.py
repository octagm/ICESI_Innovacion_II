import streamlit as st

from api.ml import get_mlmodels_configs, run_mlmodel, stop_mlmodel
from domain.ml import MLModelConfig
from states.ml import get_mlmodels_state, set_mlmodels_state


@st.dialog("Edición de configuración de modelo ML", width="large")
def render_on_edit(mlmodel: MLModelConfig):
    # TODO complete edition
    edited = st.data_editor([mlmodel.dict()])

    # DRAFT
    #
    # if st.button("Guardar cambios"):
    #     st.success(f"Modelo {edit_id} actualizado")
    #
    # if st.button("Cancelar"):
    #     pass


@st.dialog("Configuración de modelo ML", width="large")
def render_on_expand(mlmodel: MLModelConfig):
    st.json(mlmodel.dict())


class OptionsCallbacks:
    def __init__(self, mlmodel: MLModelConfig):
        self.mlmodel = mlmodel

    def on_delete(self):
        # TODO impleement
        st.toast(f"Borrado sin implementar: {self.mlmodel.id}")

    def on_edit(self):
        render_on_edit(self.mlmodel)

    def on_execute(self):
        mlmodel_id = self.mlmodel.id
        try:
            mlmodel = run_mlmodel(mlmodel_id)
            state = get_mlmodels_state()
            state.update_mlmodels_configs([mlmodel])
            set_mlmodels_state(state)
            st.toast(f"Modelo en ejecución: {mlmodel_id}", icon="✅")
        except RuntimeError as ex:
            st.toast(f"RuntimeError: {ex}", icon=":material/bug_report:")
        except Exception as ex:
            st.toast(f"Exception: {ex}", icon=":material/bug_report:")

    def on_expand(self):
        render_on_expand(self.mlmodel)

    def on_stop(self):
        mlmodel_id = self.mlmodel.id
        try:
            mlmodel = stop_mlmodel(mlmodel_id)
            state = get_mlmodels_state()
            state.update_mlmodels_configs([mlmodel])
            set_mlmodels_state(state)
            st.toast(f"Modelo detenido: {mlmodel_id}", icon="✅")
        except RuntimeError as ex:
            st.toast(f"RuntimeError: {ex}", icon=":material/bug_report:")
        except Exception as ex:
            st.toast(f"Exception: {ex}", icon=":material/bug_report:")


@st.fragment
def render_mlmodel_config_row(mlmodel_id: str, layout_cols_ratios: list[int]):
    """
    - st.fragment actualiza fila eficientemente posterior a cualquier callback.
    - se llama a get_mlmodels_state() para obtener la última versión de estado.
    """

    state = get_mlmodels_state()
    mlmodel = state.get_mlmodel_config(mlmodel_id)
    row = {
        "model_id": mlmodel.id,
        "runner_id": mlmodel.runner_id,
        "status": mlmodel.state.status,
    }

    layout_cols = st.columns(layout_cols_ratios)

    # Display selected fields
    for i, value in enumerate(row.values()):
        layout_cols[i].markdown(str(value))

    # Display options as row of buttons
    with layout_cols[-1].popover("Opciones"):
        callbacks = OptionsCallbacks(mlmodel)
        st.button("Expandir JSON", on_click=callbacks.on_expand, icon=":material/zoom_out_map:", key=f"manage.mlmlodel.expand:{mlmodel_id}", type="tertiary")

        status = mlmodel.state.status.lower()
        if status == "running":
            st.button("Detener", on_click=callbacks.on_stop, icon=":material/stop:", key=f"manage.mlmlodel.stop:{mlmodel_id}", type="tertiary")
        else:
            st.button("Ejecutar", on_click=callbacks.on_execute, icon=":material/arrow_right:", key=f"manage.mlmlodel.execute:{mlmodel_id}", type="tertiary")

        st.button("Editar", on_click=callbacks.on_edit, icon=":material/edit:", key=f"manage.mlmlodel.edit:{mlmodel_id}", type="tertiary")
        st.button("Borrar", on_click=callbacks.on_delete, icon=":material/delete:", key=f"manage.mlmlodel.delete:{mlmodel_id}", type="tertiary")


@st.fragment
def render():
    st.header("Gestión de modelos")
    if st.button("Agregar modelo", icon=":material/add:"):
        st.success("modelo creado")

    state = get_mlmodels_state()
    with st.spinner("Cargando modelos..."):
        mlmodels = get_mlmodels_configs()
        state.update_mlmodels_configs(mlmodels)
        set_mlmodels_state(state)


    mlmodels = state.get_mlmodels_configs()

    headers = ["model_id", "runner_id", "status"]
    layout_cols_ratios = (3, 1, 1, 1)  # columna extra para opciones
    layout_cols = st.columns(layout_cols_ratios)
    for header, col in zip(headers, layout_cols[:-1]):
        col.markdown(f"**{header}**")

    for mlmodel in mlmodels:
        render_mlmodel_config_row(mlmodel.id, layout_cols_ratios)
