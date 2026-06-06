# H8 FEATURE CATALOG V1

## Status

Catálogo metodológico inicial.

Pronto para revisão do PM.

Não contém código.

Não cria dataset.

Não cria feature builder.

Não executa validação estatística.

Não executa baseline.

Não altera schema.

Não altera importer.

---

## Objetivo

Formalizar a primeira versão do catálogo de features da hipótese H8 — Momentum e Pressão Temporal — após coleta, auditoria e importação inicial dos artefatos SofaScore:

- `graph.json`, importado em `match_graph`;
- `shotmap.json`, importado em `match_shotmap`.

Este documento define features candidatas, fonte, momento disponível, risco de leakage, dependências e prioridade metodológica.

A implementação de feature builder, dataset, validação estatística e baseline depende de aprovação posterior.

---

## Premissas Metodológicas

- Todas as features H8 devem ser calculadas apenas com dados disponíveis até o cutoff analisado.
- Eventos posteriores ao cutoff são proibidos como variáveis explicativas.
- `momentum_value` deve ser usado como valor bruto do graph, sem normalização, inversão ou transformação de sinal nesta etapa.
- `xg` e finalizações do shotmap só podem ser usados quando a finalização ocorreu até o cutoff.
- A partida `12437015` é exceção técnica conhecida para `graph.json` e deve ser excluída apenas de outputs que exijam graph completo.
- Nenhuma feature deste catálogo é target-derived.
- Nenhuma feature deste catálogo autoriza modelagem por si só.

---

# H8-A — Graph

Fonte base:

```text
match_graph
```

Grain original:

```text
sofascore_event_id + point_index
```

Campo principal:

```text
momentum_value
```

## momentum_last_5m_avg

### Definição

Média do momentum bruto nos 5 minutos imediatamente anteriores ou iguais ao cutoff.

### Fórmula Conceitual

```text
avg(momentum_value)
where minute > cutoff_minute - 5
  and minute <= cutoff_minute
```

### Fonte

- `match_graph.minute`
- `match_graph.momentum_value`

### Momento Disponível

Disponível no cutoff, desde que todos os pontos usados tenham `minute <= cutoff_minute`.

### Risco de Leakage

Baixo, se o filtro temporal for aplicado corretamente.

### Dependências

- `graph.json` disponível.
- `match_graph` importado.
- Política para `12437015` aplicada.

### Prioridade

Alta.

---

## momentum_last_10m_avg

### Definição

Média do momentum bruto nos 10 minutos imediatamente anteriores ou iguais ao cutoff.

### Fórmula Conceitual

```text
avg(momentum_value)
where minute > cutoff_minute - 10
  and minute <= cutoff_minute
```

### Fonte

- `match_graph.minute`
- `match_graph.momentum_value`

### Momento Disponível

Disponível no cutoff, desde que todos os pontos usados tenham `minute <= cutoff_minute`.

### Risco de Leakage

Baixo, se o filtro temporal for aplicado corretamente.

### Dependências

- `graph.json` disponível.
- `match_graph` importado.
- Política para `12437015` aplicada.

### Prioridade

Alta.

---

## momentum_trend_last_10m

### Definição

Tendência simples do momentum nos 10 minutos imediatamente anteriores ou iguais ao cutoff.

### Fórmula Conceitual

Opção conceitual inicial:

```text
momentum_value_at_cutoff_window_end - momentum_value_at_cutoff_window_start
```

ou, se aprovado posteriormente pelo Quant Research:

```text
slope(momentum_value ~ minute)
where minute > cutoff_minute - 10
  and minute <= cutoff_minute
```

### Fonte

- `match_graph.minute`
- `match_graph.momentum_value`

### Momento Disponível

Disponível no cutoff, desde que a janela use somente pontos com `minute <= cutoff_minute`.

### Risco de Leakage

Médio.

Motivo: a feature depende de cálculo de tendência e precisa de definição operacional precisa para evitar inclusão acidental de pontos após cutoff.

### Dependências

