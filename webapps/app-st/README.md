# Aplicación web para despliegue y consumo con modelos

**Ejecución en local utilizando ambiente virtual:**

1. Configurar ambiente virtual local con `uv` ([https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)):
    ```sh
    # multiplataforma 
    uv sync
    ```

2. Definir variables de ambiente e iniciar servicio:
    ```bash
    export API_URL=
    uv run streamlit run src/App.py
    ```

    La aplicación inicia por defecto en el puerto 8501: [http://localhost:8501](http://localhost:8501)

**Ejecución en local utilizando Docker:**

```bash
# construir imagen
docker build -t app-st .

# definir variables de ambiente
API_URL=

# ejecutar contenedor
docker run --rm --name app \
    -e API_URL="$API_URL" \
    -p 8501:8501 \
    app-st
```

**Configuración de variables de ambiente:**

```env
# variables requeridas
API_URL=

# variables con valores por defecto
WEBAPP_AUTH_PROTECTED=true  # habilitado por defecto
WEBAPP_DEMO_MOCK=false  # deshabilitado por defecto

# variables utilizadas en demo mock
ML_IRIS_SERVICE_URL=
ML_MNIST_SERVICE_URL=
```

**Consideraciones de desarrollo:**

Respecto a relaciones de dependencias entre módulos:
- `pages.*` usa `components.*` y `states.*`
- `components.*` usa `api.*` y `states.*`
- `api.*` usa `states.*`
- `states.*` usa `streamlit` y `domain.*`
- `domain.*` no tiene dependencias

Respecto al estado de la aplicación y las solicitudes al servicio API:
- el estado de la aplicación se actualiza mayoritariamente en cada renderizado a través de las solicitudes a la API, por ejemplo, en el componente de gestión de runners ([webapps/app-st/src/components/manage/runners.py](./webapps/app-st/src/components/manage/runners.py)). En una posible siguiente etapa de desarrollo se puede considerar crear un estado local de la aplicación a través `st.session_state` para aquellos componentes que hagan mayor número de solicitudes, buscando así reducir el tiempo de renderizado.

Respecto al estado de sesión de la aplicación `st.session_state` y sus correspondientes llaves y valores (keys, values):
- en [mappings.py.py](./src/states/mappings.py) se definen mappings de llaves de estado de sesión de `streamlit` para centralizar la definición de llaves y reforzar el acceso a ellas a través de propiedades definidas en modelos de `pydantic`.
- considerando que `streamlit` requiere inicializar el estado de sesión para cada llave, se puede inicializar como valor por defecto en el mapeo de estado de sesión en [mappings.py.py](./src/states/mappings.py), o manualmente en el componente; ambas opciones son mutuamente excluyentes dado que `streamlit` exige una única inicialización de valor de estado de sesión por llave.
- cada campo de estado modificado directamente por un elemento de `streamlit` requiere definir un mapping de una llave de estado en `st.session_state`, por ejemplo:
    - ningún elemento modifica el mapping `auth` directamente sino que se modifica atómicamente en [src/api/auth.py](src/api/auth.py) y [src/api/auth.py](src/states/auth.py), por tanto, no es necesario mapear cada uno de sus campos sino el mapeo es un simple string `auth` en [mappings.py.py](./src/states/mappings.py)

Respecto a nuevas configuraciones y módulos de servicios ML:
- el nombre del nuevo módulo en [src/components/ml/](./src/components/ml) deben coincidir con el identificador del servicio ML, por ejemplo, `iris`, `mnist`, y `imagenes_satelitales`
- se debe importar el módulo en la raíz del paquete [src/components/ml/__init__.py](src/components/ml/__init__.py)
- el nuevo módulo en [src/components/ml/](./src/components/ml) debe contener una función `render()` para renderizar el componente.

Respecto a autenticación de usuarios:
- se tiene una versión simple que no maneja cookies, es decir, el usuario debe autenticarse nuevamente si se actualiza la sesión

**Referencias:**

Respecto a declaración de componentes personalizados de Streamlit:
- Documentación: https://docs.streamlit.io/develop/concepts/custom-components
- Plantilla: https://github.com/streamlit/component-template
- Ejemplo plantilla vanilla (sin React): https://github.com/streamlit/component-template/blob/master/template-reactless/my_component/frontend/src/index.tsx
- CDN con demo en JSFiddle para ESM: https://www.jsdelivr.com/package/npm/streamlit-component-lib
