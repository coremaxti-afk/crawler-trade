# Team Profile Segmentation Results

Data: 2026-06-07 04:33:59 UTC

## Resumo Executivo

A analise exploratoria de segmentacao dinamica por perfil de equipes foi executada com perfis expansivos calculados apenas com jogos anteriores do proprio time. A amostra operacional contem **380 partidas**, **642 linhas-time elegiveis** e **321 confrontos elegiveis** apos exigir `min_games >= 5` para os dois times.

Resultado principal: foram encontrados segmentos com efeito positivo relevante em gols tardios, principalmente em combinacoes de **ofensivo forte** e **defesa fragil**, mas a maioria dos achados deve ser tratada como exploratoria. A evidencia e suficiente para orientar nova validacao controlada, nao para modelagem, baseline operacional ou decisao de producao.

Documento base solicitado: `docs/04_RESEARCH/TEAM_PROFILE_SEGMENTATION_EXPLORATION.md` nao foi encontrado localmente nem no GitHub no momento da execucao. A analise seguiu integralmente a metodologia especificada na tarefa.

## Fontes Usadas

- PostgreSQL somente leitura.
- `matches_master` para identificacao da partida, data, times e placar final usado apenas como historico para jogos futuros.
- `match_statistics` para estatisticas finais usadas apenas no perfil historico de jogos posteriores.
- `match_incidents` para gols e targets tardios.

Nenhuma escrita no PostgreSQL foi executada. Nenhum crawler, importer, schema, dataset existente ou dado bruto foi alterado.

## Metodologia Anti-Leakage

- Grain de perfil: 1 linha por time por partida.
- Para cada time, os perfis foram ordenados por `season`, `team_name`, `match_date`, `match_id`.
- Cada metrica de perfil usa `groupby(season, team_name).shift(1)` antes de qualquer media expansiva.
- A partida analisada nunca entra no proprio perfil.
- Partidas futuras nunca entram no perfil.
- A primeira partida elegivel de um time exige `history_matches_available >= 5`.
- As categorias dinamicas de perfil foram recalculadas por data com informacao disponivel ate aquela data, baseada em perfis ja formados por historico anterior.
- O target usa gols com `minute > cutoff`, onde cutoff pertence a [60, 65, 70, 75].

## Definicao dos Perfis

### Perfil Ofensivo

Indice ofensivo historico expansivo composto por:

- gols a favor;
- finalizacoes a favor;
- finalizacoes no alvo a favor;
- grandes chances a favor.

Classificacao dinamica:

- `strong`: tercil superior do indice ofensivo historico disponivel;
- `middle`: tercil intermediario;
- `weak`: tercil inferior.

### Perfil Defensivo

Indice de fragilidade defensiva historico expansivo composto por:

- gols sofridos;
- finalizacoes contra;
- finalizacoes no alvo contra;
- grandes chances contra.

Classificacao dinamica:

- `fragile`: tercil superior de fragilidade;
- `middle`: tercil intermediario;
- `strong`: tercil inferior de fragilidade, isto e, defesa mais forte.

## Cobertura

- Partidas totais analisadas: **380**.
- Linhas-time totais: **760**.
- Linhas-time elegiveis: **642**.
- Confrontos totais: **380**.
- Confrontos elegiveis: **321**.
- `min_games`: **5**.
- Cutoffs avaliados: **60, 65, 70, 75**.

Distribuicao dos perfis ofensivos elegiveis: `{"middle": 243, "strong": 206, "weak": 193}`.

Distribuicao dos perfis defensivos elegiveis: `{"middle": 258, "strong": 193, "fragile": 191}`.

## Criterios Estatisticos

Para cada segmento e target foram calculados:

- N do segmento;
- positivos e negativos;
- taxa do segmento;
- taxa geral da amostra elegivel;
- diferenca em pontos percentuais;
- odds ratio;
- intervalo de confianca aproximado de 95% para odds ratio;
- p-value por teste exato de Fisher contra o restante da amostra elegivel.

Classificacao aplicada:

- `PROMISSOR`: N >= 30, diferenca positiva >= 5 p.p. e p-value < 0.10.
- `OBSERVAR`: efeito positivo relevante, mas com amostra limitada ou significancia fraca.
- `DESCARTAR`: sem efeito positivo observavel nesta amostra.

## Segmentos Promissores

