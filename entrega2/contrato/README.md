# El contrato y sus piezas

Para poder aislar un ciclo hace falta primero declarar qué es "el contrato" y en
qué piezas se descompone. Sin esa descomposición, "cambiar una sola cosa" no es
verificable.

El contrato de este proyecto es el **system prompt**, y tiene cinco piezas:

| Pieza | Nombre | Qué fija |
|-------|--------|----------|
| **P1** | Identidad | El rol que asume el agente (role prompting) |
| **P2** | Reglas | Las 5 restricciones de comportamiento, numeradas |
| **P3** | Contexto | El proyecto, el Excel, los 211 afiliados |
| **P4** | Ejemplo | El few-shot de pedido → respuesta esperada |
| **P5** | Formato | Qué debe contener la salida final |

## Regla del experimento

En cada ciclo se modifica **una sola pieza**, y el caso de prueba
(`user_prompt.md`) se mantiene idéntico. Todo lo que cambie en la salida es
atribuible a esa pieza y a ninguna otra.

| Ciclo | Contrato | Pieza modificada | Caso |
|-------|----------|------------------|------|
| C1 | `v1.md` | — (línea base) | Iteración 1 |
| C2 | `v2.md` | **P5** (formato de salida) | Iteración 2 |
| C3 | `v3.md` | **P2, regla 3** (manejo de credenciales y datos) | Iteración 2, **sin cambios** |

C3 es el ciclo aislado: repite el **mismo caso que C2**, palabra por palabra. La
única variable es la regla 3.
