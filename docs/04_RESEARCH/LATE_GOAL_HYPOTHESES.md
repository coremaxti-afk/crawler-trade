# LATE GOAL HYPOTHESES — LateGoalResearch

## Objetivo

Este documento registra as hipóteses quantitativas H1-H9 do projeto **LateGoalResearch**.

A finalidade é orientar a criação de features, definição de targets, validação estatística e modelagem preditiva para gols tardios no futebol.

---

## Definição Inicial de Gol Tardio

Definição operacional inicial:

- gol marcado a partir dos 75 minutos, incluindo acréscimos.

Targets alternativos que poderão ser testados:

- gol após 80 minutos;
- gol após 85 minutos;
- próximo gol após minuto X;
- gol tardio do mandante;
- gol tardio do visitante;
- over 0.5 gols entre 75' e fim;
- over 0.5 gols entre 80' e fim.

A definição final do target deve ser validada pelo agente **Quant Research / Data Science** antes de modelagem.

---

## Princípio de Antivazamento

Nenhuma feature pode usar informação posterior ao minuto de previsão.

Exemplo:

- Se o modelo tenta prever gol após 75', as features in-game só podem usar dados disponíveis até o minuto 75.

Features pré-jogo e features in-game devem ser separadas de forma explícita.

---

## Fontes Relevantes

### Understat

Uso principal:

- xG;
- xGA;
- forecast pré-jogo;
- PPDA;
- deep completions;
- força ofensiva/defensiva pré-jogo.

### SofaScore

Uso principal:

- dados gerais da partida;
- estatísticas agregadas;
- incidentes com minuto;
- escalações, quando coletadas;
- h2h, quando coletado;
- graph/momentum, quando implementado.

### FotMob

Uso previsto:

- fonte complementar de validação;
- possível cobertura alternativa para eventos, estatísticas e momentum.

### OddsPortal

Uso futuro:

- odds pré-jogo;
- odds históricas;
- sinal de expectativa de mercado.

---

## H1 — xG Pré-Jogo

Hipótese:

Times com maior força esperada pré-jogo, medida por xG médio, xGA médio e métricas derivadas, apresentam maior probabilidade de participar de partidas com gols tardios.

Tipo:

- pré-jogo.

Fontes prováveis:

- Understat.

Features candidatas:

- xG médio do mandante;
- xG médio do visitante;
- xGA médio do mandante;
- xGA médio do visitante;
- diferença de xG;
- soma de xG esperado dos times;
- diferença de xGA.

---

## H2 — Forecast Pré-Jogo

Hipótese:

Probabilidades pré-jogo de vitória/empate/derrota podem antecipar estados de partida mais propensos a gols tardios.

Tipo:

- pré-jogo.

Fontes prováveis:

- Understat;
- OddsPortal, futuramente.

Features candidatas:

- probabilidade de vitória mandante;
- probabilidade de empate;
- probabilidade de vitória visitante;
- equilíbrio pré-jogo;
- favoritismo absoluto;
- entropia do forecast.

---

## H3 — Força Ofensiva

Hipótese:

Times com maior força ofensiva acumulada geram mais pressão e têm maior chance de marcar gols tardios, especialmente quando o placar ainda está aberto.

Tipo:

- pré-jogo e in-game.

Fontes prováveis:

- Understat;
- SofaScore statistics;
- SofaScore incidents.

Features candidatas:

- xG ofensivo médio;
- finalizações;
- finalizações no alvo;
- ataques perigosos, se disponível;
- escanteios;
- volume ofensivo acumulado.

---

## H4 — Fragilidade Defensiva

Hipótese:

Times com maior fragilidade defensiva sofrem mais gols tardios, especialmente sob pressão acumulada.

Tipo:

- pré-jogo e in-game.

Fontes prováveis:

- Understat;
- SofaScore statistics;
- SofaScore incidents.

Features candidatas:

- xGA médio;
- finalizações cedidas;
- finalizações no alvo cedidas;
- escanteios cedidos;
- cartões/expulsões;
- gols sofridos recentes.

---

## H5 — Pressão Ofensiva In-Game

Hipótese:

Pressão ofensiva durante a partida aumenta a probabilidade de gol tardio.

Tipo:

- in-game.

Fontes prováveis:

