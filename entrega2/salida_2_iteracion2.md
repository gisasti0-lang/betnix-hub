# Salida 2 — Iteración 2: Script completo con Excel + GitHub Pages

**Prompt usado:** Iteración 2 del `user_prompt.md`  
**Técnicas:** Structured output (JSON schema para resumen.json) + RAG (lee Excel y lo actualiza) + few-shot (el agente siguió el patrón de la v1)

---

## Cambios respecto a Salida 1

| Mejora | Técnica de prompt que la disparó |
|--------|----------------------------------|
| Actualización de Excel (cols "Último contacto" y "Último mensaje") | Se especificó explícitamente en el pedido |
| Push a GitHub via API REST (no requiere git instalado) | Se especificó el repo y el archivo destino |
| Formato JSON estructurado para `resumen.json` | El agente infirió el schema desde la descripción de la web |
| Cron job para ejecución automática a las 8 AM | El agente sugirió esto como parte de la respuesta |

---

## Fragmento clave agregado (función push_to_github)

```python
def push_to_github(data: dict):
    """Sube resumen.json al repo de GitHub Pages via API REST."""
    api_url = f"https://api.github.com/repos/{GH_OWNER}/{GH_REPO}/contents/{GH_FILE}"
    headers = {
        "Authorization": f"token {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }
    # Obtener SHA actual (requerido por la API de GitHub para actualizar)
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            sha = json.loads(resp.read()).get("sha", "")
    except urllib.error.HTTPError:
        sha = ""

    content = base64.b64encode(
        json.dumps(data, ensure_ascii=False, indent=2).encode()
    ).decode()

    payload = json.dumps({
        "message": f"update resumen {data.get('fecha', '')}",
        "content": content,
        **({"sha": sha} if sha else {}),
    }).encode()

    req = urllib.request.Request(api_url, data=payload, headers=headers, method="PUT")
    with urllib.request.urlopen(req) as resp:
        print(f"  🌐 GitHub Pages actualizado (HTTP {resp.getcode()})")
```

## Schema de resumen.json (Structured Output)

```json
{
  "fecha": "2026-08-31",
  "timestamp": "2026-08-31T08:03:14.221",
  "chats_activos": 3,
  "respondidos": 2,
  "contactos_excel": 211,
  "resumen": [
    {
      "handle": "@ejemplo_afiliado",
      "nombre": "Nombre Apellido",
      "fecha": "31/08 07:45",
      "mensaje": "Hola, ¿cuándo me aprueban el deal?"
    }
  ]
}
```

## Cron job configurado

```
0 8 * * * /usr/bin/python3 /Users/.../morning_summary.py >> morning_log.txt 2>&1
```

---

## Resultado final

- Script corre automáticamente a las 8 AM con la computadora encendida
- Actualiza el Excel con la fecha y texto del último mensaje de cada afiliado
- Publica `resumen.json` en `gisasti0-lang/betnix-hub`
- La página `https://gisasti0-lang.github.io/betnix-hub/` muestra el resumen del día en tiempo real
