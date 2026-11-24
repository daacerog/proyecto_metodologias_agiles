# Pronóstico de la volatilidad del petróleo WTI y Brent con Deep Learning

Proyecto aplicado del Programa de Formación en Machine Learning y Data Science (MLDS) de la Universidad Nacional de Colombia, desarrollado con la metodología TDSP (Team Data Science Process).

## Descripción

El proyecto pronostica la **volatilidad realizada** del barril de petróleo WTI y Brent a **1, 5 y 22 días hábiles**. El beneficiario es la mesa de riesgo de una empresa productora y comercializadora de crudo, que usa la volatilidad esperada para fijar su límite de pérdida (VaR) y decidir cuánta exposición cubrir con futuros.

Se comparan modelos de Deep Learning (MLP, LSTM, GRU, TCN, Transformer encoder y un híbrido GARCH-LSTM) contra las referencias econométricas estándar GARCH y HAR-RV. El resultado queda abierto: si los modelos econométricos superan al Deep Learning, también es un hallazgo válido.

El detalle está en el [Project Charter](docs/business_understanding/project_charter.md).

## Equipo

- Erika Katherin Olivera Parrado
- Dairo Andres Acero Guerrero
- Jhon Anderson Bermudez Hurtado

**Tutor:** Juan Sebastian Malagon

## Datos

Series de tiempo financieras públicas desde 2007, obtenidas por API:

| Fuente | Series | Frecuencia |
|---|---|---|
| [FRED](https://fred.stlouisfed.org/) | Precios spot de WTI y Brent | Diaria |
| [Yahoo Finance](https://finance.yahoo.com/) | Futuros continuos de WTI y Brent (OHLC), índices de volatilidad implícita OVX y VIX | Diaria |
| [EIA](https://www.eia.gov/opendata/) | Inventarios de crudo de EE.UU. | Semanal |

Más información en la [definición de los datos](docs/data/data_definition.md) y el [diccionario de datos](docs/data/data_dictionary.md).

## Estructura del repositorio

```
├── docs/
│   ├── business_understanding/   # Project Charter
│   ├── data/                     # Definición, diccionario y resumen de los datos
│   ├── modeling/                 # Modelos baseline y reporte de modelos
│   ├── deployment/               # Documentación de despliegue
│   └── acceptance/               # Reporte de salida
├── scripts/                      # Scripts que se ejecutan, uno por etapa
│   ├── data_acquisition/         # Carga de datos
│   ├── eda/
│   ├── preprocessing/
│   ├── training/
│   └── evaluation/
├── src/volatilidad/              # Paquete de Python con la implementación
│   └── database/                 # Descarga y caché de las fuentes de datos
├── .env.example                  # Plantilla de las API keys
└── pyproject.toml
```

## Cómo ejecutarlo

1. Crear el entorno e instalar el paquete:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. Configurar las API keys. FRED y EIA requieren una clave gratuita:
   - FRED: https://fred.stlouisfed.org/docs/api/api_key.html
   - EIA: https://www.eia.gov/opendata/register.php

   ```bash
   cp .env.example .env
   # editar .env y poner las claves después del "="
   ```

   El archivo `.env` no se sube al repositorio.

3. Descargar los datos:

   ```bash
   python scripts/data_acquisition/main.py
   ```

   Los datos se guardan como CSV en `data/raw/` (no se sube al repositorio). Si un archivo ya existe, se lee de ahí y no se vuelve a consultar la API. Para usar otra fecha de corte: `--fecha-fin AAAA-MM-DD`.

## Avance

| Etapa | Fechas | Estado |
|---|---|---|
| 1. Entendimiento del negocio y carga de datos | 23 al 29 de noviembre de 2026 | En curso |
| 2. Preprocesamiento, modelos de referencia y primeros modelos de DL | 30 de noviembre al 6 de diciembre de 2026 | Pendiente |
| 3. Modelamiento avanzado | 7 al 13 de diciembre de 2026 | Pendiente |
| 4. Evaluación y entrega final | 14 al 20 de diciembre de 2026 | Pendiente |

---

Estructura basada en la [plantilla TDSP](https://github.com/mindlab-unal/tdsp_template) del programa MLDS.