- confrontos_segmentados / ambos_defesa_forte @ 60: N=30, taxa=83.3%, geral=69.5%, diff=+13.9 p.p., OR=2.18, p=0.0973
- confrontos_segmentados / sem_ofensivo_forte_sem_defesa_fragil @ 60: N=43, taxa=81.4%, geral=69.5%, diff=+11.9 p.p., OR=2.01, p=0.0763
- perfil_defensivo_isolado / defensivo_fragile @ 70: N=191, taxa=44.5%, geral=34.4%, diff=+10.1 p.p., OR=1.86, p=0.0006
- perfil_defensivo_isolado / defensivo_fragile @ 65: N=191, taxa=48.7%, geral=39.1%, diff=+9.6 p.p., OR=1.76, p=0.0014
- perfil_defensivo_isolado / defensivo_fragile @ 75: N=191, taxa=37.7%, geral=28.8%, diff=+8.9 p.p., OR=1.81, p=0.0016
- perfil_defensivo_isolado / defensivo_fragile @ 60: N=191, taxa=51.8%, geral=43.1%, diff=+8.7 p.p., OR=1.65, p=0.0041
- perfil_ofensivo_isolado / ofensivo_strong @ 60: N=206, taxa=50.0%, geral=43.1%, diff=+6.9 p.p., OR=1.50, p=0.0170
- perfil_ofensivo_isolado / ofensivo_strong @ 65: N=206, taxa=45.6%, geral=39.1%, diff=+6.5 p.p., OR=1.49, p=0.0242
- perfil_ofensivo_isolado / ofensivo_strong @ 70: N=206, taxa=40.8%, geral=34.4%, diff=+6.4 p.p., OR=1.50, p=0.0210

## Segmentos Para Observar

- confrontos_segmentados / ambos_defesa_forte @ 65: N=30, taxa=76.7%, geral=64.8%, diff=+11.9 p.p., OR=1.80, p=0.1665
- confrontos_segmentados / ofensivo_forte_vs_defesa_fragil @ 65: N=58, taxa=74.1%, geral=64.8%, diff=+9.3 p.p., OR=1.67, p=0.1284
- confrontos_segmentados / ofensivo_forte_vs_defesa_fragil @ 70: N=58, taxa=67.2%, geral=58.3%, diff=+9.0 p.p., OR=1.58, p=0.1424
- confrontos_segmentados / ofensivo_forte_vs_defesa_fragil @ 75: N=58, taxa=56.9%, geral=49.8%, diff=+7.1 p.p., OR=1.41, p=0.2490
- confrontos_segmentados / ofensivo_forte_vs_defesa_fragil @ 60: N=58, taxa=75.9%, geral=69.5%, diff=+6.4 p.p., OR=1.44, p=0.2731
- confrontos_segmentados / ofensivo_forte_vs_ofensivo_forte @ 65: N=27, taxa=70.4%, geral=64.8%, diff=+5.6 p.p., OR=1.28, p=0.6745
- confrontos_segmentados / ambos_defesa_forte @ 70: N=30, taxa=63.3%, geral=58.3%, diff=+5.1 p.p., OR=1.24, p=0.6980
- perfil_ofensivo_isolado / ofensivo_strong @ 75: N=206, taxa=33.0%, geral=28.8%, diff=+4.2 p.p., OR=1.34, p=0.1131

## Segmentos Descartados

- Segmentos sem efeito positivo consistente foram classificados como DESCARTAR nesta amostra. A lista completa por cutoff esta nas tabelas abaixo.

## Perfil Ofensivo Isolado vs Gols Tardios do Time

| Cutoff | Segmento | N | Pos | Neg | Taxa seg. | Taxa geral | Dif. p.p. | OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 60 | ofensivo_strong | 206 | 103 | 103 | 50.0% | 43.1% | +6.9 | 1.50 | 0.0170 | PROMISSOR |
| 60 | ofensivo_middle | 243 | 110 | 133 | 45.3% | 43.1% | +2.1 | 1.15 | 0.4121 | DESCARTAR |
| 60 | ofensivo_weak | 193 | 64 | 129 | 33.2% | 43.1% | -10.0 | 0.55 | 0.0009 | DESCARTAR |
| 65 | ofensivo_strong | 206 | 94 | 112 | 45.6% | 39.1% | +6.5 | 1.49 | 0.0242 | PROMISSOR |
| 65 | ofensivo_middle | 243 | 98 | 145 | 40.3% | 39.1% | +1.2 | 1.09 | 0.6181 | DESCARTAR |
| 65 | ofensivo_weak | 193 | 59 | 134 | 30.6% | 39.1% | -8.5 | 0.59 | 0.0037 | DESCARTAR |
| 70 | ofensivo_strong | 206 | 84 | 122 | 40.8% | 34.4% | +6.4 | 1.50 | 0.0210 | PROMISSOR |
| 70 | ofensivo_middle | 243 | 85 | 158 | 35.0% | 34.4% | +0.6 | 1.04 | 0.8641 | DESCARTAR |
| 70 | ofensivo_weak | 193 | 52 | 141 | 26.9% | 34.4% | -7.5 | 0.61 | 0.0088 | DESCARTAR |
| 75 | ofensivo_strong | 206 | 68 | 138 | 33.0% | 28.8% | +4.2 | 1.34 | 0.1131 | OBSERVAR |
| 75 | ofensivo_middle | 243 | 74 | 169 | 30.5% | 28.8% | +1.6 | 1.14 | 0.4740 | DESCARTAR |
| 75 | ofensivo_weak | 193 | 43 | 150 | 22.3% | 28.8% | -6.5 | 0.62 | 0.0175 | DESCARTAR |

