# Modelo Iris - clasificación de especie

**Desarrollo de modelo y datos en local:**

1. Configurar ambiente virtual local:
    ```sh
    # Unix 
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Windows (Git-Bash)
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt

    # Windows (Power-Shell)
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2. Desarrollo de modelo y escritura de modelo:
    ```sh
    python -m scripts.fit_write_model --name iris_logreg_v1.onnx --dir .models/
    ```

3. Guardar datos de prueba:
    ```sh
    python -m scripts.write_test_data --dir .data/
    ```
