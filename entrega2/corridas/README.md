# Las tres corridas

Un único esquema (`esquema.json`) al que deben validar las tres. Sin esquema
común no hay comparación posible: cada corrida reportaría lo que le conviene.

## Protocolo

**Una sola lectura de la realidad.** `correr_ciclos.py` consulta Telegram una vez
y los tres ciclos consumen ese mismo snapshot. Por eso `hash_entrada` es idéntico
en las tres **por construcción**, no por coincidencia. Si alguien corriera cada
ciclo por separado, cualquier diferencia observada podría venir de que llegaron
mensajes distintos en el medio.

**Ninguna corrida envía mensajes.** `envios_reales` es `0` en las tres, y el
validador lo exige. Suprimir el efecto saliente es el control del experimento:
lo que se compara es *qué publica* cada contrato, y eso se computa sin
escribirle a 211 afiliados.

**C2 y C3 comparten el caso.** Mismo `hash_prompt`. Es la condición de
aislamiento: si el caso cambiara, la diferencia de salida no sería atribuible a
la pieza del contrato.

## Qué mide el checklist

Seis criterios, iguales para las tres:

| Criterio | De dónde sale |
|---|---|
| `flujo_numerado` | P2, regla 1 |
| `manejo_errores` | P2, regla 2 |
| `secretos_fuera_del_codigo` | P2, regla 3 |
| `advierte_riesgo_tos` | P2, regla 4 |
| `salida_persistente` | P5 |
| `sin_pii_publicada` | P2, regla 3 (sólo en v3) |

Los primeros cinco existen desde v1. El sexto es el que introduce C3, y es la
única fila donde C2 y C3 pueden diferir por diseño.

## Cómo se generan

```bash
source .env && python3 correr_ciclos.py
python3 validar.py
```

`validar.py` no sólo chequea el esquema: verifica el aislamiento (misma entrada,
mismo caso en C2/C3, pieza distinta) y que la corrección de privacidad haya
tomado efecto. Falla ruidosamente si el experimento no es válido.

## Estado

**Las tres corridas todavía no están generadas.** Dependen de que se roten las
credenciales de Telegram expuestas y se rehaga el login — ver la nota en
`../salida_1_iteracion1.md`. Rotar invalida la sesión actual, así que cualquier
corrida hecha antes de rotar habría que rehacerla.

No se incluyen corridas de ejemplo ni simuladas: una corrida inventada
invalidaría la comparación entera.

## Sobre `payload_publicable` en C2

El registro de C2 tiene que probar que ese contrato publicaba `handle`, `nombre`
y `mensaje` — pero no puede publicarlos. Se guarda **redactado**: se conserva la
forma (los nombres de campo) y se reemplaza cada valor por un marcador de tipo.

La evidencia cruda queda en `_local_corrida_c2.json`, fuera de git por
`.gitignore`. Documentar un problema de privacidad reproduciéndolo sería
repetirlo.
