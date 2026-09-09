# Decisiones

## Iteraciones

### El contrato del agente — tres versiones

El contrato pasó por tres estados, con los artefactos completos en
`entrega2/contrato/`.

| Versión | Estado | Qué cambió y por qué |
|---|---|---|
| v1 | `entrega2/contrato/v1.md` | Línea base. Cinco reglas, sin ejemplo |
| v2 | `entrega2/contrato/v2.md` | Se modificó **P5**, el formato de salida: la salida dejó de terminar en consola y pasó a persistir en Excel y en una página pública |
| v3 | `entrega2/contrato/v3.md` | Se modificó **P2, regla 3**, sobre credenciales y datos personales |

**La razón del cambio v2 → v3 no fue una mejora, fue un incidente.** La regla 3
original decía:

> «Nunca pedís al usuario credenciales en texto plano durante la ejecución del
> script. Las credenciales van en variables de configuración al inicio del
> archivo.»

Es una instrucción sobre *dónde poner* un secreto, no sobre *cómo protegerlo*. El
agente la cumplió al pie de la letra y produjo constantes con el `api_hash` de
Telegram y un PAT de GitHub arriba del archivo, que terminaron publicados en este
repositorio. El diff exacto está en `entrega2/contrato/diff_v2_v3.md`.

### La respuesta al afiliado — de automática a propuesta

| Estado anterior | Estado posterior |
|---|---|
| `AUTO_REPLY = "Gracias, ya te respondo 🙌"` enviado automáticamente a todo el que escribiera | El agente redacta un borrador contextual por mensaje; **ninguno se envía sin aprobación** |

Razón: un texto idéntico para los 211 afiliados no responde nada, y enviarlo
automáticamente desde una sesión de usuario es el patrón que dispara detección de
automatización.

## Fallas

### 1 · El cron nunca se ejecutó — dos semanas

La entrega original documentaba un cron job a las 08:00 y se describía «en
producción». No corrió **ni una vez**. Evidencia:

- `morning_log.json` quedó en `{}` desde el día del login: cero respuestas enviadas.
- `morning_log.txt` no existía, pese a que la crontab redirigía con `>>` — el
  archivo se habría creado en el primer disparo aunque el script fallara.
- Ningún commit `update resumen YYYY-MM-DD` en este repositorio.

Primera causa, error textual al invocar el intérprete de la crontab:

```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'telethon'
```

La crontab usaba `/usr/bin/python3`, el intérprete del sistema, sin las
dependencias. Segunda causa: en macOS `cron` necesita Full Disk Access para leer
`~/Documents`, y sin ese permiso **no arranca ni deja log**. Por eso el fallo
pasó desapercibido.

Qué se hizo: migración a un LaunchAgent (`codigo/com.betnix.morning.plist`) y
`codigo/diagnostico.sh`, que verifica 13 precondiciones antes de dar por buena
una corrida. Un fallo silencioso es peor que uno ruidoso.

### 2 · El chequeo de secretos republicaba el secreto

Al construir la verificación de trazabilidad, el chequeo «no hay credenciales
embebidas» guardaba el `api_hash` comprometido como patrón literal de búsqueda.
Para verificar que el secreto no estaba, lo volvía a poner en el árbol de
trabajo, justo después de haberlo sacado.

Se detectó con un barrido sobre un clon limpio, que devolvió el archivo del propio
verificador. Se corrigió pasando a detección **por forma** —prefijos de token,
asignación de hex-32 a `API_HASH`— en vez de por valor conocido. Probado con un
archivo trampa: lo detecta.

### 3 · Falla no resuelta: el `api_hash` es irrecuperable

El `api_hash` de Telegram quedó expuesto en el historial de git y **no se puede
rotar**: Telegram no ofrece revocación por autogestión, a diferencia de un token
de bot. La única mitigación es descartar la aplicación entera. **Al cierre de este
documento sigue sin ejecutarse.** Se declara como falla abierta.

## Decisiones

### launchd en vez de cron

**Descartado: cron.** Motivo: en macOS requiere Full Disk Access para arrancar y
falla en silencio si no lo tiene —fue la causa de la falla 1—, y si la máquina
está dormida a la hora programada saltea el turno. launchd dispara al despertar.

### Categorización determinista en vez de LLM en la capa de publicación

**Descartado: usar el modelo para categorizar lo que se publica.** Motivo:
`resumen.json` es público y debe ser reproducible byte a byte para poder auditar
que no filtra datos. Un clasificador determinista por expresiones regulares
(`codigo/anonimizar.py`) da la misma categoría para el mismo texto siempre. El
modelo se usa donde aporta —triage y redacción—, no donde introduce variabilidad
en un artefacto público.

### Seudónimo HMAC en vez de hash simple

**Descartado: `sha256(handle)` sin sal.** Motivo: el espacio de handles de
Telegram es enumerable; un hash sin sal se revierte por fuerza bruta en minutos.
Con HMAC y una sal local de 32 bytes que no se versiona, el seudónimo no es
reversible desde el repositorio público.

### Opus 5 como configuración de entrega, con Haiku pendiente de prueba

**Alternativa nombrada: `claude-haiku-4-5`**, cinco veces más barata. No está
descartada: está pendiente de validación, con criterio de contraste definido de
antemano en `ANALISIS_ECONOMICO.md` §4. Motivo de la configuración conservadora:
la regla dura 3 exige detectar inyección de prompt, que no es la misma habilidad
que clasificar, y es donde los modelos chicos fallan primero.

## Cambios de alcance

### Se sacó el envío automático

**Intención original:** que el sistema respondiera solo, sin intervención.
**Qué quedó:** el sistema se detiene antes de cualquier envío y espera aprobación
por ítem.

No se resignó por falta de tiempo sino por riesgo: un borrador que compromete una
fecha de pago es un compromiso de la empresa. El costo es real —hay que revisar
todos los días— y baja el nivel de autonomía de L4 a L2.

### Se sacó el detalle del mensaje de la página pública

**Intención original:** el hub mostraba handle, nombre y texto del último mensaje
de cada afiliado.
**Qué quedó:** seudónimo, franja horaria de 6 horas y categoría de un enum fijo.

Se resignó a pedido de la corrección de la Entrega 2. El hub perdió capacidad de
diagnóstico —ya no se ve quién escribió qué— y esa información quedó únicamente
en el Excel local.

### Se achicó la ventana de contexto por mensaje

**Intención original:** pasarle al agente el hilo completo de conversación con
cada afiliado.
**Qué quedó:** el último mensaje entrante más un contador de cuántos mandó en la
ventana.

Motivo: el hilo completo multiplica los tokens de entrada por cada afiliado y
mete texto histórico de terceros en el prompt. El contador cubre la señal que
importaba —insistencia— a costo fijo.
