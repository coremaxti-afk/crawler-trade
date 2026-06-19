# RENTABILIDADE_DAS_ESTRATEGIAS_POR_TIME_RESULTADOS_V4

Data: 2026-06-18

Agente responsavel: `05 - Data Science / Quant Research`

Status: `APROVADA COM PEQUENOS AJUSTES`

---

## 1. Decisao oficial

A V3 foi abortada como frente principal.

Motivo:

```text
A V3 reduziu o poder de decisao em relacao a V2, porque escondeu informacoes importantes e classificou todas as candidatas como ressalva por causa de alerta externo de DD.
```

Decisao:

```text
V2 permanece como base metodologica.
V4 passa a ser a evolucao oficial da frente de rentabilidade por time.
```

A V4 nao deve substituir a V2 apagando informacoes.

A V4 deve preservar a V2 e adicionar metricas quantitativas de decisao.

---

## 2. Objetivo da V4

Responder com mais clareza:

```text
Esta estrategia continua lucrativa quando removemos os times que mais ajudam?
```

E tambem:

```text
Quanto do lucro depende do Top 1 e do Top 3 times?
```

---

## 3. O que a V4 preserva da V2

A V4 deve preservar integralmente as informacoes da V2:

- lucro total;
- ROI total;
- lucro sem Top 1;
- lucro sem Top 3;
- ROI sem Top 3;
- concentracao Top 1;
- concentracao Top 3;
- classificacao de robustez;
- ranking de exclusao;
- indice de recorrencia por time;
- top times favoraveis;
- top times desfavoraveis.

A V2 continua sendo a melhor base detalhada da frente.

---

## 4. Novas metricas adicionadas na V4

### 4.1 Robustez score

Formula:

```text
robustez_score = lucro_sem_top3 / lucro_total
```

Objetivo:

```text
Medir quanto lucro permanece apos remover os 3 times que mais sustentam a estrategia.
```

Interpretacao oficial:

| robustez_score | classificacao_robustez_v4 |
|---:|---|
| >= 0.80 | MUITO_ROBUSTA |
| >= 0.60 | ROBUSTA |
| >= 0.40 | MODERADA |
| >= 0.20 | FRACA |
| < 0.20 | DEPENDENTE |

### 4.2 Impacto Top 3

Formula:

```text
impacto_top3_pct = 1 - (lucro_sem_top3 / lucro_total)
```

Objetivo:

```text
Medir quanto do lucro total desaparece quando os 3 melhores times sao removidos.
```

### 4.3 Flags de dependencia critica

Campos adicionados:

```text
lucro_sem_top1_negativo
lucro_sem_top3_negativo
```

Valores:

```text
SIM
NAO
```

---

## 5. Avaliacao da entrega V4

Parecer:

```text
APROVADA COM PEQUENOS AJUSTES
```

Pontos positivos:

- preservou a estrutura quantitativa da V2;
- adicionou robustez_score;
- adicionou impacto_top3_pct;
- adicionou flags de lucro negativo sem Top1/Top3;
- criou rankings de robustez e dependencia;
- evitou repetir o erro da V3 de esconder informacoes relevantes;
- voltou a priorizar lucro, ROI e robustez multi-time.

---

## 6. Ajustes obrigatorios antes de considerar final

### 6.1 Corrigir fronteira do robustez_score

Problema encontrado:

```text
robustez_score = 0.60 estava sendo classificado como MODERADA.
```

Regra correta:

```text
robustez_score >= 0.60 deve ser ROBUSTA.
```

A classificacao deve respeitar limites inclusivos:

```text
>= 0.80 = MUITO_ROBUSTA
>= 0.60 = ROBUSTA
>= 0.40 = MODERADA
>= 0.20 = FRACA
< 0.20 = DEPENDENTE
```

### 6.2 Filtrar ranking das mais dependentes

Problema encontrado:

```text
O ranking das mais dependentes ficou poluido por estrategias com lucro total muito baixo.
```

Exemplos de casos que distorcem impacto percentual:

```text
lucro_total muito baixo, como 8.16, 16.67, 24.18.
```

Regra recomendada para o ranking das mais dependentes:

```text
lucro_total >= 500
OU
N >= 30
```

Objetivo:

```text
Evitar que micro-lucros criem impacto_top3_pct artificialmente alto.
```

---

## 7. O que nao fazer na V4

A V4 nao deve recriar os erros da V3.

Nao fazer:

```text
- criar whitelist;
- criar blacklist;
- criar candidatas operacionais;
- criar candidatas com ressalva;
- usar temporal_order_verified como filtro principal;
- esconder estrategias lucrativas por alerta externo do DD;
- substituir a V2 por um resumo pobre;
- gerar pareceres textuais repetitivos.
```

A rentabilidade por time deve responder apenas:

```text
A estrategia depende ou nao de poucos times?
```

---

## 8. Uso correto da V4

A V4 deve ser usada como extensao quantitativa da V2.

Fluxo recomendado:

```text
Discovery
-> Normalizacao pre-DD
-> DD financeiro
-> Rentabilidade por time V2
-> Rentabilidade por time V4
```

A V4 nao substitui DD financeiro.

A V4 nao substitui ranking financeiro geral.

A V4 ajuda a decidir se a estrategia e:

```text
MUITO_ROBUSTA
ROBUSTA
MODERADA
FRACA
DEPENDENTE
```

apos remover os principais times positivos.

---

## 9. Regra financeira obrigatoria

Toda leitura financeira continua sendo:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

Proibido chamar de backtest financeiro real.

---

## 10. Parecer final

```text
V4 APROVADA COM PEQUENOS AJUSTES.
V3 ABORTADA.
V2 CONTINUA COMO BASE DETALHADA.
V4 PASSA A SER A EXTENSAO QUANTITATIVA OFICIAL PARA ROBUSTEZ POR TIME.
```
