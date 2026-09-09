# Corridas

Cada corrida es una carpeta `YYYY-MM-DD/` con tres archivos:

| Archivo | Contenido |
|---|---|
| `entrada.json` | El lote que recibió el agente, seudonimizado |
| `salida.json` | El JSON que devolvió, **sin edición cosmética** |
| `meta.json` | Fecha, modelo, tokens de entrada y salida medidos, costo, y `enviados: 0` |

La fecha vive en `meta.json`, además del nombre de la carpeta.

## Estado

**Las tres corridas todavía no están generadas.** Dependen de credenciales de
Telegram que sólo puede obtener el titular de la cuenta: el login pide un código
enviado al teléfono y no se puede automatizar.

No se incluyen corridas simuladas. Una corrida inventada invalidaría el análisis
económico —que toma sus tokens de `meta.json`— y convertiría el resto del trabajo
en material sospechoso.

## Cómo generarlas

```bash
python3 agente/construir_lote.py --salida corridas/$(date +%F)/entrada.json
python3 agente/triage.py --entrada corridas/$(date +%F)/entrada.json
```

Tres días distintos dan tres entradas reales distintas. Ninguna corrida envía
mensajes: `meta.json` registra `enviados: 0` en todas.