## Perfil Defensivo Isolado vs Gols Tardios Sofridos

| Cutoff | Segmento | N | Pos | Neg | Taxa seg. | Taxa geral | Dif. p.p. | OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 60 | defensivo_fragile | 191 | 99 | 92 | 51.8% | 43.1% | +8.7 | 1.65 | 0.0041 | PROMISSOR |
| 60 | defensivo_strong | 193 | 78 | 115 | 40.4% | 43.1% | -2.7 | 0.85 | 0.3854 | DESCARTAR |
| 60 | defensivo_middle | 258 | 100 | 158 | 38.8% | 43.1% | -4.4 | 0.74 | 0.0738 | DESCARTAR |
| 65 | defensivo_fragile | 191 | 93 | 98 | 48.7% | 39.1% | +9.6 | 1.76 | 0.0014 | PROMISSOR |
| 65 | defensivo_strong | 193 | 69 | 124 | 35.8% | 39.1% | -3.3 | 0.82 | 0.2899 | DESCARTAR |
| 65 | defensivo_middle | 258 | 89 | 169 | 34.5% | 39.1% | -4.6 | 0.72 | 0.0577 | DESCARTAR |
| 70 | defensivo_fragile | 191 | 85 | 106 | 44.5% | 34.4% | +10.1 | 1.86 | 0.0006 | PROMISSOR |
| 70 | defensivo_strong | 193 | 59 | 134 | 30.6% | 34.4% | -3.9 | 0.78 | 0.2047 | DESCARTAR |
| 70 | defensivo_middle | 258 | 77 | 181 | 29.8% | 34.4% | -4.6 | 0.71 | 0.0513 | DESCARTAR |
| 75 | defensivo_fragile | 191 | 72 | 119 | 37.7% | 28.8% | +8.9 | 1.81 | 0.0016 | PROMISSOR |
| 75 | defensivo_middle | 258 | 65 | 193 | 25.2% | 28.8% | -3.6 | 0.74 | 0.1097 | DESCARTAR |
| 75 | defensivo_strong | 193 | 48 | 145 | 24.9% | 28.8% | -3.9 | 0.76 | 0.1551 | DESCARTAR |

## Confrontos Segmentados vs Gol Tardio na Partida

