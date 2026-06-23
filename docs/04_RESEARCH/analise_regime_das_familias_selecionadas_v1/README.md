# ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1

## Status

```text
APROVADA COMO PROXIMA FRENTE
NAO EXECUTADA AINDA
NAO APROVA OPERACAO REAL
```

## Contexto

O projeto ja possui `ANALISE_REGIME_POR_FASE_V1`, que mede o comportamento global da liga por fase.

Esse estudo global e util para entender o clima da liga, mas pode ser contaminado por estrategias ruins, pois avalia o universo completo de familias e variacoes.

A nova frente deve olhar apenas familias/variacoes selecionadas e candidatas.

---

## Objetivo

Analisar em quais fases da temporada cada familia selecionada funciona, quebra ou fica inconclusiva.

Pergunta central:

```text
Dentro das familias que ja passaram por filtros anteriores, quais fases sao realmente favoraveis?
```

---

## Escopo inicial

Usar como entrada:

```text
CARTEIRA_PRINCIPAL
CARTEIRA_OBSERVACAO
VARIACOES_OFICIAIS
FAMILIAS_GOAL_DEPENDENTES_DE_REGIME
```

Nao usar todas as estrategias indiscriminadamente para decisao operacional.

---

## Relacao com regime global

### Regime global

```text
Serve para entender o comportamento geral da liga por fase.
```

### Regime das familias selecionadas

```text
Serve para entender quando cada familia candidata deve ser monitorada, evitada ou preservada como dependente de fase.
```

---

## Perguntas obrigatorias

```text
1. Qual fase e forte por familia?
2. Qual fase e fraca/proibida por familia?
3. A fase forte se repete entre temporadas?
4. Goal/Over tem familias negativas no agregado, mas positivas em fases recorrentes?
5. No Goal continua estrutural ou tambem depende de fase?
6. A leitura de regime melhora a operacao sem criar overfitting?
```

---

## Classificacoes esperadas

```text
REGIME_FORTE_RECORRENTE
REGIME_FORTE_ISOLADO
REGIME_OSCILANTE
REGIME_RISCO
REGIME_INCONCLUSIVO
```

---

## Regras metodologicas

- Nao criar estrategia nova.
- Nao alterar cutoff, target ou window.
- Nao recalcular discovery.
- Nao recalcular drawdown completo sem necessidade.
- Nao usar fase forte isolada como regra operacional definitiva.
- Nao aprovar operacao real.
- Nao somar variacoes com overlap alto.
- Todos os resultados financeiros devem continuar como `ESTIMATIVA OPERACIONAL COM ODDS MEDIAS`.

---

## Observacao sobre Goal/Over

Goal/Over pode ser ruim no agregado anual e ainda assim ser lucrativo em fase especifica.

Por isso, familias Goal/Over nao devem ser descartadas definitivamente quando houver evidencia de fase forte recorrente.

Nova interpretacao:

```text
Goal/Over ruim no agregado + fase forte recorrente = DEPENDENTE_DE_REGIME
```

Isso nao aprova operacao. Apenas preserva a hipotese para analise controlada.

---

## Proxima acao

Gerar prompt Codex para implementar/executar `ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1`.
