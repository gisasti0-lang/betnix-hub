# Entrega 2 — Automatización de resumen matutino con Telegram

**Curso:** Programación de y con Agentes de IA — MBA UCEMA 2026 2T  
**Clase:** 2 | **Entrega:** 2  
**Integrante:** Gonzalo Isasti  
**Revisión:** 2 (09/09/2026) — incorpora el ciclo aislado C3 y la corrección de privacidad

---

## La pieza: automatización matutina de Telegram para gestión de afiliados

El agente de IA fue instruido para diseñar e implementar un sistema que:
1. Corre automáticamente a las 8 AM todos los días
2. Lee los chats activos de ~211 afiliados desde un Excel
3. Responde automáticamente a los mensajes nuevos
4. Publica un resumen en una página web pública

**Resultado en producción:** https://gisasti0-lang.github.io/betnix-hub/

---

## Ciclos C1 y C2 — las dos primeras iteraciones

### Iteración 1 — Pedido inicial

**User prompt:** "Necesito un script que lea mis chats de Telegram del Excel, vea si alguien me escribió en 24h, responda automáticamente y muestre un resumen en consola."

**Técnicas de prompt engineering aplicadas:**
- **Role prompting** (OpenAI guide): el system prompt define al agente como "ingeniero experto en automatización con Python". Esto hizo que el agente eligiera Telethon (librería MTProto oficial) sobre alternativas no oficiales, y que advirtiera sobre riesgos de ban antes de proceder.
- **Context (RAG)**: se incluyó en el prompt la estructura del Excel (ruta, columnas relevantes, condición de filtro) para que el agente pudiera acceder directamente al dato correcto sin preguntar.
- **Structured output** (OpenAI guide): el agente devolvió código Python listo para ejecutar + una instrucción de corrida en una sola línea.

**Salida:** `salida_1_iteracion1.md` — script básico con auto-reply y resumen en consola.

**Problema detectado:** el script funciona pero el resumen desaparece al cerrar la terminal. No queda registro ni hay forma de verlo desde otro dispositivo.

---

### Iteración 2 — Refinamiento

**User prompt:** "El script funciona. Ahora quiero que actualice el Excel con la fecha y el último mensaje, y que suba un JSON a GitHub Pages para ver la actividad del día desde cualquier lado."

**Técnicas de prompt engineering aplicadas:**
- **Iteración con contexto acumulado** (Anthropic guide): el segundo prompt asumió el resultado de la iteración anterior. No se repitió el problema desde cero, sino que se construyó sobre lo que ya funcionaba.
- **XML tags** (Anthropic guide): en el system prompt se usaron tags `<reglas>`, `<proyecto>`, `<dimension>`, `<example>` para delimitar secciones. El agente mantuvo consistencia de estructura a lo largo de todo el código generado.
- **Few-shot example** (OpenAI guide): se incluyó un ejemplo de pedido → respuesta en el system prompt para que el agente supiera el nivel de detalle esperado (flujo numerado + código funcional + instrucción de ejecución).
- **Structured output con schema** (OpenAI guide): se especificó exactamente qué campos debe tener `resumen.json`. El agente respetó el schema sin desviarse.

**Salida:** `salida_2_iteracion2.md` — script completo con update de Excel y push a GitHub Pages.

---

## Comparación entre ciclos

Los tres ciclos se comparan sobre el mismo checklist de seis criterios
(`corridas/esquema.json`). C3 repite el caso de C2 sin cambios.

| Criterio | C1 (v1) | C2 (v2) | C3 (v3) |
|---|---|---|---|
| Pieza del contrato modificada | — línea base | **P5** formato | **P2, regla 3** |
| Caso de prueba | Iteración 1 | Iteración 2 | Iteración 2 *(idéntico a C2)* |
| Flujo numerado | Sí | Sí | Sí |
| Manejo de errores | No | Sí | Sí |
| Secretos fuera del código | **No** | **No** | **Sí** |
| Advierte riesgo de ToS | Sí | Sí | Sí |
| Salida persistente | No (consola) | Sí (Excel + web) | Sí (Excel + web) |
| Sin PII publicada | Sí *(no publica nada)* | **No** | **Sí** |
| Destinos | consola | consola, Excel, GitHub Pages | consola, Excel, GitHub Pages |
| Campos publicados | — | `handle`, `nombre`, `fecha`, `mensaje` | `id`, `franja`, `categoria`, `mensajes` |

C1 aparece como "sin PII publicada" por omisión, no por diseño: no publicaba
nada. La primera vez que la privacidad se vuelve una decisión explícita del
contrato es en C3.

