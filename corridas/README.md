# Corridas

Cada corrida es una carpeta cuyo nombre combina la fecha y el número de lote del
día. Las tres de esta entrega son `2026-09-10-1`, `2026-09-10-2` y `2026-09-10-3`,
y cada una contiene exactamente tres archivos:

| Ruta (ejemplo de la primera corrida) | Contenido |
|---|---|
| [`2026-09-10-1/entrada.json`](2026-09-10-1/entrada.json) | El lote que recibió el agente, seudonimizado |
| [`2026-09-10-1/salida.json`](2026-09-10-1/salida.json) | El JSON que devolvió, **sin edición cosmética** |
| [`2026-09-10-1/meta.json`](2026-09-10-1/meta.json) | Fecha, modelo, tokens medidos por la API, costo y `enviados: 0` |

La fecha vive dentro de cada `meta.json`, además del nombre de la carpeta.


La fecha vive en `meta.json`, además del nombre de la carpeta.

## Estado

**Las tres corridas están generadas**, el 10/9/2026:

| Corrida | Prospectos | Tokens E/S | Costo |
|---|---:|---:|---:|
| `2026-09-10-1` | 25 (del #1) | 6.279 / 6.992 | USD 0,206195 |
| `2026-09-10-2` | 25 (del #26) | 6.444 / 6.075 | USD 0,184095 |
| `2026-09-10-3` | 25 (del #51) | 6.433 / 5.790 | USD 0,176915 |

Los tres lotes son **disjuntos**: 75 prospectos sin repetir, verificado por
intersección de identificadores. El desplazamiento (`--desde`) reproduce la
operación real, donde el lote diario avanza sobre la lista ordenada.

Las tres salidas satisfacen el formato declarado en el contrato, validado campo
por campo: mismos campos, identificadores con formato `AF-` de ocho hexadecimales,
y ningún mensaje por encima de los 500 caracteres.

Ninguna envió nada: `enviados: 0` en los tres `meta.json`.

No se incluyen corridas simuladas. Una corrida inventada invalidaría el análisis
económico —que toma sus tokens de `meta.json`— y convertiría el resto del trabajo
en material sospechoso.

## Cómo generarlas

```bash
python3 agente/construir_lote.py --salida corridas/$(date +%F)/entrada.json
python3 agente/seguimiento.py --entrada corridas/$(date +%F)/entrada.json
```

Tres corridas con `--limite` distinto, o en tres días distintos a medida que el
tope diario avanza sobre los 217 elegibles, dan tres entradas reales distintas.
Ninguna corrida envía mensajes: `meta.json` registra `enviados: 0` en todas.

El lote publicado no contiene razón social, @handle ni email: solo seudónimo y
atributos de negocio. Por eso estas corridas **sí son publicables**, a diferencia
de las del agente de triage anterior, cuyo insumo era el texto de mensajes
privados.


## El insumo

La planilla de origen no se versiona. Su especificación completa y el artefacto
que acredita su consumo están en [`INSUMO.md`](INSUMO.md).
