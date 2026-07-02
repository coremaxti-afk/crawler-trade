# HT GOAL RESEARCH V1 — Fechamento oficial

Status: **CONCLUIDO**  
Tipo: **pesquisa financeira estimada com odds medias**  
Uso: **nao operacional**

Este documento registra o fechamento oficial da frente `HT_GOAL_RESEARCH_V1`.

---

## 1. Escopo encerrado

A frente estudou mercados de primeiro tempo após cutoffs fixos:

| Item | Valor |
| --- | --- |
| Mercado GOAL | Back Over HT |
| Mercado NO_GOAL | Lay Over HT |
| Stake GOAL | R$ 100 |
| Responsabilidade NO_GOAL | R$ 100 |
| Cutoffs | 15, 20, 25, 30, 35, 40 |
| Final HT | 45 |
| Odds | medias, nao reais |

---

## 2. Leitura final

A frente chegou a um mapa financeiro estimado, nao a uma operacao real.

Representantes finais:

| Alias | Mercado | Cutoff | N | Lucro | ROI | DD |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| QPP35 | GOAL | 35 | 31 | R$ 1.904,00 | 61,4% | R$ -200,00 |
| AQUEC40_FAV | GOAL | 40 | 20 | R$ 984,00 | 49,2% | R$ -354,00 |
| BQR35 | NO_GOAL | 35 | 44 | R$ 597,75 | 13,6% | R$ -300,00 |

---

## 3. Refinamentos preservados

| Alias | Pai | N | ROI | Soma? |
| --- | --- | ---: | ---: | --- |
| QPP35_SCORE | QPP35 | 21 | 72,1% | Nao |
| AQUEC40_ORIG | AQUEC40_FAV | 30 | 24,3% | Nao |
| BQR35_FAV | BQR35 | 24 | 17,1% | Nao |
| BQR40_FAV | BQR35 | 20 | 16,1% | Nao |
| BQR35_SCORE | BQR35 | 30 | 14,5% | Nao |

Regra final: **sobreposicao nao exclui leitura, mas bloqueia soma**.

---

## 4. Proibicoes finais

A pesquisa encerrada nao permite:

1. Operacao real.
2. Robo.
3. Cashout.
4. Carteira.
5. ROI global.
6. Uso de odds medias como odds reais.
7. Soma entre representantes e refinamentos sem dedup por fixture.

---

## 5. Artefatos finais de leitura

Documentos principais:

```text
docs/04_RESEARCH/COMPLETED/GOAL_HT_V1_PREMIER_LEAGUE_2025_26.md
docs/04_RESEARCH/COMPLETED/HT_GOAL_RESEARCH_V1_FINAL_CLOSURE.md
```

A META-03 V2 e a META-04 V2 sao os artefatos metodologicos finais da frente em `docs/04_RESEARCH/primeiro_tempo/...`.

---

## 6. Motivo do encerramento

A frente cumpriu seu objetivo:

1. Descobriu candidatos.
2. Validou financeiramente com odds medias.
3. Corrigiu candidatos/observacoes.
4. Corrigiu familias macro.
5. Auditou sobreposicao.
6. Selecionou representantes globais.
7. Documentou reprodutibilidade.

Novas ideias devem nascer em frentes separadas.

---

## 7. Proxima frente aberta

A proxima frente e:

```text
HT_JANELAS_CASHOUT_V1
```

Essa nova frente estudara janelas de 5/10/15 minutos antes da entrada e comparara OLD contra cashout estimado.
