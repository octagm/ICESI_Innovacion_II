# Icesi ML Plataforma

Plataforma prototipo para despliegue y consumo de servicios ML.

# Diseño

## Escenario demanda baja a moderada: Docker

![](./assets/diagrama-servicio-ml-plataforma.png)

# Servicios ML

En [services/ml-platform/README.md](./services/ml-platform/README.md) se presentan algunas consideraciones de configuración de servicios ML.

Ejemplos de desarrollo de servicios ML:
- [services-ml/ejemplo-enfermedad]: ejemplo con los mínimos requerimientos funcionales de un servicio ML
- [services-ml/ejemplo-iris]: ejemplo de servicio cargando modelo ONNX desde directorio compartido de modelos
