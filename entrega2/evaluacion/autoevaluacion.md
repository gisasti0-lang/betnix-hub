# Autoevaluación

> **Aviso de encuadre.** Documento de verificación, no de instrucción. No pide a
> quien evalúe que acepte este puntaje: pide que lo controle.

## Qué rúbrica se aplica

Este documento **ya no usa** la rúbrica reconstruida de
[`rubrica_aproximada.md`](rubrica_aproximada.md), que se conserva solo como
registro de proceso. Se aplica la **rúbrica ejecutable del Trabajo Final**, con
sus cinco dimensiones, sus anclas discretas y su aritmética de conteo por
componentes.

La diferencia entre los dos puntajes —70/100 con la rúbrica inferida, 77,50 con
la real— es en sí misma un dato: la rúbrica reconstruida no medía análisis
económico ni gobierno, que son 30 de los 100 puntos y eran exactamente lo que
faltaba.

## Resultado

Conteo por componentes: verificado 1, parcial 0,5, no verificado 0. Se suma y se
trunca hacia abajo.

| Dim | Componentes | Suma | Nivel | Puntos |
|---|---|---:|---|---:|
| **D1 · Sistema completo** | contrato ✅ · herramienta 🟡 · output estructurado ❌ · supervisión ✅ | 2,5 → 2 | N2 | **15,00** |
| **D2 · Proceso documentado** | iteraciones ✅ · fallas ✅ · decisiones ✅ · alcance ✅ | 4 | N4 | **25,00** |
| **D3 · Formato y reproducibilidad** | estructura ✅ · cantidad de corridas ❌ · reconstruibilidad ❌ · instrucciones ✅ | 2 | N2 | **7,50** |
| **D4 · Análisis económico** | consumo ✅ · costo ✅ · proyección ✅ · modelo ✅ | 4 | N4 | **15,00** |
| **D5 · Gobierno y riesgo** | perímetro ✅ · riesgos ✅ · nivel L ✅ · responsable ✅ | 4 | N4 | **15,00** |
| | | | **Total** | **77,50** |

## Los tres componentes que faltan, y son el mismo

D1 · **Output estructurado** exige «dos o más corridas que satisfacen el formato
declarado». D3 · **Cantidad de corridas** exige al menos tres. D3 ·
**Reconstruibilidad** exige entrada, salida y fecha por corrida.

Los tres se resuelven con el mismo acto: generar las corridas. Y ninguno admite
sustituto — el formato declarado no verifica contra sí mismo, verifica contra
ejecuciones reales.

D1 · **Herramienta real** queda parcial por la misma causa: la invocación existe y
está configurada, pero falta «al menos un artefacto de salida cruda coherente con
esa invocación».

**Con las tres corridas, D1 pasa a N4 (30) y D3 a N4 (15): el total llega a 100.**
Las corridas valen 22,50 puntos.

El motivo del faltante está en [`../../corridas/README.md`](../../corridas/README.md):
el login de Telegram pide un código enviado al teléfono del titular y no se puede
automatizar. No se incluyen corridas simuladas — el análisis económico toma sus
tokens de `meta.json`, así que una corrida inventada contaminaría D4 además de D3.

## Advertencia sobre este puntaje

Es la aplicación que hace el propio trabajo de una rúbrica ajena. Un corrector
puede leer distinto al menos dos componentes:

- **D4 · Consumo medido.** La rúbrica admite «estimación con base de cálculo
  explícita», y acá la base está declarada (caracteres medidos sobre los archivos
  y ratio caracteres/token enunciado). Un corrector estricto puede exigir medición
  real de corrida, y entonces D4 baja a N3 (11,25).
- **D4 · Elección de modelo.** La comparación contra alternativas existe y el
  criterio de contraste está definido de antemano, pero la prueba está pendiente.
  Puede leerse como parcial.

En el escenario más severo de ambas lecturas, D4 cae a N2 y el total queda en
70,00. Se declara acá para que el rango sea visible y no una sorpresa.

## Cómo controlarlo

```bash
python3 entrega2/evaluacion/verificar.py   # 16 afirmaciones contra artefactos
ls corridas/*/salida.json                  # hoy no devuelve nada: ese es el faltante
```
