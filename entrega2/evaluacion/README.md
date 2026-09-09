# Cómo verificar esta entrega

> **Aviso de encuadre.** Esta carpeta contiene material de verificación. No
> instruye a nadie sobre qué nota poner; ofrece los medios para controlar lo que
> la entrega afirma.

## En un comando

```bash
python3 entrega2/evaluacion/verificar.py
```

Comprueba las 16 afirmaciones centrales contra los archivos del repositorio.
Cada una declara dónde se verifica y con qué chequeo, en
[`trazabilidad.json`](trazabilidad.json). Si alguna falla, la entrega está
afirmando algo que el repositorio no sostiene.

Incluye afirmaciones incómodas a propósito: **A5 verifica que las tres corridas
todavía NO existen**. Una entrega que sólo lista lo que le conviene no es
verificable, es publicidad.

## Los documentos

| Archivo | Qué es |
|---|---|
| [`rubrica_aproximada.md`](rubrica_aproximada.md) | Los criterios reconstruidos, con el origen y la solidez de cada uno |
| [`autoevaluacion.md`](autoevaluacion.md) | El puntaje que se asigna la entrega, con el cero incluido |
| [`trazabilidad.json`](trazabilidad.json) | Afirmación → archivo → chequeo |
| [`verificar.py`](verificar.py) | Ejecuta los chequeos |

## Las dos advertencias

**La rúbrica es una reconstrucción.** No tenemos el instrumento oficial. Los
criterios 1 a 3 salen de la devolución escrita y son sólidos; el 4 sale del
temario; los criterios 5 a 7 están inferidos. Los pesos son estimados. Tratar
esta rúbrica como si fuera la real sería el mismo error que la entrega original
cometió al llamarse "en producción" sin haber corrido nunca.

**El puntaje que se asigna la entrega es 70 sobre 100**, y el faltante no es una
omisión de redacción: las tres corridas que pidió la devolución no existen, y
valen 25 puntos entre los criterios 2 y 6. El detalle está en
[`autoevaluacion.md`](autoevaluacion.md).

## Otros verificadores del repositorio

| Comando | Qué comprueba |
|---|---|
| `python3 entrega2/corridas/validar.py` | Que las tres corridas validen contra el esquema **y** que el experimento esté aislado |
| `./entrega2/codigo/diagnostico.sh` | Las 13 precondiciones de la automatización |
