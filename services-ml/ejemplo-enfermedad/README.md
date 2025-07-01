# Servicio ML básico mock de clasificación de enfermedad

Servicio ML básico mock de clasificación de enfermedad para ejemplificar la configuración mínima de un servicio ML con FastAPI, compatible con el servicio plataforma ML.

**Construcción y ejecución local con Docker:**
```bash
# construir imagen
docker build -t ml-ejemplo-enfermedad:v1 .

# ejecutar contenedor en puerto 5000
docker run --rm --name ml-enfermedad -p 5000:8000 ml-ejemplo-enfermedad:v1
```

**NOTA: ESTE ES UN MOCK DE UN MODELO DE CLASIFICACIÓN SIN NINGÚN SUSTENTO MÉDICO.**

**Solicitar predicciones a través de navegador web para una única instancia:**
- http://localhost:5000/predict?blood_pressure=90&heart_rate=120&temperature=36
- http://localhost:5000/predict?blood_pressure=90&heart_rate=120&temperature=38

**Solicitar predicciones a través de `curl` para múltiples instancias:**
```sh
INSTANCES='''
{"blood_pressure": 90, "heart_rate": 120, "temperature": 36},
{"blood_pressure": 90, "heart_rate": 120, "temperature": 38}
'''

curl -X POST -H "Content-Type: application/json" -d "{\"instances\": [$INSTANCES]}" http://localhost:5000/predict
```
