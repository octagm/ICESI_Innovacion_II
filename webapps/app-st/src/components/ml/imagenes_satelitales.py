import io
import os

import streamlit as st
from PIL import Image

from api.ml import get_mlservice_config, request_external_mlservice
from states.ml import get_mlmodel_service_url_state_kv


SERVICE_ID = os.path.basename(__file__).rstrip('.py')


def render_images(images_files):
    st.subheader("Imágenes cargadas")
    for n, images_file in enumerate(images_files):
        image_bytes = images_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))

        st.subheader(f"Imagen {n+1}: {images_file.name}")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"Archivo: {images_file.name}")
            st.write(f"Tipo: {images_file.type}")
            st.write(f"Tamaño: {images_file.size / (1024 * 1024):.2f} MB")
            st.write(f"Dimensiones: {image.width} x {image.height} pixels")

        with col2:
            st.image(image, caption=f"Previo de {images_file.name}", use_container_width=True)

        st.markdown("---")


def render():
    st.subheader("Cargue las imágenes")
    images_files = st.file_uploader("Seleccione imágenes (PNG, JPG, JPEG)...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    print(type(images_files), images_files)
    if images_files:
        if st.button("Identificar objetos"):
            st.write("identificando objetos...")
        else:
            st.success(f"Se cargaron correctamente {len(images_files)} archivo(s)")
            render_images(images_files)
