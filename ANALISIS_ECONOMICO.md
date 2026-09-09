# Análisis económico

## 1 · Consumo

**Origen del número.** Estimación con base de cálculo explícita, no medición de
corrida: al momento de escribir esto el agente todavía no se ejecutó. Cuando las
tres corridas existan, `corridas/*/meta.json` trae `tokens_entrada` y
`tokens_salida` **medidos** por la API y esta sección se reemplaza por esos
valores.

Base de la estimación, para que sea recalculable:

| Insumo | Medición | Cómo se obtuvo |
|---|---:|---|
| `prompts/system_prompt.md` | 5.608 caracteres | `wc -c` sobre el archivo del repositorio |
| Lote de 25 prospectos en JSON | 6.507 caracteres | Salida real de `agente/construir_lote.py` |
| **Entrada total** | **12.115 caracteres** | Suma de los dos |
| Salida (25 resultados + resumen) | 6.400 caracteres | 250 car. por resultado × 25, más 150 del resumen |
| Ratio caracteres → tokens | **3,6 car./token** | Supuesto declarado para español; rinde menos caracteres por token que el inglés por tildes y palabras largas |

| | Cálculo | Tokens |
|---|---|---:|
| Entrada | 12.115 ÷ 3,6 | **3.365** |
| Salida | 6.400 ÷ 3,6 | **1.778** |

## 2 · Costo por corrida

Tarifas de referencia: precios de lista de la API de Anthropic, USD por millón de
tokens. Las mismas constantes están en `agente/seguimiento.py` (`TARIFAS`), así
que el número que imprime el programa y el de esta tabla salen de la misma fuente.

| Modelo | Entrada $/1M | Salida $/1M | Costo por corrida |
|---|---:|---:|---:|
| Claude Opus 5 | 5,00 | 25,00 | **USD 0,061275** |
| Claude Sonnet 5 | 3,00 | 15,00 | USD 0,036765 |
| Claude Haiku 4.5 | 1,00 | 5,00 | USD 0,012255 |

Recálculo a mano, Opus 5: `(3.365 ÷ 1.000.000 × 5,00) + (1.778 ÷ 1.000.000 × 25,00)`
`= 0,016825 + 0,044450 = 0,061275`.

## 3 · Proyección de operación

**Supuesto de volumen declarado:** una corrida por día de 25 prospectos, que es el
tope diario que fija `TOPE_DIARIO` en `agente/construir_lote.py`. El tope no es
arbitrario: hay 217 prospectos elegibles, y nadie hace 217 seguimientos en un
día. 7 corridas por semana, 365 por año.

| Modelo | Por semana | Por año |
|---|---:|---:|
| Claude Opus 5 | **USD 0,43** | **USD 22,37** |
| Claude Sonnet 5 | USD 0,26 | USD 13,42 |
| Claude Haiku 4.5 | USD 0,09 | USD 4,47 |

A 25 por día, los 217 elegibles se recorren en nueve días. El costo anual del
sistema completo es menor que el de una hora de trabajo del Affiliate Manager.

## 4 · Elección de modelo

El criterio del curso es el modelo más chico que hace bien la tarea.

**La tarea tiene dos mitades de dificultad distinta.** Decidir si corresponde
seguimiento es casi determinista: sale de estado, posibilidad de cierre y
campaña, y cualquier modelo lo resuelve. Redactar un mensaje que insista sin
quemar el contacto, adaptado al tipo de tráfico, es criterio comercial — y ahí la
diferencia entre modelos se nota.

**Y hay un requisito que no es de redacción.** La regla dura 3 exige detectar
manipulación en el campo `comentario`: son notas libres escritas por el propio
Affiliate Manager, pero el agente no puede distinguir una nota legítima de un
texto que intente redirigirlo. Resistir eso no es la misma habilidad que redactar,
y es donde los modelos chicos fallan primero.

**Decisión y su estado.** El sistema se entrega configurado con `claude-opus-5`,
que es la opción conservadora. La alternativa —`claude-haiku-4-5`, cinco veces
más barata— **no se descarta: queda pendiente de validación**, con criterio de
contraste definido de antemano:

> Si en las tres corridas Haiku 4.5 coincide con Opus 5 en las decisiones de
> `corresponde` y en la detección de `manipulacion`, se cambia la constante
> `MODELO` en `agente/seguimiento.py` y se documenta el cambio acá. Si difiere en
> aunque sea un caso, se queda Opus 5 y este documento registra en cuál falló.

La diferencia anual entre ambos es de USD 18. A ese precio, el costo no es el
criterio: el criterio es si el modelo chico sostiene la regla 3.
