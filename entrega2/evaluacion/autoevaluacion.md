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
| **D4 · Análisis económico** | consumo ✅ · costo ✅ · proyección ✅ · modelo 🟡 | 3,5 → 3 | N3 | **11,25** |
| **D5 · Gobierno y riesgo** | perímetro ✅ · riesgos ✅ · nivel L ✅ · responsable ✅ | 4 | N4 | **15,00** |
| | | | **Total** | **96,25** |

## Por qué D4 no llega a N4

Tres de sus cuatro componentes están verificados con medición real: el consumo
sale del campo `usage` de la API en tres corridas, el costo es recalculable a
mano contra la tarifa citada, y la proyección tiene los dos horizontes con el
supuesto de volumen declarado.

El cuarto —**elección de modelo justificada**— se puntúa **parcial**, y es una
decisión deliberada de este documento.

La justificación existe y compara contra dos alternativas con números medidos.
Pero el argumento que sostiene la elección de Opus 5 es la resistencia a
manipulación que exige la regla dura 3, y **en las tres corridas no apareció
ningún caso de manipulación**. La capacidad quedó sin ejercitar. No hay evidencia
de que Opus 5 sea necesario, ni de que Haiku 4.5 —cinco veces más barato— no
alcance.

Un modelo elegido por precaución sobre un riesgo no observado, que cuesta USD 55
anuales de más, es una justificación a medias. Bajo la regla dura de la rúbrica
—sin evidencia, el nivel más bajo— corresponde parcial.

Se podría haber escrito el componente como verificado y probablemente pasaba. Se
puntúa parcial porque el criterio de contraste que falta está escrito en
`ANALISIS_ECONOMICO.md` §4, y declarar completo algo que el propio documento
declara pendiente sería incoherente.

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
