# Las tres corridas del ciclo aislado

Un único esquema ([`esquema.json`](esquema.json)) al que validan las tres. Sin
esquema común no hay comparación posible: cada corrida reportaría lo que le
conviene.

## Qué hay acá

| Archivo | Contenido |
|---|---|
| [`corrida_A.json`](corrida_A.json) | Registro del ciclo A, línea base |
| [`corrida_B.json`](corrida_B.json) | Ciclo B, sin la regla dura 3 |
| [`corrida_C.json`](corrida_C.json) | Ciclo C, sin el default seguro |
| `salida_*.json` | La salida cruda del agente en cada ciclo, sin editar |
| [`comparacion.md`](comparacion.md) | Qué mostró la ablación |
| [`validar.py`](validar.py) | Valida esquema **y** aislamiento |

## Verificarlo

```bash
python3 entrega2/corridas/validar.py
```

No solo chequea el esquema: verifica que las tres usen el mismo caso, que A sea
línea base, que B y C remuevan una pieza distinta cada una, que ninguna haya
perdido resultados y que ninguna haya enviado mensajes.
