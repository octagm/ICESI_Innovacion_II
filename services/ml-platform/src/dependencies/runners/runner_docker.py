import logging
import os

from datetime import datetime
from pathlib import Path

import docker

from config import settings
from dependencies.runners.runner import ContainerRunner
from entities.mlmodels import MLContainerConfig, MLModelConfig, MLModelRunningState
from entities.mlrunners import MLRunnerState
from exceptions.container import ContainerImageNotAccessible


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATA_DIR: Path = settings["data"]["data_dir"]
DNS_NETWORK: str = settings["runners"]["docker"]["dns_network"]
ML_SERVICES_HOST_PORT_DEBUG: str = settings["runners"]["docker"]["host_port_debug"]
ML_SERVICES_STORAGE_DIR: Path = settings["storage"]["ml_services_dir"]
MODELS_DIR: Path = settings["mlmodels"]["mlmodels_dir"]


def _extract_container_name(mlmodel: MLModelConfig) -> str:
    # docker: only [a-zA-Z0-9][a-zA-Z0-9_.-] are allowed
    return mlmodel.id.replace(":", "-")


def _list_hosts(container_name, container_ports, host_port_mapping) -> list[str]:
    hosts_by_dns = [f"http://{container_name}:{port}" for port in container_ports]
    hosts_by_host_mapping = [f"http://localhost:{port}" for port in host_port_mapping.values()]
    hosts = hosts_by_dns + hosts_by_host_mapping
    return hosts


def _map_ports(mlmodel: MLModelConfig) -> dict[str, str]:
    if ML_SERVICES_HOST_PORT_DEBUG is None:
        return {}

    port_host = int(ML_SERVICES_HOST_PORT_DEBUG)
    container_ports = mlmodel.container_config.ports

    # {'8080/tcp': 7000} : publicar el puerto 8080 del contenedor a través del puerto 7000 del host
    ports = {f'{port}/tcp': (port_host + n) for (n, port) in enumerate(container_ports)}

    return ports


def _map_volumes(mlmodel: MLModelConfig) -> list[str]:
    mappings = []
    if mlmodel.container_config.volumes is not None:
        vols = mlmodel.container_config.volumes.copy()
        if "/data" in vols:
            mappings.append(f"{DATA_DIR}:/data:ro")
            vols.remove("/data")
        if "/models" in vols:
            mappings.append(f"{MODELS_DIR}:/models:ro")
            vols.remove("/models")

        if len(vols) > 0:  
            storage_dir = ML_SERVICES_STORAGE_DIR / mlmodel.name / mlmodel.version
            os.makedirs(storage_dir, exist_ok=True)
            storage_mappings = [f"{storage_dir / os.path.basename(vol)}:{vol}" for vol in vols]
            mappings.extend(storage_mappings)

    return mappings


class DockerRunner(ContainerRunner):
    # TODO implement custom network
    client: docker.DockerClient | None = None
 

    def __repr__ (self):
        if self.client is None:
            return "DockerRunner(client=None, state=None)"

        return f"DockerRunner(client={self.client}, state={self.state.dict()})"


    def connect(self) -> MLRunnerState:
        self.client = docker.from_env()
        self.refresh_state()
        if self.state.connected:
            logger.info("Cliente de Docker inicializado y conectado exitosamente")

        return self.state


    def refresh_state(self) -> MLRunnerState:
        self.validate_client()
        
        connected = False
        error_message = None
        try:
            self.client.ping()
            connected = True
        except docker.errors.DockerException as e:
            error_message = f"El demonio de Docker no responde"
            logger.error(f"{error_message}; error: {e}")

        self.state = MLRunnerState(
            connected=connected,
            error_message=error_message,
            last_updated=datetime.now().isoformat(),
        )

        return self.state


    def run_container(self, mlmodel: MLModelConfig) -> MLModelRunningState:
        assert isinstance(mlmodel, MLModelConfig), "El argumento debe ser una instancia de MLModelConfig"

        self.validate_client()
        self.validate_image_access(mlmodel.container_config.image)

        name = _extract_container_name(mlmodel)
        ports = _map_ports(mlmodel)
        volumes = _map_volumes(mlmodel)

        logger.info(f'volumes={volumes}')

        try:
            container = self.client.containers.run(
                mlmodel.container_config.image,
                detach=True,
                environment=mlmodel.container_config.envs,
                name=name,
                network=DNS_NETWORK,
                ports=ports,
                remove=mlmodel.container_config.remove,
                volumes=volumes,
            )
            self.mlmodels_containers_map.add_entry(mlmodel.id, container.id)
            logger.info(f"Contenedor creado con ID={container.id} para el modelo={mlmodel.id}.")

        except docker.errors.ImageNotFound as e:
            logger.error(f"La imagen '{image_name}' no fue encontrada.")
            raise ContainerImageNotAccessible(f"La imagen '{mlmodel.container_config.image}' no fue encontrada.")
        except docker.errors.APIError as e:
            info = f"Error en la API de Docker al intentar crear el contenedor de mlmodel: {mlmodel}"
            logger.error(f"{info}; error: {e}")
            raise RuntimeError(info, e)
        except Exception as e:
            info = f"Error inesperado al intentar crear el contenedor de mlmodel: {mlmodel}"
            logger.error(f"{info}; error: {e}")
            raise RuntimeError(info, e)

        hosts = _list_hosts(name, mlmodel.container_config.ports, ports)

        return MLModelRunningState(
            hosts=hosts,
            last_updated=datetime.now().isoformat(),
            runner_metadata={
                "container_id": container.id,
                "ports": ports
            },
            status="running",
        )


    def stop_container(self, mlmodel: MLModelConfig) -> MLModelRunningState:
        assert isinstance(mlmodel, MLModelConfig), "El argumento debe ser una instancia de MLModelConfig"

        self.validate_client()

        container_id = self.mlmodels_containers_map.get_container_by_mlmodel(mlmodel.id)
        if container_id is None:
            raise ValueError(f"El modelo {mlmodel.id} no está en ejecución")

        try:
            container = self.client.containers.get(container_id)
            container.stop()
            # container.remove()
            logger.info(f"Contenedor {container_id} detenido y eliminado exitosamente.")
        except docker.errors.NotFound:
            logger.error(f"El contenedor {container_id} no fue encontrado.")
            # raise RuntimeError(f"El contenedor {container_id} no fue encontrado.")
        except docker.errors.APIError as e:
            logger.error(f"Error al detener el contenedor {container_id}: {e}")
            raise RuntimeError(f"Error al detener el contenedor {container_id}: {e}")

        self.mlmodels_containers_map.remove_entry(mlmodel.id)

        return MLModelRunningState(
            hosts=[],
            last_updated=datetime.now().isoformat(),
            status="stopped",
        )


    def validate_client(self) -> None:
        if self.client is None:
            raise RuntimeError("El cliente de Docker no está inicializado. No se puede refrescar el estado.")


    def validate_image_access(self, image_name: str) -> None:
        try:
            self.client.images.get(image_name)
        except docker.errors.ImageNotFound:
            logger.info(f"Imagen '{image_name}' no encontrada localmente. Descargando...")

            try: 
                # Intentar descargar la imagen desde el registro
                self.client.images.pull(image_name)
            except docker.errors.ImageNotFound:
                raise ContainerImageNotAccessible(f"La imagen '{image_name}' no fue encontrada en el registro.")
