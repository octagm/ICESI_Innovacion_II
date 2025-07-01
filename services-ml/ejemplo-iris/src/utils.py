import logging
import os
from urllib.parse import urlparse

import httpx

from config import MLMODELS_DIR


logger = logging.getLogger(__name__)


def download_model_from_http(model_uri: str, models_dir: str = MLMODELS_DIR) -> str:
    filename = os.path.basename(urlparse(model_uri).path)
    filepath = os.path.join(models_dir, filename)

    os.makedirs(models_dir, exist_ok=True)
    try:
        with httpx.stream("GET", model_uri) as response:
            response.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
        logger.info(f'Model downloaded from "{model_uri}" to "{filepath}"')
    except Exception as e:
        logger.error(f"Failed to download model from {model_uri}: {e}")
        raise

    return filepath
