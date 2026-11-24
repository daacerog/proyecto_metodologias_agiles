# Diccionario de datos

Los rangos corresponden a la carga con fecha de corte 2026-11-23 (período 2007-01-01 a 2026-11-23), tomados del resumen de calidad que genera el script de carga (`data/raw/resumen_calidad_2007-01-01_2026-11-23.csv`). Cada fuente publica con un rezago distinto, por eso las fechas finales no coinciden.

## Base de datos 1: Precios spot (FRED)

Precios spot diarios del barril de petróleo, publicados por FRED a partir de datos de la EIA. Archivo: `data/raw/fred_spot_<inicio>_<fin>.csv`.

| Variable | Descripción | Tipo de dato | Rango/Valores posibles | Fuente de datos |
| --- | --- | --- | --- | --- |
| fecha | Fecha de la observación (índice) | datetime | 2007-01-02 a 2026-11-17 | FRED |
| wti_spot | Precio spot del WTI en USD por barril | float | -36.98 a 145.31 | FRED (`DCOILWTICO`) |
| brent_spot | Precio spot del Brent en USD por barril | float | 9.12 a 143.95 | FRED (`DCOILBRENTEU`) |

## Base de datos 2: Futuros e índices de volatilidad (Yahoo Finance)

Futuros continuos de WTI y Brent e índices de volatilidad implícita, en frecuencia diaria, con apertura (`_open`), máximo (`_high`), mínimo (`_low`) y cierre (`_close`). Archivo: `data/raw/yahoo_mercado_<inicio>_<fin>.csv`.

| Variable | Descripción | Tipo de dato | Rango/Valores posibles | Fuente de datos |
| --- | --- | --- | --- | --- |
| fecha | Fecha de la observación (índice), sin zona horaria | datetime | 2007-01-02 a 2026-11-23 | Yahoo Finance |
| wti_fut_open | Futuro continuo del WTI, apertura, USD por barril | float | -14.00 a 145.19 | Yahoo Finance (`CL=F`) |
| wti_fut_high | Futuro continuo del WTI, máximo, USD por barril | float | 13.69 a 147.27 | Yahoo Finance (`CL=F`) |
| wti_fut_low | Futuro continuo del WTI, mínimo, USD por barril | float | -40.32 a 143.22 | Yahoo Finance (`CL=F`) |
| wti_fut_close | Futuro continuo del WTI, cierre, USD por barril | float | -37.63 a 145.29 | Yahoo Finance (`CL=F`) |
| brent_fut_open | Futuro continuo del Brent, apertura, USD por barril (desde 2007-07-30) | float | 19.56 a 146.08 | Yahoo Finance (`BZ=F`) |
| brent_fut_high | Futuro continuo del Brent, máximo, USD por barril | float | 21.27 a 147.43 | Yahoo Finance (`BZ=F`) |
| brent_fut_low | Futuro continuo del Brent, mínimo, USD por barril | float | 16.00 a 144.27 | Yahoo Finance (`BZ=F`) |
| brent_fut_close | Futuro continuo del Brent, cierre, USD por barril | float | 19.33 a 146.08 | Yahoo Finance (`BZ=F`) |
| ovx_open | Volatilidad implícita del petróleo a 30 días (CBOE), apertura, % anualizado (desde 2007-05-10) | float | 14.67 a 234.66 | Yahoo Finance (`^OVX`) |
| ovx_high | OVX, máximo, % anualizado | float | 14.87 a 517.19 | Yahoo Finance (`^OVX`) |
| ovx_low | OVX, mínimo, % anualizado | float | 13.93 a 213.59 | Yahoo Finance (`^OVX`) |
| ovx_close | OVX, cierre, % anualizado | float | 14.50 a 325.15 | Yahoo Finance (`^OVX`) |
| vix_open | Volatilidad implícita del S&P 500 a 30 días (CBOE), apertura, % anualizado | float | 9.01 a 82.69 | Yahoo Finance (`^VIX`) |
| vix_high | VIX, máximo, % anualizado | float | 9.31 a 89.53 | Yahoo Finance (`^VIX`) |
| vix_low | VIX, mínimo, % anualizado | float | 8.56 a 72.76 | Yahoo Finance (`^VIX`) |
| vix_close | VIX, cierre, % anualizado | float | 9.14 a 82.69 | Yahoo Finance (`^VIX`) |

## Base de datos 3: Inventarios de crudo (EIA)

Inventarios semanales de crudo de EE.UU., sin contar la reserva estratégica. Archivo: `data/raw/eia_inventarios_<inicio>_<fin>.csv`.

| Variable | Descripción | Tipo de dato | Rango/Valores posibles | Fuente de datos |
| --- | --- | --- | --- | --- |
| fecha | Fecha de corte semanal del reporte (índice) | datetime | 2007-01-05 a 2026-11-13 | EIA |
| inv_crudo | Inventarios de crudo de EE.UU. sin reserva estratégica, en miles de barriles | int | 265,361 a 540,722 | EIA API v2 (`WCESTUS1`) |

- **Variable**: nombre de la variable.
- **Descripción**: breve descripción de la variable.
- **Tipo de dato**: tipo de dato que contiene la variable.
- **Rango/Valores posibles**: rango o valores que puede tomar la variable.
- **Fuente de datos**: fuente de los datos de la variable.
