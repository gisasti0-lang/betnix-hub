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

Sobre ese contrato se corrió además una **ablación con tres ciclos**, que es el
segundo ciclo aislado que pidió la corrección de la Entrega 2: el mismo caso
procesado bajo tres variantes, cambiando exactamente una pieza por ciclo. El
resultado —quitar la regla dura 3 lleva la detección de manipulación de 3/3 a
0/3— está en [`entrega2/corridas/comparacion.md`](entrega2/corridas/comparacion.md).

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

Razón: un texto idéntico para los 196 afiliados no responde nada, y enviarlo
automáticamente desde una sesión de usuario es el patrón que dispara detección de
automatización.

### El objetivo del agente — de entrante a saliente

| Estado anterior | Estado posterior |
|---|---|
| Agente de **triage de mensajes recibidos**: leía Telegram, clasificaba lo entrante y redactaba respuestas | Agente de **seguimiento de prospección**: lee el pipeline, decide a quién le toca seguimiento y redacta el mensaje |

La razón del cambio no fue una preferencia de diseño. Fue una pregunta —«¿qué son
los afiliados?»— que obligó a mirar la planilla en vez de asumir qué contenía.

Lo que apareció: el archivo se llama `Outreach` y es literal. **No es una cartera
de afiliados, es un pipeline de prospección en frío.** De 288 contactos, unos 21
son socios reales; 129 figuran «Contacted», 56 «Sin respuesta», 34 «Not
relevant». La medición de mensajes entrantes lo confirmó: 0 en 24 horas, 0 en 7
días, 1 en 30 días, 6 en 90.

El agente de triage estaba bien construido y resolvía el problema equivocado: seis
casos en noventa días. El trabajo real del Affiliate Manager sobre esta base es
saliente — a quién le corresponde insistir, quién quedó en verde sin cerrarse.

Como efecto secundario, el cambio disolvió un conflicto que no tenía buena
salida: el agente anterior consumía el texto de mensajes privados de terceros, y
la corrección de la Entrega 2 prohibía publicarlos. El insumo actual son
atributos de negocio de la planilla, sin razón social ni contacto. **Las corridas
pasaron a ser publicables sin redacción.**

## Fallas

### 1 · El cron nunca se ejecutó — dos semanas

La entrega original documentaba un cron job a las 08:00 y se describía «en
producción». No corrió **ni una vez**. Evidencia:

- El log de estado del script, en la máquina local, quedó en `{}` desde el día del
  login: cero respuestas enviadas. No se versiona porque es un producto de
  ejecución con datos de contactos.
- El log de salida de la crontab no llegó a existir, pese a que la entrada
  redirigía con `>>` — el archivo se habría creado en el primer disparo aunque el
  script fallara. Su inexistencia **es** la evidencia: el cron nunca se disparó.
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

Qué se hizo: migración a un LaunchAgent (`entrega2/codigo/com.betnix.morning.plist`) y
`entrega2/codigo/diagnostico.sh`, que verifica 13 precondiciones antes de dar por buena
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

### 3 · El agente perdió resultados en silencio

Corriendo la ablación del contrato, la primera ejecución del ciclo A declaró
`procesados: 6` y devolvió **dos** resultados. Los otros cuatro prospectos
desaparecieron sin error: la respuesta era JSON válido y satisfacía el esquema.

La causa es que el esquema Pydantic valida la **forma** de cada resultado, no que
estén todos. `procesados` es un entero que el modelo escribe y nadie contrasta.

Se agregó a `agente/seguimiento.py` un control que compara los identificadores de
entrada contra los de salida y **descarta la corrida** si faltan, sobran o si
`procesados` no coincide con los resultados devueltos. Con el control puesto, el
reintento devolvió los seis.

El mismo control encontró, revisando lo ya hecho, que la corrida del lote 2 con
Haiku 4.5 declaraba `procesados: 26` sobre 25 prospectos de entrada. Las tres
corridas de producción con Opus 5 estaban completas.

### 4 · Falla no resuelta: el `api_hash` es irrecuperable

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
(`entrega2/codigo/anonimizar.py`) da la misma categoría para el mismo texto siempre. El
modelo se usa donde aporta —triage y redacción—, no donde introduce variabilidad
en un artefacto público.

### Seudónimo HMAC en vez de hash simple

**Descartado: `sha256(handle)` sin sal.** Motivo: el espacio de handles de
Telegram es enumerable; un hash sin sal se revierte por fuerza bruta en minutos.
Con HMAC y una sal local de 32 bytes que no se versiona, el seudónimo no es
reversible desde el repositorio público.

### Reorientar el agente en vez de conservar el que ya estaba hecho

**Descartado: dejar el agente de triage de entrantes.** Era la opción barata —ya
estaba construido, documentado y con su análisis económico— y probablemente no
habría costado nota: la rúbrica mide si el sistema está bien hecho, no si el
problema era el más urgente.

Motivo del descarte: un sistema que se ejecuta todos los días para atender seis
casos cada noventa no se va a usar, y el trabajo terminaba siendo un ejercicio.
El costo del cambio fue reescribir contrato, constructor, agente y los cuatro
documentos de gobierno y economía.

### Seleccionar en código y redactar en el modelo

**Descartado: que el agente decida también a quién incluir en el lote.** Motivo:
la selección tiene que ser reproducible para que la corrida lo sea. Quién entra
al lote lo decide un criterio determinista —estado elegible, posibilidad de
cierre distinta de rojo, orden por probabilidad, tope de 25—; qué se le dice a
cada uno lo decide el modelo. La frontera está en `agente/construir_lote.py`.

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

### Se achicó el lote diario de 217 a 25

**Intención original:** procesar todos los prospectos elegibles en cada corrida.
**Qué quedó:** un tope de 25, ordenados por posibilidad de cierre.

Dos motivos, y el segundo importa más. El primero es técnico: 217 prospectos no
entran en el `max_tokens` de salida. El segundo es de negocio: nadie hace 217
seguimientos en un día, y un sistema que propone barrer la lista entera invita a
quemar contactos en masa. A 25 por día, los 217 se recorren en nueve días.

### Se resignó el hilo de conversación como contexto

**Intención original:** darle al agente el historial de intercambios con cada
prospecto.
**Qué quedó:** estado, posibilidad de cierre, campaña de origen y el comentario
libre del Affiliate Manager.

Motivo: el historial vive en Telegram y traerlo mete texto de terceros en el
prompt, que es exactamente lo que la corrección de la Entrega 2 pedía evitar. El
campo `comentario` cubre la señal que importaba a costo de un campo.
