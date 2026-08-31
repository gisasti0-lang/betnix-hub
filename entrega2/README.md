# Entrega 2 — Automatización de resumen matutino con Telegram

**Curso:** Programación de y con Agentes de IA — MBA UCEMA 2026 2T  
**Clase:** 2 | **Entrega:** 2  
**Integrante:** Gonzalo Isasti  

---

## La pieza: automatización matutina de Telegram para gestión de afiliados

El agente de IA fue instruido para diseñar e implementar un sistema que:
1. Corre automáticamente a las 8 AM todos los días
2. Lee los chats activos de ~211 afiliados desde un Excel
3. Responde automáticamente a los mensajes nuevos
4. Publica un resumen en una página web pública

**Resultado en producción:** https://gisasti0-lang.github.io/betnix-hub/

---

## Dos iteraciones documentadas

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

## Comparación entre iteraciones

| Aspecto | Iteración 1 | Iteración 2 |
|---------|-------------|-------------|
| Output del agente | Script básico | Script completo |
| Persistencia del resumen | Solo consola | Excel + web pública |
| Automatización | Manual | Cron job a las 8 AM |
| Técnicas de prompt | Role + Context + Structured output | + Few-shot + XML tags + Schema |
| Salida verificable | No (solo consola) | Sí: https://gisasti0-lang.github.io/betnix-hub/ |

---

## Aprendizaje principal

El mayor salto entre iteraciones no fue técnico sino de **especificidad del prompt**. En la Iteración 1, el agente produjo código correcto pero incompleto porque el pedido no definía dónde debía terminar el output. En la Iteración 2, especificar el destino (GitHub, nombre del archivo, nombre del repo) fue suficiente para que el agente diseñara toda la lógica de publicación sin preguntas adicionales. La técnica de **XML tags para separar contexto de instrucciones** también redujo la ambigüedad: el agente nunca confundió la descripción del proyecto con una instrucción a ejecutar.

---

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `system_prompt.md` | System prompt v2 con role, instrucciones, contexto y few-shot |
| `user_prompt.md` | Los dos user prompts usados (iteración 1 e iteración 2) |
| `salida_1_iteracion1.md` | Output del agente v1: script básico |
| `salida_2_iteracion2.md` | Output del agente v2: script completo con Excel + GitHub Pages |
| `salida_3_resultado_final.md` | Sistema en producción: componentes, output real y URL verificable |
