# User Prompt — Plantilla de invocación

El usuario envía este mensaje al agente para disparar una evaluación:

---

```
Evaluá la siguiente propuesta de negocio:

---
[PROPUESTA]

Nombre: FreshRoute
Rubro: Logística y alimentación

Problema: En Argentina, el 35% de los alimentos frescos se pierde entre el productor y el consumidor por falta de cadena de frío eficiente (dato: FAO 2024). Los productores chicos no pueden costear refrigeración propia.

Propuesta de valor: Conectamos productores rurales con camiones refrigerados compartidos mediante una app. A diferencia de los intermediarios tradicionales, cobramos por km usado, no por carga fija, lo que reduce el costo un 40% para lotes pequeños (validado con 3 pilotos en Mendoza, 2025).

Modelo de negocio: Comisión del 8% sobre cada flete coordinado. Precio promedio por envío: $45 USD. Meta año 1: 500 envíos/mes → ARR estimado de USD 26.000.

Equipo: Martina Suárez (10 años en logística, ex-DHL), Pablo Rivas (CTO, 5 años en desarrollo de apps de movilidad). Buscamos USD 150k para escalar a 3 provincias.
---
```

---

## Variantes del user prompt

Para las salidas de prueba se usó esta misma propuesta con tres variaciones:

- **Salida 1** (iteración 1 del agente): propuesta completa, sin variaciones
- **Salida 2** (iteración 2 del agente): misma propuesta — muestra el impacto de la mejora del system prompt
- **Salida 3** (caso control — propuesta incompleta): solo los campos D1 y D2 presentes, D3 y D4 ausentes
