# Betnix Hub — Agente de triage de mensajes de afiliados

**Trabajo Final — Programación de y con Agentes de IA · MBA UCEMA 2026 2T**
**Integrante:** Gonzalo Isasti

Hub en producción: https://gisasti0-lang.github.io/betnix-hub/

---

## Qué construimos

Un agente que cada mañana lee los mensajes que le llegaron por Telegram a un
Affiliate Manager de ~211 afiliados, los clasifica por intención y urgencia, y
redacta un borrador de respuesta para cada uno. **No envía nada:** deja los
borradores para que la persona los apruebe, edite o descarte uno por uno.

El sistema completo tiene tres capas:

| Capa | Qué hace | Dónde |
|---|---|---|
| **Lectura** | Lee Telegram y el Excel de afiliados; seudonimiza cada handle antes de que salga de la máquina | `agente/construir_lote.py` |
| **Agente** | Clasifica y redacta, con salida JSON validada contra esquema | `agente/triage.py` |
| **Publicación** | Publica agregados sin datos personales en una página pública | `entrega2/codigo/morning_summary.py`, `index.html` |

Corre solo a las 08:00 mediante un LaunchAgent, y se detiene antes de cualquier
efecto externo.

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

Requiere Python 3.14, `anthropic`, `telethon`, `openpyxl`, una `ANTHROPIC_API_KEY`
y credenciales de Telegram en el entorno (`entrega2/codigo/.env.example`).

```bash
python3 agente/construir_lote.py --salida corridas/$(date +%F)/entrada.json
python3 agente/triage.py --entrada corridas/$(date +%F)/entrada.json
```

El primer comando lee Telegram y escribe el lote seudonimizado. El segundo llama
al modelo y escribe `salida.json` y `meta.json` con tokens y costo medidos.
Ninguno envía mensajes.

Modelo: `claude-opus-5`, constante `MODELO` en `agente/triage.py`. La comparación
contra alternativas está en [`ANALISIS_ECONOMICO.md`](ANALISIS_ECONOMICO.md) §4.
