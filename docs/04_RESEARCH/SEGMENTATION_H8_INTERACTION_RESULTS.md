# Segmentation H8 Interaction Results

Data: 2026-06-07 12:04:24 UTC

## Resumo Executivo

Validacao estatistica executada para interacoes entre Segmentacao Dinamica e H8 no cutoff de **60 minutos**, usando target `target_late_goal_75`.

Amostra base: **320 partidas segmentaveis**. Para `momentum_trend_last_10m`, a amostra efetiva foi **319** por causa do `graph_known_missing`. Para `shots_last_10m`, a amostra efetiva foi **320**.

Resultado: 1 das 6 interacoes atingiu criterio `PROMISSOR`: **defensivo_fragile + shots_last_10m**, com N=52, taxa=65.4%, diff=+15.4 p.p., OR=2.10 e p-value=0.0224. A maior diferenca bruta foi **ofensivo_forte_vs_defesa_fragil + shots_last_10m**, mas com N=20, portanto classificada como `OBSERVAR`.

## Respostas Objetivas

1. Existe interacao superior a segmentacao isolada? **Sim**.
2. Existe interacao superior ao H8 isolado? **Sim**.
3. Qual combinacao apresentou maior efeito? **ofensivo_forte_vs_defesa_fragil + shots_last_10m**.
4. Existe pelo menos uma interacao PROMISSORA? **Sim**.

## Fontes Usadas

- `data/processed/datasets/team_profile_segment_dataset_v1.csv`
- `data/processed/datasets/late_goal_dataset_h8_v1.csv`

Nenhuma escrita em PostgreSQL foi realizada. Nenhum schema, importer, crawler, raw data, modelo, baseline, backtesting ou artefato de producao foi alterado.

## Metodologia

- Target: `target_late_goal_75`.
- Cutoff H8: `60` minutos.
- Segmentos permitidos:
  - `ofensivo_forte_vs_defesa_fragil`;
  - `ofensivo_strong`, operacionalizado como `ao_menos_um_ofensivo_forte`;
  - `defensivo_fragile`, operacionalizado como `ao_menos_uma_defesa_fragil`.
- Features H8 permitidas:
  - `momentum_trend_last_10m`;
  - `shots_last_10m`.
- Total de interacoes testadas: 6.
- Interacao = segmento ativo AND sinal H8 ativo.

## Regras dos Sinais H8

- `momentum_trend_last_10m >= 18.000 (tercil superior)`.
- `shots_last_10m >= 4 (acima do tercil superior discreto; q66=3.000)`.

Essas regras foram usadas apenas para validacao estatistica exploratoria, sem criar feature permanente ou modelo.

## Validacoes Anti-Leakage

- Segmentos vieram de perfis historicos calculados com `shift(1)` e sem uso da propria partida.
- H8 usa somente cutoff 60 e features permitidas.
- Target foi usado apenas como variavel resposta.
- Nenhuma coluna derivada do target foi usada como explicativa.
- Nenhum evento apos o cutoff foi usado nas features H8.

## Efeitos Isolados dos Segmentos

| Item | N | Pos | Neg | Taxa | Taxa geral | Dif. p.p. | OR | IC 95% | p-value | Classe |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| ofensivo_forte_vs_defesa_fragil | 56 | 32 | 24 | 57.1% | 50.0% | +7.1 | 1.41 | [0.79, 2.51] | 0.3031 | OBSERVAR |
| ofensivo_strong | 177 | 88 | 89 | 49.7% | 50.0% | -0.3 | 0.98 | [0.63, 1.51] | 1.0000 | DESCARTAR |
| defensivo_fragile | 163 | 83 | 80 | 50.9% | 50.0% | +0.9 | 1.08 | [0.70, 1.67] | 0.8231 | DESCARTAR |

## Efeitos Isolados H8

| Item | N | Pos | Neg | Taxa | Taxa geral | Dif. p.p. | OR | IC 95% | p-value | Classe |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| momentum_trend_last_10m | 107 | 43 | 64 | 40.2% | 50.2% | -10.0 | 0.55 | [0.34, 0.88] | 0.0129 | DESCARTAR |
| shots_last_10m | 98 | 53 | 45 | 54.1% | 50.0% | +4.1 | 1.26 | [0.79, 2.03] | 0.3960 | DESCARTAR |

