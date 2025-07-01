import logging

from dto import PredictInstance


CATS = {
    0: "NO ENFERMO",
    1: "ENFERMEDAD LEVE",
    2: "ENFERMEDAD AGUDA",
    3: "ENFERMEDAD CRÓNICA",
}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _predict_mock(temperature: float, heart_rate: int, blood_pressure: int) -> str:
    """
    predecir las siguientes categorías de condición de enfermedad de un paciente a partir de la temperatura, el ritmo cardiaco, y la presión sanguínea:
    - "NO ENFERMO"
    - "ENFERMEDAD LEVE"
    - "ENFERMEDAD AGUDA"
    - "ENFERMEDAD CRÓNICA"

    NOTA: LA SIGUIENTE ES UNA FUNCIÓN MOCK DE UN MODELO DE CLASIFICACIÓN SIN NINGÚN SUSTENTO MÉDICO.
    """

    if temperature < 35.0 or heart_rate < 60 or blood_pressure < 90:
        return CATS[3]
    elif temperature > 38.0 and heart_rate > 100:
        return CATS[2]
    elif temperature > 37.0 and heart_rate > 90:
        return CATS[1]
    elif blood_pressure > 140:
        return CATS[3]
    else:
        return CATS[0]


class ModelService:
    _model = None


    def load_model(self):
        logger.info("cargando modelo...")
        # cargar modelo en sistema de archivos, almacenamiento en la nube, etc.
        # raise error si no es posible cargar el modelo
        self._model = "objeto serializado: .pkl, .ph, .keras, .onnx, etc"


    def predict(self, batch: list[PredictInstance]) -> list[str]:
        if self._model is None:
            raise ValueError("el modelo no ha sido cargado previamente")

        # calcular predicciones con objeto serializado self._model; en este ejemplo se usa una función mock
        predictions = [_predict_mock(n.temperature, n.heart_rate, n.blood_pressure) for n in batch]

        return predictions
