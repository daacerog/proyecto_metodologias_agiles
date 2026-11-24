# Definición de los datos

## Origen de los datos

- [x] Especificar la fuente de los datos y la forma en que se obtuvieron.

Los datos vienen de tres fuentes públicas:

- **FRED**, la base de datos económicos de la Reserva Federal de St. Louis, publica los precios spot diarios de WTI (`DCOILWTICO`) y Brent (`DCOILBRENTEU`), originados en la EIA.
- **Yahoo Finance** aporta los futuros continuos de WTI (`CL=F`) y Brent (`BZ=F`) con apertura, máximo, mínimo y cierre, además de dos índices de volatilidad implícita: **OVX**, la volatilidad esperada del crudo calculada por CBOE, y **VIX**, la del mercado accionario.
- **EIA** (Administración de Información Energética de EE.UU.) aporta variables fundamentales como los inventarios semanales de crudo (serie `WCESTUS1`).

La información se obtiene por conexión programática:

- La API de FRED, con la librería `fredapi`.
- La API v2 de la EIA, con `requests`.
- La librería `yfinance` para Yahoo Finance.

Son series de tiempo financieras: precios e índices de volatilidad implícita en frecuencia diaria, e inventarios en frecuencia semanal. El período va de 2007 a la fecha de corte porque OVX existe desde ese año, y la ventana incluye los regímenes de volatilidad más relevantes para el problema: la crisis de 2008, la caída de 2014 a 2016, el precio negativo de WTI en abril de 2020 y el shock de 2022.

## Especificación de los scripts para la carga de datos

- [x] Especificar los scripts utilizados para la carga de los datos.

| Archivo | Contenido |
|---|---|
| [`src/volatilidad/database/fuentes.py`](../../src/volatilidad/database/fuentes.py) | Funciones reutilizables: `descargar_fred`, `descargar_yahoo`, `descargar_eia`, `cargar_con_cache` y `resumen_calidad`. |
| [`scripts/data_acquisition/main.py`](../../scripts/data_acquisition/main.py) | Script que se ejecuta: lee las claves, descarga (o lee de la caché) las tres fuentes, hace los chequeos de calidad y guarda el resumen. |

Ejecución, desde la raíz del repositorio y con el paquete instalado (`pip install -e .`):

```bash
python scripts/data_acquisition/main.py
python scripts/data_acquisition/main.py --fecha-fin 2026-11-20   # otra fecha de corte
```

**Credenciales.** FRED y EIA requieren una API key gratuita. Las claves se leen de las variables de entorno `FRED_API_KEY` y `EIA_API_KEY`, que pueden definirse en un archivo `.env` en la raíz del repositorio (ver `.env.example`). El archivo `.env` está excluido de git y las claves nunca se escriben en el código. Si no están definidas, el script las pide por consola, y solo cuando hace falta consultar la API: quien ya tenga la caché puede correrlo sin claves.

## Referencias a rutas o bases de datos origen y destino

- [x] Especificar las rutas o bases de datos de origen y destino para los datos.

### Rutas de origen de datos

- [x] Especificar la ubicación de los archivos de origen de los datos.
- [x] Especificar la estructura de los archivos de origen de los datos.
- [x] Describir los procedimientos de transformación y limpieza de los datos.

| Fuente | Ubicación | Series | Estructura de la respuesta |
|---|---|---|---|
| FRED | API de FRED (`fredapi`) | `DCOILWTICO`, `DCOILBRENTEU` | Una serie por código, indexada por fecha. |
| Yahoo Finance | `yfinance` | `CL=F`, `BZ=F`, `^OVX`, `^VIX` | Tabla OHLC diaria por ticker, con fechas con zona horaria. |
| EIA | `https://api.eia.gov/v2/petroleum/stoc/wstk/data/` | `WCESTUS1` (frecuencia semanal) | JSON con una lista de registros (`period`, `value`) en `response.data`. |

Transformaciones aplicadas en la carga:

- Las series se renombran con nombres claros (`wti_spot`, `wti_fut_close`, `ovx_close`, `inv_crudo`, etc.).
- De Yahoo Finance se conservan solo apertura, máximo, mínimo y cierre, y las fechas se dejan sin zona horaria para poder alinearlas con FRED.
- De la EIA se convierte `period` a fecha y `value` a número.
- No se imputan nulos ni se eliminan registros en esta fase. Los chequeos de calidad (rango de fechas por columna, valores válidos y nulos, mínimo y máximo, índice ordenado y sin duplicados) quedan registrados para la fase de preprocesamiento.
- Se conservan los precios negativos de WTI del 20 de abril de 2020, que son reales. Se tendrán en cuenta al construir el objetivo de volatilidad.

### Base de datos de destino

- [x] Especificar la base de datos de destino para los datos.
- [x] Especificar la estructura de la base de datos de destino.
- [x] Describir los procedimientos de carga y transformación de los datos en la base de datos de destino.

El destino es una caché local de archivos CSV en `data/raw/`, que está excluida de git.

| Archivo | Contenido |
|---|---|
| `data/raw/fred_spot_<inicio>_<fin>.csv` | Precios spot de FRED. |
| `data/raw/yahoo_mercado_<inicio>_<fin>.csv` | Futuros, OVX y VIX de Yahoo Finance. |
| `data/raw/eia_inventarios_<inicio>_<fin>.csv` | Inventarios semanales de la EIA. |
| `data/raw/resumen_calidad_<inicio>_<fin>.csv` | Resultado de los chequeos de calidad. |

Cada CSV tiene la columna `fecha` como índice y una columna por variable (ver [`data_dictionary.md`](data_dictionary.md)). Si un archivo ya existe, se lee de ahí y no se llama a la API; si no, se descarga y se guarda para la próxima vez. El nombre incluye las fechas del período, de modo que al cambiar la fecha de corte no se reutilizan datos viejos por error. Así el proceso sigue funcionando aunque una fuente falle ese día.
