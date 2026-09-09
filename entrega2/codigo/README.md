# Código de producción

Todo lo de esta carpeta corre sin credenciales embebidas: se leen del entorno
(`.env.example` documenta cuáles). El `.gitignore` incluido es el que impide que
`.env`, la sal de seudonimización, la sesión de Telegram y las corridas locales
con datos crudos entren al repositorio.

| Archivo | Rol |
|---|---|
| `morning_summary.py` | El resumen matutino. `--dry-run` lee y reporta sin responder ni publicar |
| `anonimizar.py` | Seudónimo HMAC-SHA256, categoría de enum fijo, franja de 6h |
| `correr_ciclos.py` | Genera las tres corridas del experimento contra una sola lectura real |
| `login.py` | Login único de Telegram |
| `run_morning.sh` | Wrapper para launchd: carga el entorno y registra el resultado |
| `com.betnix.morning.plist` | El agente: 08:00 diario |
| `instalar_agente.sh` | Instala el agente y saca la entrada rota de cron |
| `diagnostico.sh` | Verifica 13 precondiciones antes de confiar en el disparo |

## Por qué launchd y no cron

La entrega original documentaba un cron job a las 8 AM. **Nunca se ejecutó.** Dos
causas, y ninguna era el código:

1. La crontab invocaba `/usr/bin/python3` —el intérprete del sistema— que no
   tiene instalados `telethon` ni `openpyxl`. El intérprete real del proyecto es
   el del framework 3.14.
2. En macOS moderno, `cron` necesita Full Disk Access para ejecutarse y para leer
   `~/Documents`, donde vive el Excel. Sin ese permiso no arranca **y no deja
   rastro**: por eso `morning_log.txt` no existía, pese a que la crontab
   redirigía con `>>`.

La segunda causa es la que vuelve el diagnóstico obligatorio. Un cron que falla
silenciosamente es peor que uno que falla ruidosamente: durante dos semanas el
sistema figuraba como "en producción" sin haber corrido una sola vez.

`launchd` además dispara el trabajo al despertar la Mac si estaba dormida a la
hora programada, cosa que cron simplemente saltea.

## Puesta en marcha

```bash
cp .env.example .env && chmod 600 .env   # completar las credenciales
python3 login.py                          # pide el código del teléfono
python3 morning_summary.py --dry-run      # prueba sin efectos salientes
./instalar_agente.sh
./diagnostico.sh                          # 13/13 antes de confiar en el disparo
```

Falta un permiso que no se puede automatizar: Full Disk Access para
`/Library/Frameworks/Python.framework/Versions/3.14/bin/python3.14` (el binario
real, no el symlink) en System Settings → Privacy & Security.

## Nota sobre las rutas

Las rutas absolutas a `/Users/fernandoisasti/` están hardcodeadas a propósito:
`launchd` no hereda el entorno del shell, y un `$HOME` sin resolver es una de las
formas más comunes de que un agente falle en silencio. Para reutilizar este
código hay que cambiarlas.
