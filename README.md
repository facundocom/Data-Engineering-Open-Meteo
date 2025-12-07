# Data Engineering Pipeline: Open-Meteo a MinIO (Delta Lake)

Este proyecto implementa un pipeline de ingeniería de datos (ETL) diseñado para extraer datos meteorológicos (pronósticos e históricos) de la API de **Open-Meteo** y almacenarlos en un **Object Storage (MinIO)** utilizando el formato **Delta Lake**.

El caso de uso actual está configurado para monitorear las condiciones climáticas en **Cuesta del Viento, San Juan, Argentina**.

## 🚀 Características

* **Extracción de Datos:** Obtiene variables horarias como temperatura (2m), velocidad del viento (10m), ráfagas de viento (10m) y dirección del viento (10m).
* **Gestión de API:** Implementa caché y reintentos automáticos (retries) para optimizar las peticiones a Open-Meteo y manejar fallos de red.
* **Almacenamiento Eficiente:** Utiliza **Delta Lake** sobre S3/MinIO, lo que permite transacciones ACID y un manejo eficiente de versiones de datos.
* **Carga Incremental (Forecast):** Soporta `upserts` (merge) para actualizar los pronósticos sin duplicar datos. Inserta nuevos registros o actualiza los existentes basándose en la fecha ("src.date = tgt.date").
* **Carga Histórica:** Permite la carga masiva de datos históricos organizados por año y mes (rango configurado por defecto: 2019-2024).

## 📂 Estructura del Proyecto

El proyecto está modularizado para separar responsabilidades de extracción, configuración y carga:

.
├── main.py                     # Punto de entrada. Orquesta la extracción y la carga de datos.
├── datapipeline/
│   ├── gestorAPI.py            # Configuración del cliente API Open-Meteo (params, cache, retry).
│   ├── gestorEXT.py            # Lógica de extracción: realiza las peticiones y transforma a Pandas DataFrame.
│   ├── gestorCARGA.py          # Lógica de carga: escribe DataFrames en MinIO usando Delta Lake.
│   └── MINIOconfig.py          # Configuración de conexión al bucket S3/MinIO (credenciales y endpoints).
└── .gitignore                  # Archivos ignorados por git (ej. __pycache__, .vscode).

## 🛠️ Requisitos e Instalación

Este proyecto requiere **Python 3.x**. Las principales librerías utilizadas son:

* `openmeteo-requests`
* `requests-cache`
* `retry-requests`
* `deltalake`
* `pandas`
* `pyarrow`
* `apscheduler` (para la ejecución programada)

### Instalación de dependencias

Puedes instalar todas las librerías necesarias ejecutando el siguiente comando:

pip install openmeteo-requests requests-cache retry-requests deltalake pandas pyarrow apscheduler

## ⚙️ Configuración

### 1. Configuración de MinIO (datapipeline/MINIOconfig.py)
Actualmente, las credenciales están definidas dentro del código. 
**Importante:** Para un entorno productivo, se recomienda usar variables de entorno. Para pruebas locales, asegúrate de que `AWS_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY` coincidan con tu instancia de MinIO.

### 2. Parámetros de Ubicación (main.py)
Por defecto, el script busca datos para **Cuesta del Viento**. Puedes modificar las coordenadas y la zona horaria en el bloque principal de `main.py`:

latitud_cuesta = -30.183
longitud_cuesta = -69.066
timezone_cuesta = "America/Argentina/San_Juan"

## ▶️ Uso

Para ejecutar el pipeline manualmente, corre el script principal:

python main.py

### Flujo de Ejecución en `main.py`:

1.  **Inicialización:** Se configuran los gestores de API (`APIconfig`), extracción (`extraccion`), carga (`carga`) y almacenamiento (`configMINIO`).
2.  **Carga Incremental (Forecast):** * Llama a `extincremental`.
    * Intenta realizar un `upsert` (merge) con los datos del pronóstico del día.
    * Si la tabla Delta no existe (primera ejecución), realiza una carga inicial (`carga_forecast_overw`).
3.  **Carga Histórica:** * Llama a `gc.carga_historical_overw`.
    * Itera sobre el rango de años y meses definido para descargar y guardar el historial.

> **Automatización:** El código incluye bloques comentados para usar `BlockingScheduler`, lo que permitiría ejecutar el proceso automáticamente todos los días a una hora específica.

## 📊 Datos Generados (Data Lake)

Los datos se guardan en el bucket especificado (`facundocoria-bucket`) siguiendo una estructura de **Bronze Layer**:

* **Forecast (Pronóstico):** Ruta: `datalake/bronze/forecast/YYYY/MM/DD`
* **Historical (Histórico):** Ruta: `datalake/bronze/historical/YYYY/MM`

Al utilizar **Delta Lake**, estos datos pueden ser consultados posteriormente utilizando motores como Spark, Trino, o nuevamente con Python (`deltalake` / `pandas`).