- `graph.json` disponível.
- `match_graph` importado.
- Definição estatística final da tendência.
- Política para `12437015` aplicada.

### Prioridade

Média-alta.

---

## momentum_sum_until_cutoff

### Definição

Soma acumulada do momentum bruto desde o início da partida até o cutoff.

### Fórmula Conceitual

```text
sum(momentum_value)
where minute <= cutoff_minute
```

### Fonte

- `match_graph.minute`
- `match_graph.momentum_value`

### Momento Disponível

Disponível no cutoff, pois usa apenas pontos até o cutoff.

### Risco de Leakage

Baixo, se `minute <= cutoff_minute` for respeitado.

### Dependências

- `graph.json` disponível.
- `match_graph` importado.
- Política para `12437015` aplicada.

### Prioridade

Média.

---

# H8-B — Shotmap

Fonte base:

```text
match_shotmap
```

Grain original:

```text
sofascore_event_id + shot_index
```

Campos principais:

```text
minute
added_time
time_seconds
xg
xgot
shot_type
```

## xg_last_5m

### Definição

Soma de xG das finalizações ocorridas nos 5 minutos imediatamente anteriores ou iguais ao cutoff.

### Fórmula Conceitual

```text
sum(xg)
where minute > cutoff_minute - 5
  and minute <= cutoff_minute
```

### Fonte

- `match_shotmap.minute`
- `match_shotmap.xg`

### Momento Disponível

Disponível no cutoff, desde que apenas finalizações com `minute <= cutoff_minute` sejam consideradas.

### Risco de Leakage

Baixo.

### Dependências

- `shotmap.json` disponível.
- `match_shotmap` importado.
- xG presente no payload.

### Prioridade

Alta.

---

## xg_last_10m

### Definição

Soma de xG das finalizações ocorridas nos 10 minutos imediatamente anteriores ou iguais ao cutoff.

### Fórmula Conceitual

```text
sum(xg)
where minute > cutoff_minute - 10
  and minute <= cutoff_minute
```

### Fonte

- `match_shotmap.minute`
- `match_shotmap.xg`

### Momento Disponível

Disponível no cutoff, desde que apenas finalizações com `minute <= cutoff_minute` sejam consideradas.

### Risco de Leakage

Baixo.

### Dependências

- `shotmap.json` disponível.
- `match_shotmap` importado.
- xG presente no payload.

### Prioridade

Alta.

---

## shots_last_5m

### Definição

Quantidade de finalizações nos 5 minutos imediatamente anteriores ou iguais ao cutoff.

### Fórmula Conceitual

```text
count(*)
where minute > cutoff_minute - 5
  and minute <= cutoff_minute
```

### Fonte

- `match_shotmap.minute`
- `match_shotmap.shot_index`

### Momento Disponível

Disponível no cutoff, desde que apenas finalizações com `minute <= cutoff_minute` sejam consideradas.

### Risco de Leakage

Baixo.

### Dependências

- `shotmap.json` disponível.
- `match_shotmap` importado.

### Prioridade

Alta.

---

## shots_last_10m

### Definição

Quantidade de finalizações nos 10 minutos imediatamente anteriores ou iguais ao cutoff.

### Fórmula Conceitual

```text
count(*)
where minute > cutoff_minute - 10
  and minute <= cutoff_minute
```

### Fonte

- `match_shotmap.minute`
- `match_shotmap.shot_index`

### Momento Disponível

Disponível no cutoff, desde que apenas finalizações com `minute <= cutoff_minute` sejam consideradas.

### Risco de Leakage

Baixo.

### Dependências

- `shotmap.json` disponível.
- `match_shotmap` importado.

### Prioridade

Alta.

---

## xg_sum_until_cutoff

### Definição

Soma acumulada de xG de todas as finalizações ocorridas até o cutoff.

### Fórmula Conceitual

```text
sum(xg)
where minute <= cutoff_minute
```

### Fonte

- `match_shotmap.minute`
- `match_shotmap.xg`

