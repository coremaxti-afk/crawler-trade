# DECISAO_RENTABILIDADE_POR_TIME_V4_VS_V3

Data: 2026-06-18

## Decisao

```text
V3 ABORTADA.
V2 MANTIDA COMO BASE DETALHADA.
V4 APROVADA COM PEQUENOS AJUSTES.
```

---

## Motivo para abortar a V3

A V3 reduziu o poder de decisao em relacao a V2.

Problemas observados:

- zerou candidatas operacionais;
- colocou muitas estrategias como ressalva;
- usou alerta externo do DD como trava principal;
- escondeu informacoes quantitativas importantes;
- criou whitelist/blacklist que nao ajudou a priorizar lucro e robustez;
- gerou pareceres repetitivos.

---

## Diretriz oficial

A V2 continua sendo a base detalhada.

A V4 deve ser apenas uma extensao quantitativa da V2.

A V4 deve preservar:

- lucro total;
- ROI total;
- lucro sem Top1;
- lucro sem Top3;
- ROI sem Top3;
- concentracao Top1;
- concentracao Top3;
- ranking de exclusao;
- indice de recorrencia por time;
- top times favoraveis;
- top times desfavoraveis.

---

## V4 aprovada com ajustes

A V4 adicionou metricas uteis:

- `robustez_score`;
- `impacto_top3_pct`;
- `lucro_sem_top1_negativo`;
- `lucro_sem_top3_negativo`;
- ranking das mais robustas;
- ranking das mais dependentes.

Parecer:

```text
APROVADA COM PEQUENOS AJUSTES.
```

---

## Ajustes obrigatorios

### 1. Corrigir fronteira do robustez_score

Regra correta:

```text
robustez_score >= 0.80 = MUITO_ROBUSTA
robustez_score >= 0.60 = ROBUSTA
robustez_score >= 0.40 = MODERADA
robustez_score >= 0.20 = FRACA
robustez_score < 0.20 = DEPENDENTE
```

Caso especifico:

```text
robustez_score = 0.60 deve ser ROBUSTA, nao MODERADA.
```

### 2. Filtrar ranking das mais dependentes

Problema:

```text
Ranking ficou poluido por estrategias com lucro total muito baixo.
```

Regra recomendada:

```text
lucro_total >= 500
OU
N >= 30
```

---

## Regra de uso

A V4 nao deve substituir ranking financeiro geral.

A V4 deve responder:

```text
A estrategia continua lucrativa apos remover os principais times positivos?
```

Toda leitura financeira continua sendo:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```
