# Corridas

Cada corrida es una carpeta `YYYY-MM-DD/` con tres archivos:

| Archivo | Contenido |
|---|---|
| `entrada.json` | El lote que recibió el agente, seudonimizado |
| `salida.json` | El JSON que devolvió, **sin edición cosmética** |
| `meta.json` | Fecha, modelo, tokens de entrada y salida medidos, costo, y `enviados: 0` |

La fecha vive en `meta.json`, además del nombre de la carpeta.

## Estado

**Las tres corridas todavía no están generadas.** Depende de una única cosa: la
`ANTHROPIC_API_KEY` en el entorno. Ya **no** dependen de Telegram — el insumo del
agente es la planilla, no los mensajes recibidos.

No se incluyen corridas simuladas. Una corrida inventada invalidaría el análisis
económico —que toma sus tokens de `meta.json`— y convertiría el resto del trabajo
en material sospechoso.

## Cómo generarlas

```bash
python3 agente/construir_lote.py --salida corridas/$(date +%F)/entrada.json
python3 agente/seguimiento.py --entrada corridas/$(date +%F)/entrada.json
```

Tres corridas con `--limite` distinto, o en tres días distintos a medida que el
tope diario avanza sobre los 217 elegibles, dan tres entradas reales distintas.
Ninguna corrida envía mensajes: `meta.json` registra `enviados: 0` en todas.

El lote publicado no contiene razón social, @handle ni email: solo seudónimo y
atributos de negocio. Por eso estas corridas **sí son publicables**, a diferencia
de las del agente de triage anterior, cuyo insumo era el texto de mensajes
privados.