### Momento Disponível

Disponível no cutoff, pois usa apenas finalizações até o cutoff.

### Risco de Leakage

Baixo, se `minute <= cutoff_minute` for respeitado.

### Dependências

- `shotmap.json` disponível.
- `match_shotmap` importado.
- xG presente no payload.

### Prioridade

Média-alta.

---

## Classificação de Risco de Leakage

### Baixo

Feature que usa somente registros com timestamp/minuto menor ou igual ao cutoff e cuja fórmula não depende de informação posterior.

Exemplos:

- `momentum_last_5m_avg`
- `momentum_last_10m_avg`
- `momentum_sum_until_cutoff`
- `xg_last_5m`
- `xg_last_10m`
- `shots_last_5m`
- `shots_last_10m`
- `xg_sum_until_cutoff`

### Médio

Feature que usa somente dados até o cutoff, mas exige regra operacional mais cuidadosa para cálculo, janela, tendência ou agregação.

Exemplo:

- `momentum_trend_last_10m`

### Alto

Feature que usa, direta ou indiretamente, informação posterior ao cutoff, estatísticas finais da partida, target ou derivados do target.

Nenhuma feature deste catálogo deve ser classificada como alto risco se implementada conforme este documento.

Se uma implementação futura depender de dados pós-cutoff, ela deve ser bloqueada ou reclassificada como alto risco.

---

## Plano de Validação Estatística Inicial H8

Objetivo:

Avaliar sinal estatístico inicial das features H8 antes de qualquer baseline/modelagem.

Restrições da validação:

- Não treinar modelo.
- Não executar baseline.
- Não usar dados após cutoff.
- Não usar target-derived features.
- Não usar estatísticas full-match como explicativas.

### Fase H8-A

Validar inicialmente, nesta ordem:

1. `momentum_last_5m_avg`
2. `momentum_last_10m_avg`
3. `momentum_trend_last_10m`
4. `momentum_sum_until_cutoff`

Critérios esperados:

- amostra disponível;
- taxa do target por grupos/quartis;
- diferença contra baseline de prevalência;
- teste estatístico adequado;
- tamanho de efeito;
- recomendação: manter, observar ou descartar.

### Fase H8-B

Validar inicialmente, nesta ordem:

1. `xg_last_5m`
2. `xg_last_10m`
3. `shots_last_5m`
4. `shots_last_10m`
5. `xg_sum_until_cutoff`

Critérios esperados:

- amostra disponível;
- taxa do target por grupos/quartis;
- diferença contra baseline de prevalência;
- teste estatístico adequado;
- tamanho de efeito;
- recomendação: manter, observar ou descartar.

---

## Estratégia Futura Multi-Cutoff

Objetivo:

Avaliar a relação entre antecedência operacional e capacidade preditiva.

### Primeiro tempo

Cutoffs candidatos:

- 15
- 25

Uso esperado:

- medir sinal muito antecipado;
- avaliar se pressão/momentum inicial carrega informação útil;
- comparar baixa disponibilidade de eventos contra antecedência maior.

### Segundo tempo

Cutoffs candidatos:

- 60
- 65
- 70
- 75

Uso esperado:

- comparar ganho informacional progressivo;
- medir trade-off entre antecedência e proximidade do target;
- avaliar estabilidade das features H8 em janelas operacionais realistas.

---

## Dependências Gerais

- `match_graph` importada com `momentum_value`.
- `match_shotmap` importada com `xg`, `minute`, `time_seconds` e finalizações.
- `match_source_status` registrando exceções conhecidas.
- Política para `12437015` aplicada.
- Target temporal definido em dataset futuro sem vazamento.

---

## Restrições Ativas

- Não criar código.
- Não criar dataset.
- Não criar feature builder.
- Não treinar modelo.
- Não executar baseline.
- Não alterar schema.
- Não alterar importer.
- Não alterar crawlers.
- Não alterar dados brutos.

---

## Status Final

Documento metodológico completo, auditável e pronto para revisão do PM.
