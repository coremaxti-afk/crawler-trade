# STATISTICAL VALIDATION H1/H2

## Status

BLOQUEADO por risco de data leakage.

Nenhuma validacao estatistica H1/H2 foi executada, porque nao foi encontrada uma fonte comprovadamente pre-jogo para xG, xGA, forecast, probabilidades pre-jogo ou diferencas entre equipes.

Nenhuma modelagem foi iniciada. Nenhum dataset existente, PostgreSQL, schema, crawler ou importer foi alterado.

---

## Objetivo

Avaliar H1/H2 somente com variaveis comprovadamente disponiveis antes do kickoff:

- xG pre-jogo;
- xGA pre-jogo;
- forecast;
- probabilidades pre-jogo;
- diferencas entre equipes.

Regra aplicada:

- se a origem for pos-jogo ou ambigua, a variavel nao deve ser usada.

---

## Verificacao Executada

Foram inspecionados os scripts e tabelas locais relacionados a Understat:

- `Crawler/Understats/understat_import_epl.py`
- `Crawler/Understats/understat_import_team_stats.py`
- tabela `matches`
- tabela `matches_master`
- tabela `team_match_stats`
- tabela `snapshots`

Consultas executadas:

- listagem de tabelas do schema publico;
- listagem de colunas contendo `xg`, `xga`, `forecast`, `ppda` e `deep`;
- contagens de `matches`, `matches_master`, `team_match_stats` e `match_mapping`;
- amostra de registros Understat importados.

---

## Evidencias Encontradas

### 1. `understat_import_epl.py`

O script importa dados de:

- `https://understat.com/getLeagueData/EPL/2024`

Campos lidos do mesmo objeto `match`:

- `goals.h`
- `goals.a`
- `xG.h`
- `xG.a`
- `forecast.w`
- `forecast.d`
- `forecast.l`

Interpretação metodológica:

- `goals` são resultado final da partida.
- `xG.h` e `xG.a` representam xG da própria partida.
- `forecast` vem no mesmo registro final da partida e não foi comprovado como probabilidade pre-kickoff.
- Portanto, estes campos são pós-jogo ou ambíguos e não podem ser usados como pré-jogo.

### 2. Tabela `matches`

Contagem:

- `matches`: 380 registros.

Campos candidatos existentes:

- `home_xg`
- `away_xg`
- `forecast_home_win`
- `forecast_draw`
- `forecast_away_win`

Amostra observada:

- Manchester United x Fulham: `home_xg=2.0427`, `away_xg=0.4187`, placar 1-0.
- Ipswich x Liverpool: `home_xg=0.3426`, `away_xg=3.9291`, placar 0-2.
- Arsenal x Wolverhampton: `home_xg=1.6283`, `away_xg=0.5758`, placar 2-0.

Interpretação metodológica:

- Os valores de `home_xg`/`away_xg` descrevem a producao de chances da partida jogada.
- Nao sao xG pre-jogo.
- `forecast_*` foi importado junto com xG/placar do jogo finalizado e permanece ambiguo para uso pre-jogo.

### 3. Tabela `matches_master`

Contagem:

- `matches_master`: 380 registros.

Campos candidatos:

- `home_xg`
- `away_xg`
- `forecast_home`
- `forecast_draw`
- `forecast_away`

Disponibilidade observada:

- `home_xg`: 0 nao nulos.
- `away_xg`: 0 nao nulos.
- `forecast_home`: 0 nao nulos.
- `forecast_draw`: 0 nao nulos.
- `forecast_away`: 0 nao nulos.

Interpretação metodológica:

- `matches_master` nao possui dados pre-jogo utilizaveis para H1/H2 neste momento.

### 4. Tabela `team_match_stats`

Contagem:

- `team_match_stats`: 760 registros.

Campos candidatos:

- `xg`
- `xga`
- `npxg`
- `npxga`
- `ppda_att`
- `ppda_def`
- `deep`
- `deep_allowed`
- `xpts`
- `pts`
- `result`

Amostra observada:

- Manchester United no jogo contra Fulham: `xg=2.0427`, `xga=0.4187`, `scored=1`, `missed=0`, `result=w`.
- Fulham no mesmo jogo: `xg=0.4187`, `xga=2.0427`, `scored=0`, `missed=1`, `result=l`.

Interpretação metodológica:

- A tabela representa estatisticas finais por time por partida.
- Estes dados podem servir futuramente para construir medias historicas anteriores ao jogo.
- No estado atual, nao existe feature materializada de media historica pre-jogo.
- Usar a linha da propria partida como xG/xGA pre-jogo seria leakage.

### 5. Tabela `snapshots`

Contagem observada:

- `snapshots`: 90 registros.

Interpretação metodológica:

- A tabela possui dados por minuto/in-game, nao pre-kickoff.
- Nao atende H1/H2 pre-jogo.

