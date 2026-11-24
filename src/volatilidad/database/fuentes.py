"""Descarga y caché de las fuentes de datos del proyecto (FRED, Yahoo Finance y EIA)."""

import os
from getpass import getpass

import pandas as pd
import requests

SERIES_FRED = {"DCOILWTICO": "wti_spot", "DCOILBRENTEU": "brent_spot"}
TICKERS_YF = {"CL=F": "wti_fut", "BZ=F": "brent_fut", "^OVX": "ovx", "^VIX": "vix"}
URL_EIA = "https://api.eia.gov/v2/petroleum/stoc/wstk/data/"
SERIE_EIA = "WCESTUS1"


def leer_clave(nombre):
    """Lee una API key de las variables de entorno y, si no está, la pide por consola."""
    clave = os.environ.get(nombre)
    if clave:
        return clave
    return getpass(f"Ingrese {nombre}: ")


def cargar_con_cache(nombre, descargar, cache_dir, fecha_inicio, fecha_fin):
    """Lee el CSV de la caché si existe. Si no, llama a `descargar()` y guarda el resultado.

    El nombre del archivo incluye el período, para no reutilizar datos de otra fecha de corte.
    """
    os.makedirs(cache_dir, exist_ok=True)
    ruta = os.path.join(cache_dir, f"{nombre}_{fecha_inicio}_{fecha_fin}.csv")
    if os.path.exists(ruta):
        print(f"{nombre}: leído de la caché")
        return pd.read_csv(ruta, index_col=0, parse_dates=True)
    print(f"{nombre}: consultando la API")
    df = descargar()
    df.to_csv(ruta)
    return df


def descargar_fred(fecha_inicio, fecha_fin):
    """Precios spot diarios de WTI y Brent desde la API de FRED."""
    from fredapi import Fred

    fred = Fred(api_key=leer_clave("FRED_API_KEY"))
    series = {
        nombre: fred.get_series(codigo, observation_start=fecha_inicio, observation_end=fecha_fin)
        for codigo, nombre in SERIES_FRED.items()
    }
    df = pd.DataFrame(series)
    df.index.name = "fecha"
    return df


def descargar_yahoo(fecha_inicio, fecha_fin):
    """Futuros continuos de WTI y Brent y los índices OVX y VIX (apertura, máximo, mínimo, cierre)."""
    import yfinance as yf

    # En yfinance la fecha final es excluyente: se suma un día para incluir fecha_fin.
    fin = (pd.Timestamp(fecha_fin) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    partes = []
    for ticker, nombre in TICKERS_YF.items():
        h = yf.Ticker(ticker).history(start=fecha_inicio, end=fin, auto_adjust=False)
        h = h[["Open", "High", "Low", "Close"]]
        h.columns = [f"{nombre}_{c.lower()}" for c in h.columns]
        h.index = h.index.tz_localize(None).normalize()
        partes.append(h)
    df = pd.concat(partes, axis=1)
    df.index.name = "fecha"
    return df


def descargar_eia(fecha_inicio, fecha_fin):
    """Inventarios semanales de crudo de EE.UU. sin reserva estratégica (miles de barriles), API v2 de la EIA."""
    params = {
        "api_key": leer_clave("EIA_API_KEY"),
        "frequency": "weekly",
        "data[0]": "value",
        "facets[series][]": SERIE_EIA,
        "start": fecha_inicio,
        "end": fecha_fin,
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "length": 5000,
    }
    r = requests.get(URL_EIA, params=params, timeout=30)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["response"]["data"])
    df["fecha"] = pd.to_datetime(df["period"])
    df["inv_crudo"] = pd.to_numeric(df["value"])
    return df.set_index("fecha")[["inv_crudo"]]


def resumen_calidad(df):
    """Rango de fechas, valores válidos y nulos, mínimo y máximo por columna."""
    return pd.DataFrame({
        "inicio": df.apply(lambda s: s.first_valid_index()),
        "fin": df.apply(lambda s: s.last_valid_index()),
        "validos": df.count(),
        "nulos": df.isna().sum(),
        "minimo": df.min(),
        "maximo": df.max(),
    })
