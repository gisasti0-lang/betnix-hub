# Entrega 2 — Agente evaluador de propuestas de negocio

**Curso:** Programación de y con Agentes de IA — MBA UCEMA 2026 2T  
**Clase:** 2 | **Entrega:** 2  
**Integrante:** Gonzalo Isasti

---

## Qué es la "pieza"

Un **agente evaluador de propuestas de negocio** para una aceleradora de startups. Recibe una propuesta en texto libre y devuelve un dictamen estructurado con puntaje por dimensión, citas de respaldo y veredicto.

---

## Iteración 1 → Iteración 2

### Iteración 1 (v1)

**Qué tenía:** El system prompt definía el rol y las cuatro dimensiones, pero el formato de salida era libre y no exigía citas textuales.

**Problema detectado al correr la Salida 1:** El agente:
- Usó una escala distinta a la definida (notas sobre 10 en vez de 0-3)
- Incorporó opinión subjetiva ("me parece interesante")
- No citó nada de la propuesta para respaldar los puntajes
- Era vulnerable a inyección de prompts

**Fragmento del system prompt v1 que causaba el problema:**

```
Evaluá la propuesta y asignale puntaje en cada dimensión.
Formato: libre, podés usar el que te parezca más claro.
```

→ El agente interpretó "formato libre" como licencia para variar la escala y agregar subjetividad.

---

### Iteración 2 (v2)

**Cambios realizados:**

| Cambio | Por qué |
|--------|---------|
| Formato de tabla obligatorio con campos fijos | Fuerza consistencia entre corridas |
| Escala 0-3 → puntaje ponderado especificado | Evita que el agente use otras escalas |
| "Sin cita, nivel máximo = 1" | Elimina puntajes sin respaldo |
| Regla anti-inyección explícita | Protege contra manipulación desde el input |
| Principio de determinismo | El agente sabe que va a ser evaluado por reproducibilidad |

**Resultado:** La Salida 2 (misma propuesta, agente v2) es completamente estructurada, cita cada puntaje, y baja D4 de nivel 3 a nivel 2 porque ahora la rúbrica exige plan de acción además de equipo.

---

## Archivos de esta entrega

| Archivo | Descripción |
|---------|-------------|
| `system_prompt.md` | System prompt v2 (versión final) |
| `user_prompt.md` | Plantilla de invocación + descripción de variantes |
| `salida_1_iteracion1.md` | Output del agente v1 sobre la propuesta FreshRoute |
| `salida_2_iteracion2.md` | Output del agente v2 sobre la misma propuesta (muestra mejora) |
| `salida_3_caso_incompleto.md` | Output del agente v2 sobre propuesta incompleta (caso control) |

---

## Aprendizaje clave

El principal salto entre v1 y v2 no fue el contenido de la rúbrica sino las **restricciones de formato y evidencia**. Un agente que puede elegir su formato de salida tiende a ser inconsistente entre corridas. La instrucción `"Sin cita, nivel máximo = 1"` fue el cambio más simple con mayor impacto: eliminó toda la subjetividad de un sola regla.
