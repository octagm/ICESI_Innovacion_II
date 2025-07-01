import logging
import os
from pathlib import Path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENVIRONMENT = os.getenv("ENVIRONMENT", "production").lower()

if ENVIRONMENT == "development":
    from dotenv import load_dotenv
    load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR", ".data/")).absolute()
MLMODELS_ROOT_DIR = Path(os.getenv("MLMODELS_DIR", ".models/")).absolute()
STORAGE_ROOT_DIR = Path(os.getenv("STORAGE_DIR", ".storage/")).absolute()

settings = {
    "data": {
        "data_dir": DATA_DIR,
    },
    "mlmodels": {
        "mlmodels_dir": MLMODELS_ROOT_DIR,
    },
    "runners": {
        "docker": {
            "enabled": os.getenv("RUNNERS_DOCKER_ENABLED", "false").lower() == "true",
            "host_port_debug": os.getenv("RUNNERS_DOCKER_HOST_PORT_DEBUG"),  # puerto inicial del host para depurar un contenedor
        }
    },
    "storage": {
        "root_dir": STORAGE_ROOT_DIR,
        "ml_services_dir": STORAGE_ROOT_DIR / "services-ml",
    },
}

logger.info(f"Settings loaded for environment '{ENVIRONMENT}': {settings}")
