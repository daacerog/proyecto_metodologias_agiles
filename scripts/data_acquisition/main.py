"""Carga de datos del proyecto: descarga (o lee de la caché) FRED, Yahoo Finance y EIA y revisa su calidad.

Uso, desde la raíz del repositorio:
    python scripts/data_acquisition/main.py
    python scripts/data_acquisition/main.py --fecha-fin 2026-11-20
"""

import argparse
import os
from pathlib import Path

import pandas as pd

from volatilidad.database.fuentes import (
    cargar_con_cache,
    descargar_eia,
    descargar_fred,
    descargar_yahoo,
    resumen_calidad,
)

RAIZ = Path(__file__).resolve().parents[2]
FECHA_INICIO = "2007-01-01"
FECHA_FIN = "2026-11-23"


def cargar_env(ruta):
    """Carga variables KEY=VALOR de un archivo .env sin sobrescribir las que ya existen."""
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))


def main():
    parser = argparse.ArgumentParser(description="Carga de datos de volatilidad del petróleo")
    parser.add_argument("--fecha-inicio", default=FECHA_INICIO)
    parser.add_argument("--fecha-fin", default=FECHA_FIN)
    parser.add_argument("--cache-dir", default=str(RAIZ / "data" / "raw"))
    args = parser.parse_args()

    cargar_env(RAIZ / ".env")
    ini, fin, cache = args.fecha_inicio, args.fecha_fin, args.cache_dir

    spot = cargar_con_cache("fred_spot", lambda: descargar_fred(ini, fin), cache, ini, fin)
    mercado = cargar_con_cache("yahoo_mercado", lambda: descargar_yahoo(ini, fin), cache, ini, fin)
    inventarios = cargar_con_cache("eia_inventarios", lambda: descargar_eia(ini, fin), cache, ini, fin)

    tablas = {"spot": spot, "mercado": mercado, "inventarios": inventarios}
    for nombre, d in tablas.items():
        print(f"{nombre}: filas={len(d)}, duplicados={d.index.duplicated().sum()}, "
              f"ordenado={d.index.is_monotonic_increasing}")

    resumen = pd.concat([resumen_calidad(d) for d in tablas.values()])
    ruta_resumen = Path(cache) / f"resumen_calidad_{ini}_{fin}.csv"
    resumen.to_csv(ruta_resumen)
    with pd.option_context("display.width", 140, "display.max_columns", None):
        print(resumen)
    print(f"Resumen de calidad guardado en: {ruta_resumen}")


if __name__ == "__main__":
    main()
