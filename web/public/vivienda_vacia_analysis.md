# Analisis vivienda semi-vacia Balears (Censo 2021)
**Fuente**: INE Censo 2021 - Tabla 59532 (percentiles consumo electrico por distrito censal) y Tabla 59531 (viviendas totales por municipio).
**Limitacion importante**: El Censo 2021 da un snapshot anual, NO serie temporal. Los percentiles no distinguen invierno vs verano. Se usan como PROXY de la heterogeneidad de uso:
- `p10` bajo: hay casas que consumen muy poco. Podrian ser vacias, segunda residencia estival, o mayores que apenas usan luz.
- `p50` (mediana): el hogar tipico del distrito.
- `ratio_p10_p50` bajo (<0.4): cola izquierda larga = mas casas con consumo muy bajo = potencial vivienda semi-vacia.
- `ratio_p10_p50` alto (~0.7+): distribucion normal = la mayoria de casas se parecen.

## Metodologia
Para cada distrito censal:
1. Se extrae p10/p25/p50/p75/p90 del consumo anual de electricidad (kWh)
2. Se calcula `ratio_p10_p50 = p10 / p50`. Bajo = distribucion asimetrica con cola de bajo consumo
3. Se cruza con listings de Airbnb del Inside Airbnb (junio 2026) por distrito
4. Se cruza con viviendas totales del municipio (Censo 2021) para normalizar

## Resultados globales
- **Distritos analizados**: 116
- **ratio p10/p50 mediana**: 0.289 (Q1: 0.246, Q3: 0.336)
- **Distritos con ratio < 0.4** (posible concentracion de vivienda semi-vacia): **103 de 116 (89%)**
- **Correlacion airbnb/1000viv vs ratio p10/p50**: 0.131
  > Correlacion debil: no hay patron claro entre Airbnb y vacio residencial.

## Top 10 distritos con MENOR ratio p10/p50 (mas cola de bajo consumo)
Estos distritos tienen el percentil 10 mas bajo en relacion a la mediana. Indica que hay un grupo de casas con consumo electrico muy bajo.

| Distrito | p10 (kWh) | p50 (kWh) | ratio p10/p50 | Listings Airbnb | Airbnb/1000 viv |
|---|---:|---:|---:|---:|---:|
| 0704501 Puigpunyent distrito 01 | 111 | 3,615 | 0.03 | 39 | 30.6 |
| 0705405 SantaEulÃ riadesRiu distrito 05 | 119 | 3,533 | 0.03 | 0 | 0.0 |
| 0702403 Formentera distrito 03 | 574 | 3,038 | 0.19 | 0 | 0.0 |
| 0790201 MigjornGran(Es) distrito 01 | 535 | 2,796 | 0.19 | 45 | 38.1 |
| 0703307 Manacor distrito 07 | 493 | 2,424 | 0.20 | 149 | 5.2 |
| 0705102 SantLlorenÃ§desCardassar distrito 02 | 525 | 2,538 | 0.21 | 165 | 25.3 |
| 0705403 SantaEulÃ riadesRiu distrito 03 | 1,006 | 4,826 | 0.21 | 0 | 0.0 |
| 0701106 CalviÃ  distrito 06 | 542 | 2,569 | 0.21 | 44 | 1.2 |
| 0702402 Formentera distrito 02 | 475 | 2,185 | 0.22 | 0 | 0.0 |
| 0700503 Andratx distrito 03 | 469 | 2,146 | 0.22 | 32 | 2.7 |

## Top 10 distritos con MAS presion Airbnb (per capita)
| Distrito | Listings Airbnb | Viviendas | Airbnb/1000 viv | ratio p10/p50 |
|---|---:|---:|---:|---:|
| 0700901 BÃºger distrito 01 | 141 | 888 | 158.8 | 0.28 |
| 0703701 Mercadal(Es) distrito 01 | 690 | 7,208 | 95.7 | 2.36 |
| 0704203 PollenÃ§a distrito 03 | 1239 | 13,772 | 90.0 | 0.23 |
| 0705502 SantaMargalida distrito 02 | 594 | 8,414 | 70.6 | 2.41 |
| 0706301 Valldemossa distrito 01 | 103 | 1,483 | 69.5 | 0.24 |
| 0705801 Selva distrito 01 | 199 | 2,990 | 66.6 | 0.23 |
| 0701401 Capdepera distrito 01 | 518 | 9,119 | 56.8 | 0.22 |
| 0703901 Muro distrito 01 | 276 | 5,092 | 54.2 | 0.25 |
| 0701201 Campanet distrito 01 | 97 | 1,911 | 50.8 | 2.62 |
| 0705901 Salines(Ses) distrito 01 | 241 | 4,922 | 49.0 | 0.29 |

## Lectura del hallazgo

**No podemos demostrar aumento de demanda invierno vs verano** con estos datos (es un snapshot del ano 2021, no serie temporal).

**Lo que SI podemos hacer**: usar `ratio p10_p50` como **proxy de heterogeneidad de uso**. La hipotesis es que:
- En zonas donde la mayoria de casas se usan como segunda residencia estival, la cola izquierda del consumo electrico es mas larga (ratio bajo).
- En zonas de uso residencial estable, la distribucion es mas homogenea (ratio alto).

Para comparar **realmente invierno vs verano** haria falta:
- Serie temporal de REE (API rota para geo_limit=baleares)
- O datos del Govern Balear / CNMC con desglose mensual
- O microdatos del Censo 2021 (no accesibles publicamente con granularidad mensual)

## Recomendaciones para profundizar

1. **Solicitar datos** a la Conselleria de Transicio Energetica del Govern Balear
2. **Esperar a que REE arregle** la API para `geo_limit=baleares` (reporte en su portal)
3. **Cruzar con datos de agua** (Conselleria de Medi Ambient): una vivienda vacia consume menos agua, mismo patron
