# Servicio ML - Iris

Servicio ML para clasificar la especie de una flor según el conjunto de datos de referencia: Iris dataset: https://archive.ics.uci.edu/dataset/53/iris

Contenido:
- [Descripción](#descripción)
- [Endpoints](#endpoints)
- [Ejecución](#ejecución)
- [Pruebas](#pruebas)

# Descripción

El siguiente servicio ML ejemplifica:
- Cargar un modelo desde un directorio local o de red
- Guardar un modelo descargado desde una dirección HTTP
- Ejecución de pruebas unitarias con `pytest`

# Endpoints

El servicio soporta los siguientes endpoints y métodos HTTP:
```
GET /_health

GET /_ready

GET /docs

POST /predict
Content-Type: application/json
{"instances": [[6.1, 2.8, 4.7, 1.2], [5.7, 3.8, 1.7, 0.3]]}

POST /predict
Content-Type: application/json
{"config": {"csv_file_uri": "FILE_URI" }}

POST /predict
Content-Type: application/json
{"config": {"csv_file_uri": "FILE_URI", "delimeter": ","}}
```

En [src/entities.py](src/entities.py) se encuentran los modelos de solicitud-respuesta para el endpoint `/predict`.


# Ejecución

**Ejecución en local utilizando Docker:**

1. Construir la imagen del contenedor:
    ```sh
    # construir imagen
    docker build --target=service -t ml-ejemplo-iris:v1 .
    ```


2. Ejecutar imagen del contenedor: 
    * Opción 1: utilizar un servidor de archivos en el directorio de modelos para definir la variable MLMODEL_URI con un enlace HTTP del archivo del modelo ONNX
        ```sh  
        # modelo local a través de servidor de archivos en el directorio de modelos
        # python -m http.server 6060
        # python3 -m http.server 6060

        # el DNS del contenedor apunta `host.docker.internal` al localhost del host de Docker
        MLMODEL_URI=http://host.docker.internal:6060/iris_logreg_v1.onnx


        # ejecutar contenedor en puerto 5000
        docker run --rm --name ml-iris -e "MLMODEL_URI=${MLMODEL_URI}" -p 5000:80 ml-ejemplo-iris:v1
        ```

    * Opción 2: utilizar un volumen para mapear el directorio de modelos y definir la variable MLMODEL_URI con la ruta del archivo del modelo ONNX
        ```sh  
        # ejecutar contenedor en puerto 5000
        docker run --rm --name ml-iris -e "MLMODEL_URI=/models/iris_logreg_v1.onnx" -p 5000:80 -v MODELS_DIR:/models:ro ml-ejemplo-iris:v1
        ```


3. Solicitar predicciones declarando instancias:
    ```sh
    INSTANCES='[[6.1, 2.8, 4.7, 1.2], [5.7, 3.8, 1.7, 0.3]]'
    curl -X POST \
        -H 'Content-Type:application/json' \
        -d "{\"instances\": ${INSTANCES} }" \
        localhost:5000/predict
    ```

4. Solicitar predicciones referenciando archivo:
    ```sh
    # levantar servidor de archivos en el directorio local de datos
    # python -m http.server 7070
    # python3 -m http.server 7070

    # el DNS del contenedor apunta `host.docker.internal` al localhost del host de Docker
    curl -X POST \
        -H 'Content-Type:application/json' \
        -d '{"config": {"csv_file_uri": "http://host.docker.internal:7070/iris_X_test.csv"}}' \
        localhost:5000/predict
    ```

**Ejecución en local utilizando ambiente virtual:**
1. Configurar ambiente:
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

2. Definición de variables de ambiente:
    ```sh
    # directorio para cargar modelos o para guardar modelos descargados
    MLMODELS_DIR=

    # cargar modelo local
    MLMODEL_URI="${MLMODELS_DIR}/iris_logreg_v12.onnx"

    # guardar modelo descargado: http o https
    MLMODEL_URI=
    ```

3. Iniciar servicio:
    ```sh
    # modo producción
    PYTHONPATH=src/ fastapi run src/app.py --port 8000

    # modo desarrollo
    ENVIRONMENT=development PYTHONPATH=src/ fastapi dev src/app.py --port 8000
    ```

4. Solicitar predicciones declarando instancias:
    ```sh
    INSTANCES='[[4.6, 3.6, 1.0, 0.2]]'
    curl -X POST \
        -H 'Content-Type:application/json' \
        -d "{\"instances\": ${INSTANCES} }" \
        localhost:8000/predict
    ```

5. Solicitar predicciones referenciando archivo:
    ```sh
    DATA_TEST_FILEPATH=
    curl -X POST \
        -H 'Content-Type:application/json' \
        -d "{\"config\": {\"csv_file_uri\": \"${DATA_TEST_FILEPATH}\" }}" \
        localhost:5000/predict
    ```

# Pruebas

**Pruebas en local utilizando Docker:**
```sh
# crear imagen de pruebas
docker build --target testing -t ml-ejemplo-iris-testing .

# ejecutar contenedor de pruebas
docker run --rm --name ml-iris-testing ml-ejemplo-iris-testing
```

**Pruebas en local utilizando ambiente virtual (previamente creado):**
```sh
# instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# correr pruebas unitarias
pytest
```
