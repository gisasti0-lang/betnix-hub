# El insumo externo y por qué no está en el repositorio

## Declaración de ausencia

`Betnix_Outreach_2026.xlsx` **no se versiona**, y es deliberado: contiene la razón
social, el @handle de Telegram y el email de 288 contactos comerciales reales.
Publicarlo sería exactamente lo que la corrección de la Entrega 2 prohibió.

Vive en `~/Documents/Betnix Partners/` en la máquina del Affiliate Manager.

## Especificación, para que un tercero lo reponga

| | |
|---|---|
| **Formato** | `.xlsx`, una sola hoja activa |
| **Volumen** | **288 filas con datos** más la fila de encabezados |
| **Columnas** | **10**, de la A a la J |

| Col | Encabezado | Uso en el sistema |
|---|---|---|
| A | Empresa / Partner | Se lee y **no** se publica |
| B | Contacto (Email / TG) | Se lee y se convierte en seudónimo `AF-`; no se publica |
| C | Canal | `Telegram` o `Email` |
| D | Semana | Tanda de contacto original → campo `campana` |
| E | GEO | → campo `geo` |
| F | Tipo de Tráfico | → campo `tipo_trafico` |
| **G** | **Estado** | Se mapea al enum del contrato. **Es la G, no la F** |
| H | Posibilidad de Cierre | `Verde` / `Amarillo` / `Rojo` / `—` |
| I | Comentario | → campo `comentario`, truncado a 300 caracteres |
| J | Notas / Detalle | No se usa |

Distribución al 10/9/2026: **211 filas con canal Telegram** y 77 con Email; de las
Telegram, **196 tienen un @handle válido**. Por estado: 129 `Contacted`, 56 `Sin
respuesta`, 34 `Not relevant`, 15 `already working`, 11 `Not replying`, 10
`REBOTÓ`, 6 `No se pudo cerrar`, 6 `Launching`.

## Artefacto que acredita el consumo

[`inventario_insumo.json`](inventario_insumo.json) lo genera el mismo lector que
usan las corridas (`agente/construir_lote.py`) y registra las magnitudes medidas
sobre el archivo real. Su contenido no podría haberse producido sin haberlo leído.

Dos magnitudes independientes que un corrector puede contrastar contra esta
especificación:

| Magnitud | Declarado acá | En `inventario_insumo.json` |
|---|---:|---:|
| Filas con datos | 288 | `filas_con_datos` |
| Columnas | 10 | `columnas` |

Y una tercera, contra las corridas: los tres lotes suman 75 prospectos tomados de
los **217 elegibles**, que es lo que queda al descartar estados no elegibles y
posibilidad `Rojo` sobre las 288 filas.
