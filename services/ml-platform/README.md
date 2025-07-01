# Servicio plataforma ML

Servicio ML Plataforma para despliegue y consumo de servicios ML.

Consideraciones relevantes:
- Respecto a las configuraciones [MLContainerConfig](services/ml/src/entities/mlmodels.py):
    - El identificador debe cumplir el formato `name:version`
    - El listado de puertos debe listar al menos un puerto expuesto por el contenedor
    - El listado de volúmenes de contenedores debe contener volúmenes con nombre base único:
        - `["/storage", /logs]` es válido
        - `["/storage/logs", /logs]` es inválido

- Respecto al ejecutor [DockerRunner](./src/dependencies/runners/runner_docker.py):
    - Las imágenes de contenedores deben ser accesibles desde de la instancia de Docker
    - Los contenedores de modelos son removidos cuando se detienen, la única persistencia de estos contenedores consiste en un volumen mapeado a un directorio local
    - Los directorios DATA_DIR, MODELS_DIR, y STORAGE_DIR pueden apuntar a cualquier localización del sistema de archivos accesible desde la instancia de Docker
    - Los volúmenes se mapean dentro de un directorio "STORAGE_DIR/services-ml/NAME/VERSION" con permisos de lectura y escritura, excepto los volúmenes `/data` y `/models` que se mapean con permisos de lectura a los directorios DATA_DIR y MODELS_DIR, respectivamente
    - Se puede pubilcar los puertos de un único contenedor en el host para depuración a través de la variable de ambiente `RUNNERS_DOCKER_HOST_PORT_DEBUG`

**ADVERTENCIA: Utilizar directamente Docker como ejecutor tiene restricciones de escalabilidad**

# Despliegue

## Despliegue en local

**En local utilizando ambiente virtual:**
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
    # habilitar Docker como ejecutor de contenedores ML
    export RUNNERS_DOCKER_ENABLED=true

    # directorios
    export DATA_DIR=.data/
    export MLMODELS_DIR=.mlmodels/
    export STORAGE_DIR=.storage/
    ```

3. Iniciar servicio:
    ```sh
    # producción
    PYTHONPATH=src/ fastapi run src/app.py --port 9090

    # desarrollo
    ENVIRONMENT=development PYTHONPATH=src/ fastapi dev src/app.py --port 9090
    ```

4. Verificar documentacción OpenAPI: http://localhost:9090/docs

Consideraciones:
- El archivo `.env` solamente se carga si `ENVIRONMENT=development`

# Referencias:
Docker Runner:
- https://docker-py.readthedocs.io/en/stable/