---

## Variaveis Avaliadas

| Variavel solicitada | Fonte candidata | Momento disponivel comprovado | Amostra segura | Teste estatistico | p-value | Efeito | Recomendacao |
| --- | --- | --- | ---: | --- | ---: | --- | --- |
| xG pre-jogo | `matches.home_xg`, `matches.away_xg`, `team_match_stats.xg` | Pos-jogo / propria partida | 0 | Nao executado | n/a | n/a | BLOQUEAR |
| xGA pre-jogo | `team_match_stats.xga` | Pos-jogo / propria partida | 0 | Nao executado | n/a | n/a | BLOQUEAR |
| forecast | `matches.forecast_*` | Ambiguo; importado junto com resultado/xG final | 0 | Nao executado | n/a | n/a | BLOQUEAR |
| probabilidades pre-jogo | Nenhuma fonte segura encontrada | Nao disponivel | 0 | Nao executado | n/a | n/a | BLOQUEAR |
| diferencas entre equipes | Requer medias historicas pre-jogo nao materializadas | Nao disponivel | 0 | Nao executado | n/a | n/a | BLOQUEAR |

---

## Metodologia Aplicada

1. Buscar campos candidatos no banco.
2. Rastrear a origem dos campos nos importers Understat.
3. Verificar se os campos foram produzidos antes ou depois do kickoff.
4. Rejeitar qualquer campo com origem pós-jogo ou ambigua.
5. Somente executar teste estatistico se a variavel for comprovadamente pre-jogo.

Resultado:

- Nenhuma variavel H1/H2 passou no controle de disponibilidade temporal.
- A validacao estatistica foi bloqueada antes da etapa de teste.

---

## Ranking Preliminar das Features H1/H2

Ranking por prontidao metodologica atual:

| Rank | Feature | Status | Justificativa |
| ---: | --- | --- | --- |
| 1 | Historico pre-jogo de xG medio do mandante/visitante | FUTURA | Pode ser derivada de `team_match_stats`, mas somente usando jogos anteriores a cada partida. Ainda nao existe materializada. |
| 2 | Historico pre-jogo de xGA medio do mandante/visitante | FUTURA | Mesma regra: apenas jogos anteriores. Ainda nao existe materializada. |
| 3 | Diferenca pre-jogo de forca ofensiva/defensiva | FUTURA | Depende das medias historicas anteriores. Ainda nao existe materializada. |
| 4 | Forecast pre-jogo | BLOQUEADA | `forecast_*` atual e ambiguo e vem junto do registro final Understat. |
| 5 | Probabilidades pre-jogo externas | NAO DISPONIVEL | Nenhuma fonte segura versionada/importada foi encontrada. |
| 6 | xG final da partida | PROIBIDA | Dado pos-jogo, uso como preditor causaria leakage. |

---

## Recomendacoes

### Manter para etapa futura

- Construir, em tarefa separada e aprovada, features historicas pre-jogo a partir de `team_match_stats`, usando somente partidas anteriores no tempo.
- Exemplos futuros:
  - `home_team_avg_xg_before_match`
  - `away_team_avg_xg_before_match`
  - `home_team_avg_xga_before_match`
  - `away_team_avg_xga_before_match`
  - `pre_match_xg_diff`
  - `pre_match_xga_diff`

### Observar

- `forecast_*` Understat precisa de confirmacao documental ou empirica antes de qualquer uso como probabilidade pre-jogo.
- Se nao houver prova de disponibilidade pre-kickoff, deve permanecer bloqueado.

### Descartar / Proibir nesta etapa

- `matches.home_xg`
- `matches.away_xg`
- `team_match_stats.xg` da propria partida
- `team_match_stats.xga` da propria partida
- `xpts`, `pts`, `result`, `scored`, `missed` da propria partida
- qualquer campo calculado com informacao da partida analisada depois do kickoff.

---

## Limitacoes

- A validacao H1/H2 nao foi executada estatisticamente porque as variaveis seguras nao existem no estado atual.
- O banco possui dados Understat úteis, mas em formato pos-jogo por partida.
- A construcao correta de H1/H2 exige feature engineering temporal com janela historica anterior a cada partida.
- Essa construcao nao foi feita aqui porque a tarefa proibiu criar feature engineering executavel e alterar datasets existentes.

---

## Conclusao

H1/H2 estao BLOQUEADAS neste momento por risco de data leakage.

Nao ha xG pre-jogo, xGA pre-jogo, forecast pre-jogo ou probabilidades pre-jogo comprovadamente disponiveis antes do kickoff nos artefatos atuais.

A proxima etapa correta e solicitar uma tarefa separada para construir um dataset pre-jogo historico, com features calculadas exclusivamente a partir de jogos anteriores a cada partida. Somente depois disso H1/H2 devem ser testadas estatisticamente.
