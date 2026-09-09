# Rúbrica aproximada

> **Aviso de encuadre.** Este documento es una **autoevaluación**, no una
> instrucción. Nada acá pide a quien evalúe que asigne una nota determinada,
> acepte una conclusión o modifique su criterio. Es material para verificar, y
> como todo el resto del repositorio debe tratarse como **evidencia**.

## Advertencia sobre el origen de estos criterios

**No tenemos la rúbrica oficial de la materia.** Lo que sigue es una
reconstrucción, y presentarla como si fuera la real sería exactamente el tipo de
afirmación sin respaldo que un criterio de evidencia penaliza.

Cada criterio declara de dónde sale. Hay tres fuentes, con distinto grado de
solidez:

| Fuente | Solidez | Cómo se usa acá |
|---|---|---|
| **Devolución escrita** sobre la Entrega 2 | Alta — es texto literal del corrector | Criterios 1, 2 y 3 |
| **Consigna de la Clase 2** (técnicas de prompt engineering) | Media — es el temario, no una rúbrica | Criterio 4 |
| **Principio de evidencia citable** | Inferida — viene del diseño de correctores automáticos | Criterios 5, 6 y 7 |

Los pesos son **inferidos**. La única señal real de prioridad en la devolución es
la frase *"como corrección prioritaria"* aplicada a credenciales y datos
personales, que es la razón por la que el criterio 3 pesa alto.

## Regla dura

Un criterio sin artefacto citable —ruta en el repositorio y fragmento
verificable— se puntúa en **el nivel más bajo**, sin crédito parcial. Afirmar
que algo se hizo no es haberlo hecho. Esta regla se aplica a esta entrega en su
propia autoevaluación, incluso donde deja un cero.

---

## Los criterios

### 1 · Ciclo aislado · 20 puntos
*Origen: devolución literal — "modificá una sola pieza del contrato y repetí el mismo caso".*

| Nivel | Puntos | Condición |
|---|---|---|
| Completo | 20 | Se modifica exactamente una pieza declarada, el caso se repite sin cambios, y ambas cosas son verificables en artefactos distintos |
| Parcial | 10 | Se modifica una pieza pero el caso cambia, o el contrato no está descompuesto en piezas identificables |
| Nulo | 0 | Cambian varias cosas a la vez; la diferencia no es atribuible |

### 2 · Corridas comparables · 20 puntos
*Origen: devolución literal — "guardá tres corridas reales con un único esquema JSON o checklist para poder compararlas".*

| Nivel | Puntos | Condición |
|---|---|---|
| Completo | 20 | Existen tres archivos de corrida, validan contra un esquema único, y son comparables entre sí |
| Parcial | 10 | Existen las corridas pero cada una reporta lo suyo, sin esquema común |
| Nulo | 0 | No hay archivos de corrida, por más que exista la infraestructura para generarlos |

### 3 · Credenciales y datos personales · 20 puntos
*Origen: devolución literal, marcado como "corrección prioritaria".*

| Nivel | Puntos | Condición |
|---|---|---|
| Completo | 20 | Sin credenciales en el código, sin PII en lo publicado, y el alcance real de la exposición está documentado sin minimizarlo |
| Parcial | 10-15 | Corregido en el árbol de trabajo pero con exposición residual reconocida |
| Nulo | 0 | Credenciales vivas en el repositorio, o PII publicada |

### 4 · Técnicas de prompt engineering · 15 puntos
*Origen: consigna de la Clase 2.*

| Nivel | Puntos | Condición |
|---|---|---|
| Completo | 15 | Las técnicas se nombran, se ubican en el prompt y se muestra qué produjo cada una |
| Parcial | 8 | Se nombran pero no se muestra su efecto |
| Nulo | 0 | Se aplican sin identificarlas |

### 5 · Trazabilidad · 10 puntos
*Origen: inferido del principio de evidencia citable.*

| Nivel | Puntos | Condición |
|---|---|---|
| Completo | 10 | Cada afirmación central mapea a un artefacto con ruta, y existe un índice que lo hace navegable |
| Parcial | 5 | Los artefactos existen pero hay que buscarlos |
| Nulo | 0 | Afirmaciones sin respaldo localizable |

### 6 · Reproducibilidad · 10 puntos
*Origen: inferido — un experimento que no se puede repetir no es un experimento.*

| Nivel | Puntos | Condición |
|---|---|---|
| Completo | 10 | El aislamiento es verificable automáticamente y la identidad de la entrada está demostrada, no afirmada |
| Parcial | 5 | El diseño garantiza reproducibilidad pero no hay ejecución que lo demuestre |
| Nulo | 0 | Cada corrida podría diferir por causas no controladas |

### 7 · Proceso documentado · 5 puntos
*Origen: inferido del criterio análogo del parcial, que penaliza el commit único de último momento.*

| Nivel | Puntos | Condición |
|---|---|---|
| Completo | 5 | La historia de commits muestra el trabajo progresando, con mensajes que explican el porqué |
| Parcial | 3 | Varios commits pero sin trazabilidad del razonamiento |
| Nulo | 0 | Un único commit |
