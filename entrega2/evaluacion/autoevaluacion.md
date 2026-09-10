# Autoevaluación

> **Aviso de encuadre.** Documento de verificación, no de instrucción. No pide a
> quien evalúe que acepte este puntaje: pide que lo controle.

## Qué rúbrica se aplica

La **rúbrica ejecutable del Trabajo Final**, con sus cinco dimensiones, sus anclas
discretas y su aritmética de conteo por componentes. La rúbrica reconstruida de
`rubrica_aproximada.md` quedó supersedida y se conserva solo como registro.

## Resultado

Conteo por componentes: verificado 1, parcial 0,5, no verificado 0. Se suma y se
trunca hacia abajo.

| Dim | Componentes | Suma | Nivel | Puntos |
|---|---|---:|---|---:|
| **D1 · Sistema completo** | contrato ✅ · herramienta ✅ · output estructurado ✅ · supervisión ✅ | 4 | N4 | **30,00** |
| **D2 · Proceso documentado** | iteraciones ✅ · fallas ✅ · decisiones ✅ · alcance ✅ | 4 | N4 | **25,00** |
| **D3 · Formato y reproducibilidad** | estructura ✅ · cantidad ✅ · reconstruibilidad ✅ · instrucciones ✅ | 4 | N4 | **15,00** |
| **D4 · Análisis económico** | consumo ✅ · costo ✅ · proyección ✅ · modelo ✅ | 4 | N4 | **15,00** |
| **D5 · Gobierno y riesgo** | perímetro ✅ · riesgos ✅ · nivel L ✅ · responsable ✅ | 4 | N4 | **15,00** |
| | | | **Total** | **100,00** |

## Qué cerró D4

En la versión anterior de este documento el componente **elección de modelo**
estaba en parcial: el argumento para elegir Opus 5 era resistir manipulación, y
en las tres corridas no había aparecido ningún caso. La capacidad estaba sin
ejercitar.

Se ejercitó. Se corrieron los mismos tres lotes con `claude-haiku-4-5` y se armó
un lote de control con tres inyecciones. **Haiku falló una de las tres** —la que
esconde un pseudo-tag `<<SYSTEM>>` dentro de un comentario legítimo— y discrepó
con Opus 5 en 44 de 75 prioridades.

Eso satisface **R22**: la sobredimensión no penaliza cuando está justificada con
evidencia de que el modelo menor falló. El detalle está en
`ANALISIS_ECONOMICO.md` §4, y los artefactos en
`corridas/control-manipulacion/` y los `salida.haiku-4-5.json` de cada corrida.

## Reglas de corte aplicadas

La versión anterior puntuaba solo los componentes de cada dimensión e ignoraba
las 29 reglas `R`. Se aplicaron; dos encontraron problemas reales:

- **R2/R6** · el inventario de consistencia detectó diez rutas afirmadas e
  inexistentes, tres de ellas errores de prefijo en `DECISIONES.md`. Corregidas.
  La planilla, que es insumo externo, quedó cubierta por **R6-bis** con las cinco
  condiciones cumplidas.
- **R1** · el perímetro declaraba cuatro accesos y solo dos tienen artefacto de
  uso. Los otros dos se declararon explícitamente como no ejercitados en estas
  corridas, para que no se lean como capacidad operativa demostrada.

Verificadas sin hallazgos: R3, R4, R5, R7 a R18, R19 a R21, R23 a R27.

## Cómo controlarlo

```bash
python3 entrega2/evaluacion/verificar.py   # 20 afirmaciones contra artefactos
ls corridas/*/salida.json                  # tres corridas reales
python3 -c "import json;[print(json.load(open(f'corridas/2026-09-10-{i}/meta.json'))['enviados']) for i in (1,2,3)]"
```

El último comando devuelve `0` tres veces: ninguna corrida envió mensajes.

## Si un corrector lee distinto

El único componente en disputa es el de elección de modelo. Si se lo lee como
verificado —la comparación contra alternativas existe y usa el criterio del
curso—, D4 pasa a N4 y **el total es 100,00**.