## Interacoes Segmentacao x H8

| Interacao | N | Pos | Neg | Taxa | Geral | Dif. p.p. | OR | IC 95% | p-value | Classe | > Segmento | > H8 |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---:|
| ofensivo_forte_vs_defesa_fragil + momentum_trend_last_10m | 16 | 8 | 8 | 50.0% | 50.2% | -0.2 | 0.99 | [0.37, 2.64] | 1.0000 | DESCARTAR | nao | sim |
| ofensivo_forte_vs_defesa_fragil + shots_last_10m | 20 | 15 | 5 | 75.0% | 50.0% | +25.0 | 3.01 | [1.11, 8.18] | 0.0353 | OBSERVAR | sim | sim |
| ofensivo_strong + momentum_trend_last_10m | 59 | 25 | 34 | 42.4% | 50.2% | -7.8 | 0.68 | [0.39, 1.21] | 0.1971 | DESCARTAR | nao | sim |
| ofensivo_strong + shots_last_10m | 56 | 28 | 28 | 50.0% | 50.0% | +0.0 | 1.00 | [0.56, 1.77] | 1.0000 | DESCARTAR | sim | nao |
| defensivo_fragile + momentum_trend_last_10m | 52 | 22 | 30 | 42.3% | 50.2% | -7.8 | 0.69 | [0.38, 1.25] | 0.2288 | DESCARTAR | nao | sim |
| defensivo_fragile + shots_last_10m | 52 | 34 | 18 | 65.4% | 50.0% | +15.4 | 2.10 | [1.14, 3.88] | 0.0224 | PROMISSOR | sim | sim |

## Classificacao das Interacoes

### PROMISSOR

- defensivo_fragile + shots_last_10m: N=52, taxa=65.4%, diff=+15.4 p.p., p=0.0224

### OBSERVAR

- ofensivo_forte_vs_defesa_fragil + shots_last_10m: N=20, taxa=75.0%, diff=+25.0 p.p., p=0.0353

### DESCARTAR

- ofensivo_forte_vs_defesa_fragil + momentum_trend_last_10m: N=16, taxa=50.0%, diff=-0.2 p.p., p=1.0000
- ofensivo_strong + momentum_trend_last_10m: N=59, taxa=42.4%, diff=-7.8 p.p., p=0.1971
- ofensivo_strong + shots_last_10m: N=56, taxa=50.0%, diff=+0.0 p.p., p=1.0000
- defensivo_fragile + momentum_trend_last_10m: N=52, taxa=42.3%, diff=-7.8 p.p., p=0.2288

## Leitura Quantitativa

As interacoes com `shots_last_10m` concentraram o sinal positivo. A combinacao `defensivo_fragile + shots_last_10m` superou tanto o segmento isolado quanto o H8 isolado e atingiu criterio PROMISSOR. Ainda assim, a evidencia permanece exploratoria e deve ser revisada pelo Quant antes de qualquer baseline.

## Limitacoes

- Apenas uma temporada EPL foi avaliada.
- O plano `SEGMENTATION_H8_INTERACTION_PLAN.md` esta truncado no GitHub; esta execucao seguiu os parametros explicitos da tarefa.
- A definicao de H8 ativo por tercil superior e exploratoria e nao deve virar feature permanente sem aprovacao Quant.
- Multiplos testes foram executados sem correcao formal.
- `momentum_trend_last_10m` tem uma partida ausente por `graph_known_missing`.

## Recomendacao

Encaminhar ao Quant Research para revisar a interacao `defensivo_fragile + shots_last_10m` como candidata PROMISSORA e manter `ofensivo_forte_vs_defesa_fragil + shots_last_10m` em OBSERVAR por amostra pequena. Nao iniciar baseline, modelo ou backtesting antes da classificacao formal do Quant.

## Status Final

Status: VALIDACAO ESTATISTICA INICIAL CONCLUIDA.
