# Autoevaluación

> **Aviso de encuadre.** Documento de verificación, no de instrucción. No pide a
> quien evalúe que acepte este puntaje: pide que lo controle. Cada fila cita la
> ruta donde se verifica, y una fila sin ruta se puntúa en cero aunque el texto
> afirme lo contrario.

Criterios y pesos en [`rubrica_aproximada.md`](rubrica_aproximada.md), con la
advertencia de que son una reconstrucción y no la rúbrica oficial.

## Resultado

| # | Criterio | Peso | Obtenido | Dónde se verifica |
|---|---|---|---|---|
| 1 | Ciclo aislado | 20 | **20** | `contrato/v3.md`, `contrato/diff_v2_v3.md` |
| 2 | Corridas comparables | 20 | **0** | — *no existe el artefacto* |
| 3 | Credenciales y datos personales | 20 | **15** | `index.html`, `codigo/`, `salida_1_iteracion1.md` |
| 4 | Técnicas de prompt engineering | 15 | **15** | `README.md`, `contrato/`, `system_prompt.md` |
| 5 | Trazabilidad | 10 | **10** | este documento + `trazabilidad.json` |
| 6 | Reproducibilidad | 10 | **5** | `codigo/correr_ciclos.py`, `corridas/validar.py` |
| 7 | Proceso documentado | 5 | **5** | historia de commits |
| | **Total** | **100** | **70** | |

## El cero, sin atenuantes

El criterio 2 vale 20 puntos y esta entrega saca **0**.

La devolución pidió *"guardá tres corridas reales"*. `corridas/` contiene el
esquema, el validador y el generador, pero **cero archivos de corrida**. Bajo la
regla dura eso es el nivel más bajo, sin crédito parcial por tener la
infraestructura lista. Tener el instrumento no es tener la medición.

Arrastra además el criterio 6 a la mitad: el aislamiento del experimento está
diseñado para ser verificable —`validar.py` compara `hash_entrada` y
`hash_prompt` entre las tres corridas— pero **nunca se ejecutó sobre datos
reales**, así que lo que hay es una garantía de diseño, no una demostración.

Entre los dos criterios, las corridas faltantes valen **25 de los 100 puntos**.

El motivo del faltante está documentado en
[`../corridas/README.md`](../corridas/README.md): generar las corridas requiere
credenciales de Telegram que sólo puede obtener el titular de la cuenta, porque
el login pide un código enviado al teléfono. No se incluyeron corridas simuladas:
una corrida inventada invalidaría la comparación entera y convertiría los otros
75 puntos en material sospechoso.

## Por qué el criterio 3 no llega a 20

Lo verificable está hecho: cero credenciales en el código, cero campos
personales en lo publicado, y el alcance de la exposición documentado sin
maquillar —incluyendo que fue **potencial y no consumada** para los datos de
terceros, porque el cron nunca corrió.

Lo que falta no es documentación sino un hecho: el `api_hash` de Telegram sigue
accesible en el historial de git y **no se puede rotar**. La única mitigación
disponible —descartar la aplicación en my.telegram.org— todavía no se ejecutó.
Mientras esa exposición residual siga viva, el criterio no está completo.

## Qué cambiaría el puntaje

| Acción | Criterios | Puntos |
|---|---|---|
| Generar y commitear las tres corridas | 2 y 6 | **+25** |
| Descartar la app de Telegram comprometida | 3 | **+5** |

Con ambas, 100. Sin la primera, ninguna otra mejora compensa: es el único
pedido explícito de la devolución que no tiene artefacto.

## Nota sobre esta autoevaluación

Un documento que se puntúa a sí mismo tiene un sesgo obvio, y la forma de
controlarlo es que las filas bajas sean verificables tan fácil como las altas.
El cero del criterio 2 se comprueba con:

```bash
ls entrega2/corridas/corrida_*.json    # no devuelve nada
```

Si ese comando alguna vez devuelve tres archivos, este documento quedó
desactualizado y hay que rehacer el puntaje.
