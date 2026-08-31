# User Prompt — Automatización de Telegram para gestión de afiliados

## Iteración 1 — Pedido inicial

```
Tengo un Excel con ~211 contactos de Telegram (afiliados de una plataforma de 
apuestas). Quiero que todas las mañanas un script:

1. Lea los @handles del Excel (columna B, solo filas donde columna C = "Telegram")
2. Revise si alguno me mandó mensaje en las últimas 24 horas
3. Si me mandó, que le responda automáticamente "Gracias, ya te respondo 🙌"
4. Que me deje un resumen en consola de quién escribió y qué dijo

El Excel está en: ~/Documents/Betnix Partners/Betnix_Outreach_2026.xlsx
```

## Iteración 2 — Pedido de mejora (refinamiento)

```
El script funciona bien. Ahora quiero agregar dos cosas:

1. Que actualice el Excel con "Último contacto" (fecha) y "Último mensaje" 
   (texto) cada vez que detecte un mensaje nuevo de un afiliado.

2. Que al terminar, suba un archivo resumen JSON a un repo de GitHub Pages 
   para que yo pueda ver la actividad del día desde cualquier lado, 
   sin exponer credenciales de Telegram.

El repo es: gisasti0-lang/betnix-hub
El archivo a actualizar: resumen.json
```

## Notas sobre los prompts

- **Iteración 1** es un pedido directo y funcional. El agente devuelve un script básico con Telethon.
- **Iteración 2** refina el pedido agregando dos outputs adicionales (Excel + GitHub). Demuestra cómo el prompt evoluciona a medida que se valida el primer resultado.
- En ningún momento se incluyen credenciales en el prompt. El agente las pide como variables de configuración en el código.