| Cutoff | Segmento | N | Pos | Neg | Taxa seg. | Taxa geral | Dif. p.p. | OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 60 | ambos_defesa_forte | 30 | 25 | 5 | 83.3% | 69.5% | +13.9 | 2.18 | 0.0973 | PROMISSOR |
| 60 | sem_ofensivo_forte_sem_defesa_fragil | 43 | 35 | 8 | 81.4% | 69.5% | +11.9 | 2.01 | 0.0763 | PROMISSOR |
| 60 | ofensivo_forte_vs_defesa_fragil | 58 | 44 | 14 | 75.9% | 69.5% | +6.4 | 1.44 | 0.2731 | OBSERVAR |
| 60 | ofensivo_forte_vs_ofensivo_forte | 27 | 19 | 8 | 70.4% | 69.5% | +0.9 | 1.02 | 1.0000 | DESCARTAR |
| 60 | ao_menos_um_ofensivo_forte | 179 | 124 | 55 | 69.3% | 69.5% | -0.2 | 0.98 | 1.0000 | DESCARTAR |
| 60 | ao_menos_uma_defesa_fragil | 164 | 111 | 53 | 67.7% | 69.5% | -1.8 | 0.84 | 0.5446 | DESCARTAR |
| 60 | ofensivo_fraco_vs_defesa_forte | 54 | 36 | 18 | 66.7% | 69.5% | -2.8 | 0.85 | 0.6295 | DESCARTAR |
| 60 | defesa_fragil_vs_defesa_fragil | 27 | 15 | 12 | 55.6% | 69.5% | -13.9 | 0.51 | 0.1257 | DESCARTAR |
| 65 | ambos_defesa_forte | 30 | 23 | 7 | 76.7% | 64.8% | +11.9 | 1.80 | 0.1665 | OBSERVAR |
| 65 | ofensivo_forte_vs_defesa_fragil | 58 | 43 | 15 | 74.1% | 64.8% | +9.3 | 1.67 | 0.1284 | OBSERVAR |
| 65 | ofensivo_forte_vs_ofensivo_forte | 27 | 19 | 8 | 70.4% | 64.8% | +5.6 | 1.28 | 0.6745 | OBSERVAR |
| 65 | ao_menos_uma_defesa_fragil | 164 | 108 | 56 | 65.9% | 64.8% | +1.1 | 1.10 | 0.7264 | DESCARTAR |
| 65 | ao_menos_um_ofensivo_forte | 179 | 117 | 62 | 65.4% | 64.8% | +0.6 | 1.06 | 0.8152 | DESCARTAR |
| 65 | sem_ofensivo_forte_sem_defesa_fragil | 43 | 28 | 15 | 65.1% | 64.8% | +0.3 | 1.00 | 1.0000 | DESCARTAR |
| 65 | ofensivo_fraco_vs_defesa_forte | 54 | 33 | 21 | 61.1% | 64.8% | -3.7 | 0.82 | 0.5358 | DESCARTAR |
| 65 | defesa_fragil_vs_defesa_fragil | 27 | 15 | 12 | 55.6% | 64.8% | -9.2 | 0.65 | 0.2996 | DESCARTAR |
| 70 | ofensivo_forte_vs_defesa_fragil | 58 | 39 | 19 | 67.2% | 58.3% | +9.0 | 1.58 | 0.1424 | OBSERVAR |
| 70 | ambos_defesa_forte | 30 | 19 | 11 | 63.3% | 58.3% | +5.1 | 1.24 | 0.6980 | OBSERVAR |
| 70 | ao_menos_uma_defesa_fragil | 164 | 98 | 66 | 59.8% | 58.3% | +1.5 | 1.13 | 0.6508 | DESCARTAR |
| 70 | ofensivo_forte_vs_ofensivo_forte | 27 | 16 | 11 | 59.3% | 58.3% | +1.0 | 1.03 | 1.0000 | DESCARTAR |
| 70 | ao_menos_um_ofensivo_forte | 179 | 105 | 74 | 58.7% | 58.3% | +0.4 | 1.04 | 0.9095 | DESCARTAR |
| 70 | sem_ofensivo_forte_sem_defesa_fragil | 43 | 25 | 18 | 58.1% | 58.3% | -0.1 | 0.99 | 1.0000 | DESCARTAR |
| 70 | ofensivo_fraco_vs_defesa_forte | 54 | 30 | 24 | 55.6% | 58.3% | -2.7 | 0.87 | 0.6538 | DESCARTAR |
| 70 | defesa_fragil_vs_defesa_fragil | 27 | 14 | 13 | 51.9% | 58.3% | -6.4 | 0.75 | 0.5428 | DESCARTAR |
| 75 | ofensivo_forte_vs_defesa_fragil | 58 | 33 | 25 | 56.9% | 49.8% | +7.1 | 1.41 | 0.2490 | OBSERVAR |
| 75 | sem_ofensivo_forte_sem_defesa_fragil | 43 | 23 | 20 | 53.5% | 49.8% | +3.6 | 1.18 | 0.6268 | DESCARTAR |
| 75 | ambos_defesa_forte | 30 | 16 | 14 | 53.3% | 49.8% | +3.5 | 1.16 | 0.7061 | DESCARTAR |
| 75 | ao_menos_uma_defesa_fragil | 164 | 83 | 81 | 50.6% | 49.8% | +0.8 | 1.06 | 0.8236 | DESCARTAR |
| 75 | ao_menos_um_ofensivo_forte | 179 | 89 | 90 | 49.7% | 49.8% | -0.1 | 0.99 | 1.0000 | DESCARTAR |
| 75 | ofensivo_fraco_vs_defesa_forte | 54 | 25 | 29 | 46.3% | 49.8% | -3.5 | 0.85 | 0.6548 | DESCARTAR |
| 75 | ofensivo_forte_vs_ofensivo_forte | 27 | 12 | 15 | 44.4% | 49.8% | -5.4 | 0.80 | 0.6883 | DESCARTAR |
| 75 | defesa_fragil_vs_defesa_fragil | 27 | 12 | 15 | 44.4% | 49.8% | -5.4 | 0.80 | 0.6883 | DESCARTAR |

