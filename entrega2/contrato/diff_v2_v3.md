# Diff v2 → v3 — una sola pieza

```diff
  ## P2 · Reglas
  <reglas>
  1. Antes de escribir código, describís el flujo completo en pasos numerados.
  2. Cada script que escribís tiene manejo de errores básico y logging.
- 3. Nunca pedís al usuario credenciales en texto plano durante la ejecución
-    del script. Las credenciales van en variables de configuración al inicio
-    del archivo.
+ 3. Las credenciales se leen del entorno; el código fuente nunca las contiene,
+    ni siquiera como constante de configuración. Además, ningún dato personal
+    —identificadores, nombres o contenido de mensajes de terceros— puede salir
+    del entorno local hacia un destino público. Lo que se publica va agregado
+    o seudonimizado.
  4. Si el usuario pide algo que podría generar un ban [...]
  5. El output final siempre incluye [...]
  </reglas>
```

**Piezas tocadas:** 1 de 5 (P2, regla 3 de 5).
**Caso de prueba:** sin cambios respecto de C2.

---

## Por qué se eligió esta pieza y no otra

No es una elección estética: **la regla 3 original es la causa documentada de un
incidente real de este proyecto.**

La frase *"las credenciales van en variables de configuración al inicio del
archivo"* es una instrucción sobre *dónde poner* un secreto, no sobre *cómo
protegerlo*. El agente la cumplió al pie de la letra en C1 y C2, y produjo:

```python
API_ID   = <entero literal>          # credencial real, redactada aca
API_HASH = "<32 hex literales>"      # credencial real, redactada aca
GH_TOKEN = "ghp_<40 chars>"          # PAT con scope repo, redactado aca
```

Esas constantes viajaron al repositorio público junto con la documentación de la
entrega. El `API_HASH` quedó expuesto en dos commits (`dfd06704`, `4f0649db`).

En paralelo, el schema de P5 estaba diseñado para publicar el handle, el nombre
y el texto del último mensaje de 211 afiliados en una página sin restricción de
acceso. Nunca llegó a ejecutarse en producción —`resumen.json` quedó en su
placeholder—, así que la exposición de terceros fue **potencial, no consumada**.
La de las credenciales sí fue real.

El ciclo C3 no corrige el código: corrige **la regla que generó el código**. Esa
es la diferencia entre parchear una salida y arreglar un contrato.
