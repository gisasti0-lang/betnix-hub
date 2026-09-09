# Betnix Hub — Agente de seguimiento de prospección

**Trabajo Final — Programación de y con Agentes de IA · MBA UCEMA 2026 2T**
**Integrante:** Gonzalo Isasti

Hub en producción: https://gisasti0-lang.github.io/betnix-hub/

---

## Qué construimos

Un agente que cada mañana lee los mensajes que le llegaron por Telegram a un
Affiliate Manager de 196 afiliados alcanzables, los clasifica por intención y urgencia, y
redacta un borrador de respuesta para cada uno. **No envía nada:** deja los
borradores para que la persona los apruebe, edite o descarte uno por uno.

El sistema completo tiene tres capas:

| Capa | Qué hace | Dónde |
|---|---|---|
| **Lectura** | Lee la planilla, selecciona por criterio determinista y seudonimiza razón social y contacto | `agente/construir_lote.py` |
| **Agente** | Decide y redacta, con salida JSON validada contra esquema | `agente/seguimiento.py` |
| **Publicación** | Publica agregados sin datos personales en una página pública | `entrega2/codigo/morning_summary.py`, `index.html` |

Corre solo a las 08:00 mediante un LaunchAgent, y se detiene antes de cualquier
efecto externo.

### Sobre el número de afiliados

La planilla tiene **288 filas con datos**: 211 marcadas con canal Telegram y 77
con Email. De las 211, **196 tienen un @handle válido** y son las únicas
alcanzables por el sistema. Las entregas anteriores decían «~211 afiliados»:
era el conteo de filas, no de contactos direccionables.

### Por qué el sistema apunta a la prospección y no a los mensajes entrantes

La planilla **no es una cartera de afiliados, es un pipeline de prospección en
frío.** De 288 contactos, solo unos 21 son socios reales —15 «already working» y
6 «Launching»—; el resto fue contactado y en su mayoría nunca respondió.

| Estado | Contactos |
|---|---:|
| Contacted | 129 |
| Sin respuesta | 56 |
| Not relevant | 34 |
| already working | 15 |
| Not replying | 11 |
| REBOTÓ | 10 |
| Launching | 6 |

### Sobre el volumen real

Medido sobre la cuenta el 9/9/2026, contando mensajes entrantes de contactos de
la planilla:

| Ventana | Mensajes |
|---|---:|
| 24 horas | 0 |
| 7 días | 0 |
| 30 días | 1 |
| 90 días | 6 |

Ese número no dice que los afiliados estén callados: dice que **la mayoría de esa
lista nunca fue afiliada**. Son prospectos que no contestaron.

Por eso el sistema apunta al trabajo saliente —a quién le corresponde seguimiento
hoy— y no al entrante. Una versión anterior de este trabajo construyó un agente
de triage de mensajes recibidos; sobre esta base de datos, ese agente habría
tenido seis casos en noventa días. El cambio está documentado en
[`DECISIONES.md`](DECISIONES.md).

## Cómo se lo pedimos

El contrato del agente está en [`prompts/system_prompt.md`](prompts/system_prompt.md)
y cubre las seis funciones: identidad, alcance y fuera de alcance, insumos, reglas
duras, comportamiento ante ambigüedad o fallo, y formato de salida.

El user prompt es el **lote serializado**, sin instrucciones mezcladas
([`prompts/user_prompt.md`](prompts/user_prompt.md)). Es deliberado: toda la
instrucción vive en el system prompt, y el mensaje del afiliado entra como dato.
Mezclarlos es la vía por la que el texto de un tercero se lee como orden.

La historia de cómo llegó a esta forma —tres versiones del contrato, con el diff
aislado— está en [`entrega2/`](entrega2/).

## Qué funciona

- Lectura de Telegram y del Excel, con seudonimización HMAC antes del prompt.
- Clasificación en ocho categorías con salida JSON validada por esquema.
- Publicación de agregados sin handles, nombres ni texto de mensajes.
- Automatización diaria por LaunchAgent, con 13 precondiciones verificadas
  (`entrega2/codigo/diagnostico.sh`).
- Gancho de supervisión: no existe ninguna ruta de código con permiso de escritura
  sobre Telegram.

## Qué falló

Tres fallas, con su evidencia, en [`DECISIONES.md`](DECISIONES.md):

1. **El cron nunca se ejecutó** — dos semanas figurando «en producción» sin haber
   corrido una vez. `ModuleNotFoundError: No module named 'telethon'`, más falta de
   Full Disk Access, que hace que cron falle sin dejar log.
2. **El chequeo de secretos republicaba el secreto** que estaba denunciando.
3. **Sin resolver:** el `api_hash` de Telegram quedó expuesto y no se puede rotar.

## Qué aprendimos

Un contrato puede ser obedecido perfectamente y aun así producir un resultado
inseguro. La regla que decía «las credenciales van en variables de configuración
al inicio del archivo» se cumplió al pie de la letra, y por eso mismo publicó un
`api_hash` en un repositorio público: especificaba una *ubicación* para el secreto
en vez de una *propiedad* que debía cumplir.

El corolario incómodo es que no todos los secretos admiten remediación. Un token
de GitHub se revoca en dos clicks; el `api_hash` de Telegram no se revoca nunca.

## Estructura

| Ruta | Contenido |
|---|---|
| [`prompts/`](prompts/) | System prompt y user prompt |
| [`agente/`](agente/) | El agente y el constructor del lote |
| [`corridas/`](corridas/) | Las tres ejecuciones: entrada, salida, fecha |
| [`DECISIONES.md`](DECISIONES.md) | Iteraciones, fallas, decisiones y cambios de alcance |
| [`ANALISIS_ECONOMICO.md`](ANALISIS_ECONOMICO.md) | Consumo, costo, proyección y elección de modelo |
| [`GOBIERNO.md`](GOBIERNO.md) | Perímetro, riesgos, nivel de autonomía L2 y responsable |
| [`entrega2/`](entrega2/) | La Entrega 2 y la historia del contrato |

## Cómo volver a correrlo

Requiere Python 3.14, `anthropic`, `openpyxl` y una `ANTHROPIC_API_KEY` en el
entorno (`entrega2/codigo/.env.example`). El agente **no** necesita credenciales
de Telegram: esas las usa solo el componente legado del hub.

```bash
python3 agente/construir_lote.py --salida corridas/$(date +%F)/entrada.json
python3 agente/seguimiento.py --entrada corridas/$(date +%F)/entrada.json
```

El primer comando lee la planilla y escribe el lote seudonimizado. El segundo llama
al modelo y escribe `salida.json` y `meta.json` con tokens y costo medidos.
Ninguno envía mensajes.

Modelo: `claude-opus-5`, constante `MODELO` en `agente/seguimiento.py`. La comparación
contra alternativas está en [`ANALISIS_ECONOMICO.md`](ANALISIS_ECONOMICO.md) §4.
