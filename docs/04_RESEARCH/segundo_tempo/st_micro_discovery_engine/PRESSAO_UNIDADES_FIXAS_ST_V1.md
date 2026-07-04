# PRESSAO_UNIDADES_FIXAS_ST_V1

## 1. Objetivo

Definir uma métrica de pressão por unidades fixas para a frente `ST_MICRO_DISCOVERY_ENGINE_V1`, substituindo o `pressure_score` composto por regras simples e configuráveis em robô.

Esta métrica foi criada para ser legível, auditável e configurável com números fixos por janela.

## 2. Escopo

Esta métrica é para pesquisa e configuração técnica de filtros. Ela não valida estratégia para operação real, não define staking, não autoriza robô em banca real e não substitui validação fora da amostra.

## 3. Nome oficial da métrica

```text
PRESSAO_UNIDADES_FIXAS_ST_V1
```

## 4. Temperaturas oficiais

```text
FRIO
SEM_PRESSAO
MODERADO
PRESSIONANDO
MUITA_PRESSAO
```

## 5. Regra geral

Temperaturas abaixo de `MODERADO` usam operadores de teto:

```text
FRIO e SEM_PRESSAO usam <=
```

Temperaturas de `MODERADO` para cima usam operadores de piso:

```text
MODERADO, PRESSIONANDO e MUITA_PRESSAO usam >=
```

## 6. Métricas usadas

```text
ataques_perigosos
dares chutes
chutes_no_gol
escanteios
posse_de_bola
```

Observação: posse de bola é ignorada em `FRIO` e `SEM_PRESSAO`.

## 7. Ataques perigosos por minuto

| Temperatura | Ataques perigosos por minuto | Operador |
| --- | ---: | --- |
| FRIO | 0.6 | <= |
| SEM_PRESSAO | 1.0 | <= |
| MODERADO | 1.4 | >= |
| PRESSIONANDO | 1.6 | >= |
| MUITA_PRESSAO | 1.8 | >= |

## 8. Regras W5

| Temperatura | Ataques perigosos W5 | Chutes W5 | Chutes no gol W5 | Escanteios W5 | Posse |
| --- | ---: | ---: | ---: | ---: | --- |
| FRIO | <= 3 | <= 1 | <= 1 | <= 1 | ignorar |
| SEM_PRESSAO | <= 5 | <= 1 | <= 1 | <= 1 | ignorar |
| MODERADO | >= 7 | >= 2 | ignorar | >= 1 | >= 65% para um dos times |
| PRESSIONANDO | >= 8 | >= 3 | ignorar | >= 2 | >= 65% para um dos times |
| MUITA_PRESSAO | >= 9 | >= 4 | ignorar | >= 3 | >= 65% para um dos times |

## 9. Regras W10

| Temperatura | Ataques perigosos W10 | Chutes W10 | Chutes no gol W10 | Escanteios W10 | Posse |
| --- | ---: | ---: | ---: | ---: | --- |
| FRIO | <= 6 | <= 1 | <= 1 | <= 1 | ignorar |
| SEM_PRESSAO | <= 10 | <= 1 | <= 1 | <= 1 | ignorar |
| MODERADO | >= 14 | >= 4 | >= 1 | >= 1 | >= 65% para um dos times |
| PRESSIONANDO | >= 16 | >= 5 | >= 1 | >= 2 | >= 65% para um dos times |
| MUITA_PRESSAO | >= 18 | >= 6 | >= 1 | >= 3 | >= 65% para um dos times |

## 10. Regras W15

| Temperatura | Ataques perigosos W15 | Chutes W15 | Chutes no gol W15 | Escanteios W15 | Posse |
| --- | ---: | ---: | ---: | ---: | --- |
| FRIO | <= 9 | <= 1 | <= 1 | <= 1 | ignorar |
| SEM_PRESSAO | <= 15 | <= 1 | <= 1 | <= 1 | ignorar |
| MODERADO | >= 21 | >= 6 | >= 1 | >= 2 | >= 65% para um dos times |
| PRESSIONANDO | >= 24 | >= 7 | >= 2 | >= 3 | >= 70% para um dos times |
| MUITA_PRESSAO | >= 27 | >= 8 | >= 3 | >= 4 | >= 75% para um dos times |

## 11. Observações importantes

- `chutes_no_gol` em W5 é ignorado para temperaturas de `MODERADO` para cima.
- `chutes_no_gol` em W10 fica fixo em `>= 1` para `MODERADO`, `PRESSIONANDO` e `MUITA_PRESSAO`.
- `chutes_no_gol` em W15 aumenta por temperatura: `>= 1`, `>= 2`, `>= 3`.
- Posse de bola só aumenta por temperatura em W15.
- Posse de bola é ignorada em `FRIO` e `SEM_PRESSAO`.
- Esta métrica não usa score ponderado.
- Cada filtro deve ser salvo de forma explícita para ser compatível com robôs que aceitam apenas números fixos.

## 12. Exemplo de regra configurável

```text
W15_MUITA_PRESSAO:
ataques_perigosos_w15 >= 27
chutes_w15 >= 8
chutes_no_gol_w15 >= 3
escanteios_w15 >= 4
posse_bola_um_dos_times >= 75%
```

## 13. Status

```text
PRESSAO_UNIDADES_FIXAS_ST_V1_DEFINIDA
```