- SofaScore statistics;
- SofaScore graph/momentum, quando implementado;
- FotMob, se fornecer momentum/eventos.

Features candidatas:

- finalizações até o minuto de corte;
- finalizações no alvo até o minuto de corte;
- escanteios até o minuto de corte;
- ataques perigosos até o minuto de corte, se disponível;
- momentum acumulado, quando disponível;
- pressão nos últimos N minutos, quando graph estiver disponível.

Observação:

Com os dados atuais, sem graph/momentum minuto a minuto, esta hipótese pode ser testada inicialmente apenas de forma limitada com estatísticas agregadas e incidentes.

---

## H6 — Estado Atual da Partida

Hipótese:

O placar e o contexto competitivo da partida influenciam a chance de gol tardio.

Tipo:

- in-game.

Fontes prováveis:

- SofaScore event;
- SofaScore incidents.

Features candidatas:

- placar no minuto de corte;
- diferença de gols;
- jogo empatado;
- favorito perdendo;
- mandante atrás no placar;
- visitante atrás no placar;
- tempo desde último gol.

---

## H7 — Combinação Multi-Fonte

Hipótese:

A combinação de fontes melhora a capacidade preditiva em relação a qualquer fonte isolada.

Tipo:

- pré-jogo e in-game.

Fontes prováveis:

- Understat;
- SofaScore;
- FotMob;
- OddsPortal, futuramente.

Features candidatas:

- features Understat + SofaScore;
- divergência entre xG esperado e placar real;
- força pré-jogo + estado in-game;
- odds/favoritismo + pressão in-game, futuramente.

---

## H8 — Momentum e Pressão Temporal

Hipótese:

Variações temporais de pressão e momentum nos minutos finais antecipam gols tardios.

Tipo:

- in-game temporal.

Fontes prováveis:

- SofaScore graph/momentum, quando implementado;
- FotMob, se disponível.

Features candidatas:

- momentum médio entre 60' e 75';
- momentum médio entre 70' e 75';
- variação de momentum;
- pressão nos últimos 5/10/15 minutos;
- sequência temporal de domínio ofensivo.

Observação:

Esta hipótese depende de coleta minuto a minuto ou endpoint de graph/momentum. No estado atual, a estrutura `match_graph` existe, mas a coleta do graph ainda precisa ser implementada.

---

## H9 — Eventos Alteram Probabilidade

Hipótese:

Eventos relevantes durante a partida alteram a probabilidade de gol tardio.

Tipo:

- in-game baseada em eventos.

Fontes prováveis:

- SofaScore incidents;
- FotMob events, se disponível.

Features candidatas:

- cartão vermelho;
- cartão amarelo;
- substituições;
- pênaltis;
- gols recentes;
- VAR;
- tempo desde último evento relevante;
- número de substituições antes do minuto de corte.

---

## Prioridade Inicial de Teste

Com os dados já coletados, a ordem inicial recomendada é:

1. H6 — Estado Atual da Partida.
2. H9 — Eventos Alteram Probabilidade.
3. H3 — Força Ofensiva.
4. H4 — Fragilidade Defensiva.
5. H1 — xG Pré-Jogo.
6. H2 — Forecast Pré-Jogo.
7. H7 — Combinação Multi-Fonte.
8. H5 — Pressão Ofensiva In-Game.
9. H8 — Momentum e Pressão Temporal.

Motivo:

- H6 e H9 dependem principalmente de `event.json` e `incidents.json`.
- H3 e H4 podem começar com `statistics.json`.
- H5 e H8 dependem melhor de graph/momentum minuto a minuto, ainda não implementado.

---

## JSONs SofaScore por Prioridade Analítica

### Core

Essenciais para avançar com importer e primeiras análises:

- `event.json`
- `statistics.json`
- `incidents.json`

### Complementares

Úteis, mas não bloqueiam o primeiro dataset:

- `lineups.json`
- `h2h.json`

### Temporal / Futuro

Necessário para momentum e análise minuto a minuto:

- `graph.json` ou endpoint equivalente de momentum.

---

## Status

Documento base criado para estabilizar a governança de pesquisa.

Deve ser revisado pelo agente **Quant Research / Data Science** antes da primeira etapa formal de feature engineering.
