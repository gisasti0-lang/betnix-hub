# Salida 3 — Caso control: propuesta incompleta (v2)

**Contexto:** Se usó el agente v2 con una propuesta que solo define el problema y la propuesta de valor, pero no tiene modelo de negocio ni equipo. Sirve para verificar que el agente aplica el nivel 0 cuando la información no está presente, sin inventar datos.

---

## Entrada (propuesta incompleta)

```
Nombre: EduBot LATAM
Rubro: EdTech

Problema: Millones de estudiantes de secundaria en Argentina no tienen acceso a tutoría personalizada por el costo. El 68% de los alumnos de escuelas públicas nunca recibió apoyo extra (UNICEF, 2023).

Propuesta de valor: Un chatbot de IA que actúa como tutor 24/7, adaptado al currículo argentino. A diferencia de plataformas como Duolingo (que enseña idiomas), nosotros cubrimos matemática, física y química del secundario con ejercicios generados en tiempo real.
```

---

## Respuesta del agente (v2)

## Evaluación de propuesta

**Propuesta analizada:** EduBot LATAM — tutoría con IA para secundaria argentina  
**Fecha:** 2026-08-31

| Dimensión | Nivel (0-3) | Puntaje | Cita de respaldo |
|-----------|-------------|---------|-----------------|
| D1 — Problema y mercado | 3 | 25/25 | "El 68% de los alumnos de escuelas públicas nunca recibió apoyo extra (UNICEF, 2023)" |
| D2 — Propuesta de valor | 2 | 17/25 | "A diferencia de plataformas como Duolingo [...] cubrimos matemática, física y química" — diferenciación clara pero no cuantificada ni validada empíricamente |
| D3 — Modelo de negocio | 0 | 0/25 | No hay información sobre fuente de ingresos, precio ni métricas |
| D4 — Equipo y ejecución | 0 | 0/25 | No se menciona equipo ni plan de ejecución |
| **TOTAL** | | **42/100** | |

**Observaciones:** La propuesta tiene un problema bien documentado y una diferenciación conceptualmente sólida, pero es una idea sin estructura de negocio. La ausencia total de modelo de ingresos y equipo impide evaluar la viabilidad. Se requiere información básica antes de cualquier decisión.

**Alertas:** ninguno

**Veredicto:** SOLICITAR MÁS INFO

---

## Qué valida esta salida

- El agente asigna nivel 0 cuando la información está ausente, sin "rellenar" datos
- El veredicto cambia correctamente respecto a Salida 2 (92 vs 42 pts)
- El formato es idéntico → confirma determinismo estructural del agente v2