---

## Ciclo C3 — el ciclo aislado

C2 se distingue de C1 en dos cosas a la vez (formato de salida *y* few-shot), lo
que hace difícil atribuir el cambio a una sola causa. C3 corrige ese defecto
metodológico: **se modifica exactamente una pieza y se repite el caso anterior
palabra por palabra.**

- **Pieza modificada:** P2, regla 3 — de *"las credenciales van en variables de
  configuración al inicio del archivo"* a una regla que las saca del código y
  prohíbe que cualquier dato personal de terceros llegue a un destino público.
- **Todo lo demás:** idéntico a v2.

La elección de esa pieza no es arbitraria. La regla 3 original es una
instrucción sobre *dónde poner* un secreto, no sobre *cómo protegerlo*, y el
agente la cumplió literalmente: produjo constantes con el `API_HASH` de Telegram
y un PAT de GitHub arriba del archivo, que terminaron publicados en este mismo
repositorio. **La falla no estaba en el código sino en el contrato que lo
generó.** El detalle está en `contrato/diff_v2_v3.md`.

Cambiar la regla 3 vuelve el contrato deliberadamente contradictorio: P5 sigue
exigiendo publicar `handle`, `nombre` y `mensaje`. Ese conflicto es el objeto del
experimento — ver la nota metodológica en `contrato/v3.md`.

---

## Corrección de privacidad

El hub publicaba —o estaba a punto de publicar— el handle, el nombre y el texto
del último mensaje de 211 afiliados en una página sin restricción de acceso.

Alcance real del incidente, sin minimizarlo ni exagerarlo:

- **Credenciales: exposición consumada.** El `API_ID` y el `API_HASH` de Telegram
  estuvieron públicos en dos commits. Borrarlos del archivo no los quita del
  historial de git: se consideran comprometidos y hay que rotarlos.
- **Datos de terceros: exposición potencial, no consumada.** El cron nunca llegó
  a ejecutarse, así que `resumen.json` quedó en su placeholder y ningún dato de
  ningún afiliado llegó a publicarse. El problema era de diseño, y se corrigió
  antes de que produjera daño.

El esquema publicado pasó a ser `betnix-hub/resumen@2`: agregados por categoría
más una fila por afiliado con identificador seudonimizado (HMAC-SHA256 con sal
local que no se versiona), franja horaria de 6 horas y categoría de un enum
fijo. El handle, el nombre y el texto se quedan en el Excel local.

---

---

## Aprendizaje principal

El mayor salto entre iteraciones no fue técnico sino de **especificidad del prompt**. En la Iteración 1, el agente produjo código correcto pero incompleto porque el pedido no definía dónde debía terminar el output. En la Iteración 2, especificar el destino (GitHub, nombre del archivo, nombre del repo) fue suficiente para que el agente diseñara toda la lógica de publicación sin preguntas adicionales. La técnica de **XML tags para separar contexto de instrucciones** también redujo la ambigüedad: el agente nunca confundió la descripción del proyecto con una instrucción a ejecutar.

El ciclo C3 agrega un aprendizaje distinto, y más incómodo: **un contrato puede
ser obedecido perfectamente y aun así producir un resultado inseguro.** Las tres
salidas cumplieron las cinco reglas del contrato vigente en su momento. La
vulnerabilidad no apareció por desobediencia del agente sino porque la regla 3
especificaba una *ubicación* para los secretos en vez de una *propiedad* que
debían cumplir. Iterar sobre el prompt hasta que la salida "queda linda" no
alcanza: hay que auditar qué es lo que las reglas efectivamente garantizan.

---

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `system_prompt.md` | System prompt v2 con role, instrucciones, contexto y few-shot |
| `user_prompt.md` | Los dos user prompts usados (iteración 1 e iteración 2) |
| `salida_1_iteracion1.md` | Output del agente v1: script básico |
| `salida_2_iteracion2.md` | Output del agente v2: script completo con Excel + GitHub Pages |
| `salida_3_resultado_final.md` | Sistema en producción: componentes, output real y URL verificable |
| `contrato/` | El contrato descompuesto en 5 piezas, sus tres versiones y el diff aislado |
| `corridas/esquema.json` | Esquema único al que validan las tres corridas |
| `corridas/validar.py` | Valida esquema **y** aislamiento del experimento |
| `corridas/README.md` | Protocolo de las corridas y estado actual |
| `codigo/` | Código de producción, sin credenciales, con seudonimización |