## Ranking dos Maiores Efeitos Positivos

| Rank | Escopo | Segmento | Cutoff | N | Taxa seg. | Taxa geral | Dif. p.p. | OR | IC 95% OR | p-value | Classe |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | confrontos_segmentados | ambos_defesa_forte | 60 | 30 | 83.3% | 69.5% | +13.9 | 2.18 | [0.84, 5.67] | 0.0973 | PROMISSOR |
| 2 | confrontos_segmentados | sem_ofensivo_forte_sem_defesa_fragil | 60 | 43 | 81.4% | 69.5% | +11.9 | 2.01 | [0.91, 4.42] | 0.0763 | PROMISSOR |
| 3 | confrontos_segmentados | ambos_defesa_forte | 65 | 30 | 76.7% | 64.8% | +11.9 | 1.80 | [0.76, 4.23] | 0.1665 | OBSERVAR |
| 4 | perfil_defensivo_isolado | defensivo_fragile | 70 | 191 | 44.5% | 34.4% | +10.1 | 1.86 | [1.31, 2.63] | 0.0006 | PROMISSOR |
| 5 | perfil_defensivo_isolado | defensivo_fragile | 65 | 191 | 48.7% | 39.1% | +9.6 | 1.76 | [1.25, 2.48] | 0.0014 | PROMISSOR |
| 6 | confrontos_segmentados | ofensivo_forte_vs_defesa_fragil | 65 | 58 | 74.1% | 64.8% | +9.3 | 1.67 | [0.89, 3.14] | 0.1284 | OBSERVAR |
| 7 | confrontos_segmentados | ofensivo_forte_vs_defesa_fragil | 70 | 58 | 67.2% | 58.3% | +9.0 | 1.58 | [0.87, 2.85] | 0.1424 | OBSERVAR |
| 8 | perfil_defensivo_isolado | defensivo_fragile | 75 | 191 | 37.7% | 28.8% | +8.9 | 1.81 | [1.26, 2.60] | 0.0016 | PROMISSOR |
| 9 | perfil_defensivo_isolado | defensivo_fragile | 60 | 191 | 51.8% | 43.1% | +8.7 | 1.65 | [1.17, 2.32] | 0.0041 | PROMISSOR |
| 10 | confrontos_segmentados | ofensivo_forte_vs_defesa_fragil | 75 | 58 | 56.9% | 49.8% | +7.1 | 1.41 | [0.80, 2.48] | 0.2490 | OBSERVAR |

## Leitura dos Resultados

A segmentacao sugere que jogos envolvendo combinacoes de ataque historicamente forte e defesa historicamente fragil podem concentrar maior frequencia de gols tardios em alguns cutoffs. Ainda assim, a analise permanece exploratoria por tres motivos:

1. a amostra elegivel e menor que a base completa por causa da regra `min_games >= 5`;
2. os tercis dinamicos criam segmentos relativamente pequenos em alguns confrontos;
3. a significancia estatistica deve ser tratada como indicativa, pois multiplos segmentos e cutoffs foram testados.

Os resultados negativos ou fracos nao invalidam H3/H4 como familias, mas indicam que segmentacao simples por tercis historicos talvez precise de refinamento antes de virar feature operacional.

## Riscos e Limitacoes

- Estatisticas full-match de uma partida sao usadas apenas depois que essa partida virou historico de jogos futuros do time.
- Como a base cobre uma unica temporada EPL, perfis de inicio de temporada usam poucas partidas e podem ser instaveis.
- Nao foi criada feature permanente nem dataset novo.
- Nao houve correcao formal para multiplos testes; p-values sao exploratorios.
- Odds ratio com intervalo de confianca usa correcao 0.5 quando ha celulas pequenas ou zero.
- O documento base `TEAM_PROFILE_SEGMENTATION_EXPLORATION.md` estava ausente, portanto nao foi possivel comparar contra uma especificacao previa alem da tarefa recebida.

## Recomendacao

1. Encaminhar o relatorio para Quant Research revisar os segmentos `PROMISSOR` e `OBSERVAR`.
2. Se aprovado, criar uma especificacao separada de `Team Profile Segment Feature Builder` com whitelist explicita, sem modelagem ainda.
3. Repetir a validacao com split temporal ou por blocos de rodada antes de qualquer baseline.
4. Nao iniciar backtesting ou producao.

## Status Final

Status: ANALISE EXPLORATORIA CONCLUIDA.

Decisao recomendada: manter a segmentacao dinamica como candidata de pesquisa, com foco inicial nos segmentos classificados como `PROMISSOR` e revisao metodologica dos segmentos `OBSERVAR`.
