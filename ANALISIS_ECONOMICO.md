# Análisis económico

## 1 · Consumo medido

**Origen del número: medición real de tres corridas**, no estimación. Los valores
salen de `corridas/*/meta.json`, que los toma del campo `usage` que devuelve la
API en cada respuesta.

| Corrida | Tokens entrada | Tokens salida | Costo |
|---|---:|---:|---:|
| `2026-09-10-1` | 6.279 | 6.992 | USD 0,206195 |
| `2026-09-10-2` | 6.444 | 6.075 | USD 0,184095 |
| `2026-09-10-3` | 6.433 | 5.790 | USD 0,176915 |
| **Promedio** | **6.385** | **6.286** | **USD 0,189068** |

Las tres corridas juntas costaron **USD 0,5672**.

### Lo que la medición corrigió de la estimación

La versión anterior de este documento estimaba 3.365 tokens de entrada y 1.778 de
salida. Los reales son 6.385 y 6.286: la entrada casi al doble, **la salida casi
cuatro veces más**.

Dos causas, y la segunda es la importante:

1. El ratio de 3,6 caracteres por token era optimista para español con JSON
   estructurado; el real ronda 1,9.
2. **El razonamiento adaptativo de Claude Opus 5 se factura como tokens de
   salida.** La estimación contaba solo el JSON visible. Es el error más caro de
   los dos, porque la salida cuesta cinco veces más que la entrada.

Ese mismo error tuvo una consecuencia operativa antes que económica: con
`max_tokens = 8000` la primera corrida se truncó a mitad de un string y Pydantic
rechazó el JSON. El techo se subió a 16.000 y el esfuerzo se fijó en `medium`.

## 2 · Costo por corrida

Tarifas de referencia: precios de lista de la API de Anthropic, USD por millón de
tokens. Las mismas constantes están en `agente/seguimiento.py` (`TARIFAS`).

| Modelo | Entrada $/1M | Salida $/1M | Costo por corrida |
|---|---:|---:|---:|
| Claude Opus 5 | 5,00 | 25,00 | **USD 0,189068** |
| Claude Sonnet 5 | 3,00 | 15,00 | USD 0,113441 |
| Claude Haiku 4.5 | 1,00 | 5,00 | USD 0,037814 |

Recálculo a mano, Opus 5: `(6.385 ÷ 1.000.000 × 5,00) + (6.286 ÷ 1.000.000 × 25,00)`
`= 0,031925 + 0,157150 = 0,189075`. La diferencia en el sexto decimal con la
tabla viene de que el promedio se redondea acá y no en el programa.

## 3 · Proyección de operación

**Supuesto de volumen declarado:** una corrida diaria de 25 prospectos, que es el
`TOPE_DIARIO` de `agente/construir_lote.py`. 7 corridas por semana, 365 por año.

| Modelo | Por semana | Por año |
|---|---:|---:|
| Claude Opus 5 | **USD 1,32** | **USD 69,01** |
| Claude Sonnet 5 | USD 0,79 | USD 41,41 |
| Claude Haiku 4.5 | USD 0,26 | USD 13,80 |

Con 217 prospectos elegibles y 25 por día, la lista se recorre en nueve días.
El costo anual sigue siendo menor al de dos horas de trabajo del Affiliate
Manager, pero **es tres veces el que proyectaba la estimación** (USD 22,37). Una
estimación que subestima por tres no sirve para decidir; por eso la rúbrica
prefiere medición.

## 4 · Elección de modelo

El criterio del curso es el modelo más chico que hace bien la tarea.

**La tarea tiene dos mitades de dificultad distinta.** Decidir si corresponde
seguimiento resultó ser casi determinista: en las tres corridas el agente
respondió `corresponde: true` en los 75 casos. Eso no es un defecto del modelo
sino del reparto: el filtrado real lo hace el código —descarta estados no
elegibles y posibilidad Rojo— así que al agente le llegan solo candidatos
legítimos. La decisión que queda es la prioridad, y ahí sí discriminó: 6 altas,
46 medias y 23 bajas, con motivos ligados al estado de cada fila.

La otra mitad —redactar sin quemar el contacto, adaptado al tipo de tráfico— es
criterio comercial. En la corrida 1 el agente redactó en portugués para un
contacto con GEO `PT` sin que ninguna regla se lo pidiera.

**Y hay un requisito que no es de redacción.** La regla dura 3 exige detectar
manipulación en el campo `comentario`. En estas tres corridas no apareció ningún
caso, así que **la capacidad quedó sin ejercitar**: no hay evidencia de que Opus 5
sea necesario para eso, ni de que Haiku no alcance.

**Decisión y su estado.** El sistema se entrega con `claude-opus-5`. La
alternativa —`claude-haiku-4-5`, cinco veces más barata, USD 13,80 anuales contra
69,01— **no está descartada: está pendiente de una prueba que estas corridas no
pudieron hacer.** El criterio de contraste queda definido:

> Correr los mismos tres lotes con Haiku 4.5 e inyectar en un cuarto lote de
> control al menos un `comentario` con intento de manipulación. Si Haiku coincide
> con Opus 5 en las 75 prioridades y detecta el caso inyectado, se cambia la
> constante `MODELO` y se documenta acá. Si difiere, se registra en cuál falló.

Lo honesto hoy es que el modelo grande se eligió por precaución sobre un riesgo
que todavía no se observó, y que eso cuesta USD 55 al año.
