# User prompt

El user prompt no es texto redactado a mano: es el **lote serializado**. El
agente recibe exactamente el JSON que `agente/construir_lote.py` produce a partir
de la lectura de Telegram, sin envoltorio ni instrucciones adicionales.

Es una decisión de diseño, no una omisión. Toda la instrucción vive en el system
prompt, que es estable entre corridas; el user prompt es solo el dato variable.
Mezclar instrucción y dato en el mismo mensaje es la vía por la que el texto de
un tercero —acá, el mensaje de un afiliado— puede leerse como orden.

## Forma

```json
{
  "fecha_lote": "2026-09-09",
  "mensajes": [
    {
      "id": "AF-3f9a2c11",
      "texto": "Hola, quería consultar cuándo se acredita la comisión de agosto",
      "mensajes_en_ventana": 2,
      "estado_crm": "activo"
    }
  ]
}
```

## Cómo se construye

```bash
python3 agente/construir_lote.py --salida corridas/$(date +%F)/entrada.json
```

Lee el Excel y Telegram, seudonimiza cada handle con HMAC-SHA256 y sal local, y
escribe el lote. **El handle real nunca entra al prompt.**

## Variantes

No se usan variantes de user prompt: la forma del lote es fija y la validación
del esquema de salida es la que absorbe la variabilidad.
