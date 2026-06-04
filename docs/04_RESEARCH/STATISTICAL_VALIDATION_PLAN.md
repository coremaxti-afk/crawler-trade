# STATISTICAL VALIDATION PLAN

## Status

Plano metodologico formal.

Nao implementado.

Nao contem codigo.

Nao contem SQL.

Nao inicia modelagem.

---

## Objetivo

Definir como as hipoteses H1-H9 serao avaliadas estatisticamente antes de qualquer modelo preditivo.

Principio central:

- validar se existe sinal estatistico consistente antes de modelar.

Nao confundir:

- correlacao;
- associacao estatistica;
- capacidade preditiva.

---

## Regras Gerais

Antes de qualquer teste:

1. Auditar targets.
2. Auditar granularidade temporal.
3. Auditar risco de leakage.
4. Confirmar fonte das features.
5. Confirmar janela historica.

Proibido:

- usar dados futuros;
- usar split aleatorio como validacao principal;
- iniciar modelo antes da validacao metodologica.

---

## Sequencia Oficial de Validacao

1. Validacao do target.
2. H6 Estado Atual da Partida.
3. H9 Eventos Alteram Probabilidade.
4. H1 xG Pre-Jogo.
5. H2 Forecast Pre-Jogo.
6. H3 Forca Ofensiva.
7. H4 Fragilidade Defensiva.
8. H7 Combinacao Multi-Fonte.
9. H5 Pressao Ofensiva In-Game.
10. H8 Momentum e Pressao Temporal.

Motivo:

- priorizar hipoteses suportadas pela base atual.
- deixar graph/momentum para etapa posterior.

---

## Etapa 0 - Validacao do Target

Objetivo:

- garantir que os targets representam corretamente os incidentes.

Amostra obrigatoria:

- partidas sem gols;
- partidas com gol apos 75;
- partidas com gol apos 80;
- partidas com gol apos 85;
- partidas com acrescimos;
- partidas com multiplos gols tardios.

Criterio de aceite:

- 100% de concordancia entre leitura manual e target calculado.

---

## H1 - xG Pre-Jogo

Hipotese:

- partidas com maior expectativa ofensiva possuem maior probabilidade de gol tardio.

Target:

- `target_late_goal_75`.

Analises:

- quartis de xG.
- taxa de gol tardio por quartil.
- odds ratio entre quartil superior e inferior.

Evidencia desejada:

- relacao monotonicamente crescente.

---

## H2 - Forecast Pre-Jogo

Hipotese:

- probabilidades pre-jogo carregam informacao util para gols tardios.

Target:

- `target_late_goal_75`.

Analises:

- bins de forecast.
- equilibrio vs desequilibrio.
- taxa de gol tardio por grupo.

Evidencia desejada:

- diferenca estatisticamente consistente entre grupos.

---

## H3 - Forca Ofensiva

Hipotese:

- equipes ofensivamente fortes marcam mais gols tardios.

Targets:

- `target_home_late_goal_75`.
- `target_away_late_goal_75`.

Analises:

- quartis de forca ofensiva.
- taxa de gol tardio por quartil.
- comparacao entre extremos.

Regra obrigatoria:

- usar apenas historico anterior a partida.

---

## H4 - Fragilidade Defensiva

Hipotese:

- equipes defensivamente frageis sofrem mais gols tardios.

Targets:

- gol tardio sofrido por lado.

Analises:

- quartis de fragilidade.
- taxa de gol tardio sofrido.
- comparacao entre extremos.

Regra obrigatoria:

- usar apenas historico anterior a partida.

---

## H5 - Pressao Ofensiva In-Game

Hipotese:

- pressao ofensiva aumenta a probabilidade de gol futuro.

Target:

- `target_goal_after_cutoff_X`.

Status:

- depende de granularidade temporal valida.

Nao validar enquanto:

- estatisticas estiverem apenas em formato full-match.

---

## H6 - Estado Atual da Partida

Hipotese:

- o estado atual do placar altera a probabilidade de gols futuros.

Target:

- `target_goal_after_cutoff_X`.

Analises:

- 0x0.
- empate com gols.
- mandante vencendo.
- visitante vencendo.
- vantagem de dois ou mais gols.

Evidencia desejada:

- diferencas claras na taxa de gol futuro.

---

## H7 - Combinacao Multi-Fonte

Hipotese:

- diferentes fontes contem informacao complementar.

Targets:

- `target_late_goal_75`.
- `target_goal_after_cutoff_X`.

Analises:

- comparar blocos separadamente.
- medir ganho incremental conceitual.

Blocos:

- pre-jogo.
- incidents.
- statistics temporais.
- graph futuro.

---

## H8 - Momentum e Pressao Temporal

Hipotese:

- momentum recente possui sinal preditivo para gols tardios.

Target:

- `target_goal_after_cutoff_X`.

Status:

- adiado ate disponibilidade de `match_graph`.

Nao validar:

- usando proxies inadequados como substituto definitivo de momentum.

---

## H9 - Eventos Alteram Probabilidade

Hipotese:

- eventos recentes alteram a probabilidade de gol futuro.

Target:

- `target_goal_after_cutoff_X`.

Eventos candidatos:

- gol recente.
- cartao vermelho.
- cartao amarelo.
- substituicoes.
- penalti.
- VAR.

Analises:

- taxa de gol futuro apos evento.
- comparacao contra ausencia do evento.

---

## Testes Estatisticos Recomendados

Dependendo da distribuicao e da amostra:

- Qui-quadrado.
- Fisher.
- Odds Ratio.
- Intervalos de confianca.

Objetivo:

- medir associacao.
- nao construir modelo.

---

## Validacao Temporal

Obrigatoria.

Nunca usar validacao aleatoria como principal.

Exemplos aceitaveis:

- temporadas antigas -> temporadas novas.
- rodadas antigas -> rodadas recentes.

Objetivo:

- simular uso real.

---

## Critério para Encerrar a Fase Metodologica

A fase metodologica sera considerada encerrada quando:

- targets estiverem especificados;
- catalogo de features estiver definido;
- riscos de leakage estiverem documentados;
- plano de validacao estiver documentado;
- PM aprovar os artefatos.

---

## Fora do Escopo Deste Documento

- codigo;
- SQL;
- implementacao de dataset;
- modelagem;
- tuning;
- backtesting financeiro;
- producao.
