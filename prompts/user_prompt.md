# User prompt

El user prompt no es texto redactado a mano: es el **lote serializado**. El
agente recibe exactamente el JSON que `agente/construir_lote.py` produce a partir
de la lectura de Telegram, sin envoltorio ni instrucciones adicionales.

Es una decisión de diseño, no una omisión. Toda la instrucción vive en el system
prompt, que es estable entre corridas; el user prompt es solo el dato variable.
Mezclar instrucción y dato en el mismo mensaje es la vía por la que el texto de
un tercero —acá, el campo `comentario`— puede leerse como orden.

## Forma

```json
{
  "fecha_lote": "2026-09-09",
  "prospectos": [
    {
      "id": "AF-3f9a2c11",
      "canal": "Telegram",
      "geo": "LATAM",
      "tipo_trafico": "SEO",
      "estado": "prospecto",
      "posibilidad_cierre": "Verde",
      "campana": "Semana 2 (TG - nov 11-12)",
      "comentario": "pidió ver condiciones antes de avanzar"
    }
  ]
}
```

## Cómo se construye

```bash
python3 agente/construir_lote.py --salida corridas/$(date +%F)/entrada.json
```

Lee la planilla, aplica el criterio de selección, ordena por posibilidad de
cierre, corta en el tope diario y seudonimiza el contacto con HMAC-SHA256 y sal
local. **Ni la razón social ni el contacto entran al prompt.**

## Variantes

No se usan variantes de user prompt: la forma del lote es fija y la validación
del esquema de salida es la que absorbe la variabilidad.
