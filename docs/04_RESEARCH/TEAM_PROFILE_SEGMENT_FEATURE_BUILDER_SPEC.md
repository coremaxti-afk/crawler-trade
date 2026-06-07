# TEAM PROFILE SEGMENT FEATURE BUILDER SPEC

## Status

Documento metodologico Quant Research.

Commit base de referencia: `ab1de718e4cfba30310ffa2511f5346d459edd7a`.

Status: PRONTO PARA REVISAO PM / QUANT RESEARCH.

Este documento nao contem codigo, nao cria dataset, nao cria modelo, nao executa baseline, nao executa backtesting e nao altera PostgreSQL, schema, importer, crawler ou dados brutos.

---

## 1. Objetivo do Feature Builder

O objetivo do futuro `Team Profile Segment Feature Builder` e gerar features auditaveis de segmentacao dinamica por perfil de equipes, permitindo avaliar se determinados subgrupos de partidas apresentam maior frequencia de gols tardios.

O builder deve transformar historico pre-jogo das equipes em perfis ofensivos, perfis defensivos e segmentos de confronto, respeitando rigorosamente regras anti-leakage.

O escopo metodologico e:

- calcular perfil historico ofensivo de cada time;
- calcular perfil historico defensivo de cada time;
- classificar cada time em grupos dinamicos;
- combinar os perfis dos dois times da partida em segmentos de confronto;
- gerar dataset de features segmentadas com grain definido;
- produzir metadata e validation report;
- manter rastreabilidade suficiente para auditoria Quant/PM.

O builder nao deve decidir se uma feature entra em modelo. Ele apenas gera features candidatas aprovadas para validacao futura.

---

## 2. Arquitetura Rolling/Expanding

A arquitetura oficial deve usar perfis rolling/expanding baseados apenas em partidas anteriores da propria equipe.

Para cada time e temporada:

1. ordenar partidas por `season`, `team_name`, `match_date`, `match_id`;
2. construir uma linha por time por partida;
3. aplicar `groupby(season, team_name).shift(1)` antes de qualquer rolling ou expanding;
4. calcular metricas historicas apenas sobre jogos anteriores;
5. gerar categorias de perfil apenas quando houver historico minimo suficiente.

A abordagem recomendada para V1 e `expanding season-to-date`, pois ela segue diretamente a regra de rodada:

```text
rodada R usa apenas jogos anteriores a rodada R
```

Exemplos obrigatorios:

- rodada 6 usa rodadas 1-5;
- rodada 7 usa rodadas 1-6;
- rodada 8 usa rodadas 1-7.

O builder pode armazenar tambem contadores de janelas rolling futuras, mas a primeira versao deve priorizar o perfil expansivo de temporada para preservar simplicidade e auditabilidade.

---

## 3. Regra de Rodada R

Para cada partida da rodada R:

- nao usar dados da propria partida;
- nao usar dados da propria rodada quando eles dependerem de resultado ocorrido apos o kickoff da partida analisada;
- nao usar jogos futuros;
- nao usar placar final da partida analisada;
- nao usar incidentes da partida analisada;
- nao usar estatisticas full-match da partida analisada como feature dessa mesma partida.

Estatisticas finais de uma partida so podem entrar no perfil de partidas futuras daquele time.

Regra operacional:

```text
profile(team, match_R) = aggregate(team_matches where match_date < kickoff(match_R))
```

Quando a base nao possuir horario de kickoff confiavel e apenas data, o builder deve ser conservador:

- preferir ordenacao por `match_date` e `match_id`;
- registrar a limitacao no validation report;
- manter campos de auditoria para verificar a data maxima usada no historico.

---

## 4. Regra de Historico Minimo

A primeira versao deve exigir:

```text
min_games >= 5
```

Isso significa:

- o perfil so e considerado valido quando o time possui pelo menos 5 partidas anteriores na temporada;
- partidas com um dos times sem historico minimo devem ser marcadas como nao elegiveis para segmentos completos;
- linhas nao elegiveis nao devem ser removidas silenciosamente;
- o dataset deve preservar flags de elegibilidade para auditoria.

Campos obrigatorios:

- `home_history_matches_available`
- `away_history_matches_available`
- `home_profile_eligible`
- `away_profile_eligible`
- `match_profile_eligible`

Regra:

```text
match_profile_eligible = home_history_matches_available >= 5 AND away_history_matches_available >= 5
```

---

## 5. Definicao dos Perfis

### 5.1 Perfil Ofensivo

O perfil ofensivo mede a forca historica de criacao/finalizacao de uma equipe antes da partida.

Metricas candidatas para o indice ofensivo:

- `goals_for_expanding_prior`
- `shots_for_expanding_prior`
- `shots_on_target_for_expanding_prior`
- `big_chances_for_expanding_prior`

Classificacoes oficiais:

#### `ofensivo_strong`

Time no tercil superior do indice ofensivo historico dinamico.

Interpretacao:

- equipe com historico recente/season-to-date acima da liga em producao ofensiva;
- candidata a gerar pressao ofensiva e gols tardios marcados.

#### `ofensivo_middle`

Time no tercil intermediario do indice ofensivo historico dinamico.

Interpretacao:

- perfil ofensivo neutro;
- usado como grupo de referencia intermediario.

#### `ofensivo_weak`

Time no tercil inferior do indice ofensivo historico dinamico.

Interpretacao:

- equipe com historico ofensivo abaixo da liga;
- pode servir como contraste ou grupo de descarte.

### 5.2 Perfil Defensivo

O perfil defensivo mede fragilidade historica defensiva antes da partida.

Metricas candidatas para o indice defensivo:

- `goals_against_expanding_prior`
- `shots_against_expanding_prior`
- `shots_on_target_against_expanding_prior`
- `big_chances_against_expanding_prior`

Classificacoes oficiais:

#### `defensivo_fragile`

Time no tercil superior do indice de fragilidade defensiva historica.

Interpretacao:

- equipe historicamente mais exposta defensivamente;
- achado exploratorio anterior indicou associacao consistente com gols tardios sofridos.

#### `defensivo_middle`

Time no tercil intermediario do indice de fragilidade defensiva historica.

Interpretacao:

- perfil defensivo neutro;
- usado como grupo intermediario.

#### `defensivo_strong`

Time no tercil inferior do indice de fragilidade defensiva historica.

Interpretacao:

- equipe historicamente menos exposta;
- defesa relativamente forte.

---

## 6. Definicao dos Confrontos

Os segmentos de confronto combinam o perfil ofensivo e defensivo dos dois times da partida.

Grain de confronto:

```text
1 linha por match_id
```

A definicao deve ser simetrica: quando aplicavel, tanto mandante quanto visitante podem satisfazer o papel ofensivo/defensivo do segmento.

### 6.1 `ofensivo_forte_vs_defesa_fragil`

Verdadeiro quando pelo menos um time ofensivamente forte enfrenta uma defesa fragil do adversario.

Formula conceitual:

```text
(home_ofensivo_strong AND away_defensivo_fragile)
OR
(away_ofensivo_strong AND home_defensivo_fragile)
```

Status metodologico: OBSERVAR / candidato relevante.

### 6.2 `ambos_defesa_forte`

Verdadeiro quando os dois times possuem perfil defensivo forte.

Formula conceitual:

```text
home_defensivo_strong AND away_defensivo_strong
```

Status metodologico: PROMISSOR exploratorio no cutoff 60, mas exige revisao Quant por ser contraintuitivo.

### 6.3 `defesa_fragil_vs_defesa_fragil`

Verdadeiro quando os dois times possuem defesa fragil.

Formula conceitual:

```text
home_defensivo_fragile AND away_defensivo_fragile
```

Status metodologico: avaliado, mas nao promissor na exploracao inicial.

### 6.4 `ofensivo_forte_vs_ofensivo_forte`

Verdadeiro quando os dois times possuem perfil ofensivo forte.

Formula conceitual:

```text
home_ofensivo_strong AND away_ofensivo_strong
```

Status metodologico: observar apenas se aprovado pelo Quant, pois amostra inicial foi limitada.

### 6.5 `ofensivo_fraco_vs_defesa_forte`

Verdadeiro quando um time ofensivamente fraco enfrenta uma defesa forte.

Formula conceitual:

```text
(home_ofensivo_weak AND away_defensivo_strong)
OR
(away_ofensivo_weak AND home_defensivo_strong)
```

Status metodologico: grupo de contraste.

### 6.6 Demais Grupos Aprovados para Auditoria

Os grupos abaixo podem ser gerados para auditoria e validacao estatistica, desde que fiquem separados da whitelist final de features modelaveis ate aprovacao Quant:

- `ao_menos_um_ofensivo_forte`
- `ao_menos_uma_defesa_fragil`
- `sem_ofensivo_forte_sem_defesa_fragil`
- `home_ofensivo_strong`
- `away_ofensivo_strong`
- `home_defensivo_fragile`
- `away_defensivo_fragile`

Esses grupos ajudam a separar efeito direcional, efeito simetrico e efeito de presenca de perfil.

---

## 7. Whitelist de Features de Segmentacao

Whitelist inicial aprovada para geracao do builder V1:

### Perfil dos Times

- `home_offense_profile`
- `away_offense_profile`
- `home_defense_profile`
- `away_defense_profile`
- `home_offense_index_prior`
- `away_offense_index_prior`
- `home_defense_fragility_index_prior`
- `away_defense_fragility_index_prior`

### Flags de Perfil

- `home_ofensivo_strong`
- `home_ofensivo_middle`
- `home_ofensivo_weak`
- `away_ofensivo_strong`
- `away_ofensivo_middle`
- `away_ofensivo_weak`
- `home_defensivo_fragile`
- `home_defensivo_middle`
- `home_defensivo_strong`
- `away_defensivo_fragile`
- `away_defensivo_middle`
- `away_defensivo_strong`

### Segmentos de Confronto

- `ofensivo_forte_vs_defesa_fragil`
- `ambos_defesa_forte`
- `defesa_fragil_vs_defesa_fragil`
- `ofensivo_forte_vs_ofensivo_forte`
- `ofensivo_fraco_vs_defesa_forte`
- `ao_menos_um_ofensivo_forte`
- `ao_menos_uma_defesa_fragil`
- `sem_ofensivo_forte_sem_defesa_fragil`

### Campos Historicos Permitidos

Os campos abaixo podem ser exportados para auditoria e validacao, mas o uso como feature modelavel exige aprovacao explicita:

- `home_goals_for_expanding_prior`
- `away_goals_for_expanding_prior`
- `home_goals_against_expanding_prior`
- `away_goals_against_expanding_prior`
- `home_shots_for_expanding_prior`
- `away_shots_for_expanding_prior`
- `home_shots_against_expanding_prior`
- `away_shots_against_expanding_prior`
- `home_shots_on_target_for_expanding_prior`
- `away_shots_on_target_for_expanding_prior`
- `home_shots_on_target_against_expanding_prior`
- `away_shots_on_target_against_expanding_prior`
- `home_big_chances_for_expanding_prior`
- `away_big_chances_for_expanding_prior`
- `home_big_chances_against_expanding_prior`
- `away_big_chances_against_expanding_prior`

Whitelist prevalece sobre blacklist. Apenas colunas explicitamente aprovadas podem entrar em X de qualquer experimento futuro.

---

## 8. Campos de Auditoria

O builder deve gerar campos que permitam auditar a ausencia de leakage e a qualidade dos perfis.

Campos obrigatorios:

- `match_id`
- `sofascore_event_id`
- `season`
- `match_date`
- `home_team`
- `away_team`
- `home_history_matches_available`
- `away_history_matches_available`
- `home_profile_eligible`
- `away_profile_eligible`
- `match_profile_eligible`
- `home_profile_max_match_date_used`
- `away_profile_max_match_date_used`
- `home_profile_source_match_count`
- `away_profile_source_match_count`
- `profile_min_games_rule`
- `profile_method`
- `profile_threshold_method`
- `builder_version`
- `generated_at`

Campos recomendados:

- `home_profile_source_match_ids`
- `away_profile_source_match_ids`
- `home_offense_threshold_low`
- `home_offense_threshold_high`
- `away_offense_threshold_low`
- `away_offense_threshold_high`
- `home_defense_threshold_low`
- `home_defense_threshold_high`
- `away_defense_threshold_low`
- `away_defense_threshold_high`

Se listas de match_ids deixarem o CSV pesado, elas podem ficar apenas no metadata ou em arquivo de auditoria separado.

---

## 9. Regras Anti-Leakage

Regras obrigatorias:

1. Aplicar `shift(1)` antes de qualquer media rolling/expanding.
2. Nunca usar estatisticas da propria partida para gerar perfil da propria partida.
3. Nunca usar partidas futuras.
4. Nunca usar target ou colunas derivadas do target.
5. Nunca usar `target_late_goal_75`, `home_late_goal_count_75`, `away_late_goal_count_75` ou equivalentes como entrada de perfil.
6. Nunca usar incidentes da propria partida como feature pre-jogo.
7. Nunca usar H8 in-game, graph, shotmap ou momentum neste builder de perfil pre-jogo.
8. Nunca usar odds, forecast pos-kickoff ou xG/xGA final da propria partida.
9. Thresholds de classificacao devem ser calculados com informacao historicamente disponivel, sem olhar target futuro.
10. O validation report deve falhar se `profile_max_match_date_used >= match_date` quando a comparacao temporal for confiavel.

Regra de auditoria final:

O builder deve listar:

- colunas usadas para calcular perfis;
- colunas exportadas;
- colunas proibidas removidas;
- motivo da remocao quando aplicavel;
- status anti-leakage final.

---

## 10. Grain Esperado

O grain principal esperado do dataset de features e:

```text
1 linha por match_id
```

Cada linha representa uma partida e contem:

- identificacao da partida;
- perfis do mandante;
- perfis do visitante;
- flags de segmentos de confronto;
- campos de auditoria.

Um dataset auxiliar opcional pode ter grain:

```text
1 linha por match_id + team_name
```

Esse dataset auxiliar serve apenas para auditoria dos perfis individuais e nao deve ser usado diretamente em baseline sem especificacao propria.

---

## 11. Dataset Esperado

Nome sugerido para implementacao futura:

```text
data/processed/features/team_profile_segments_v1.csv
data/processed/features/team_profile_segments_v1.parquet
data/processed/features/team_profile_segments_v1_metadata.json
data/processed/features/team_profile_segments_v1_validation_report.json
```

Conteudo esperado:

- 380 partidas como universo base, se usando EPL 2024/25 importavel atual;
- partidas inelegiveis preservadas com flags, nao removidas silenciosamente;
- `match_profile_eligible = true` apenas quando ambos os times possuem historico minimo;
- sem target anexado por padrao;
- sem dados pos-kickoff como features.

O target deve ser anexado apenas em dataset de validacao ou baseline futuro explicitamente aprovado.

---

## 12. Validation Report Esperado

O validation report deve conter, no minimo:

### Cobertura

- total de partidas;
- total de partidas elegiveis;
- total de partidas inelegiveis;
- distribuicao de `history_matches_available` por mandante e visitante;
- distribuicao de perfis ofensivos;
- distribuicao de perfis defensivos;
- distribuicao de segmentos.

### Integridade

- duplicatas por `match_id`;
- nulos em chaves obrigatorias;
- nulos em perfis;
- segmentos com N muito baixo;
- consistencia entre flags e categorias textuais.

### Anti-Leakage

- validacao de `shift(1)`;
- maximo `profile_max_match_date_used` por partida;
- contagem de violacoes temporais;
- confirmacao de que target-derived columns nao foram usadas;
- confirmacao de que estatisticas da propria partida nao entraram no proprio perfil.

### Status Final

Status possiveis:

- `APTO`
- `APTO COM RESSALVAS`
- `NAO APTO`

Regras sugeridas:

- `APTO`: sem violacoes anti-leakage, sem duplicatas, cobertura coerente.
- `APTO COM RESSALVAS`: sem leakage, mas com amostra limitada, nulos parciais ou segmentos pequenos.
- `NAO APTO`: qualquer violacao anti-leakage, duplicidade de grain ou perda silenciosa de partidas.

---

## 13. Criterios de Aceite

A implementacao futura so deve ser aceita se:

1. Gerar dataset com grain `1 linha por match_id`.
2. Preservar 380 partidas da base importavel atual, salvo justificativa documentada.
3. Marcar inelegibilidade por `min_games < 5` sem apagar linhas silenciosamente.
4. Aplicar `shift(1)` antes de rolling/expanding.
5. Confirmar que rodada R usa apenas jogos anteriores a rodada R.
6. Exportar metadata JSON.
7. Exportar validation report JSON.
8. Incluir campos de auditoria temporal.
9. Incluir whitelist de features geradas.
10. Nao anexar target por padrao.
11. Nao criar modelo.
12. Nao executar baseline.
13. Nao alterar PostgreSQL, schema, importer, crawler ou raw data.
14. Status final do validation report deve ser `APTO` ou `APTO COM RESSALVAS` para seguir a validacao estatistica.

---

## 14. Limitacoes Metodologicas

- A base atual cobre apenas uma temporada EPL, o que limita robustez de perfis no inicio da temporada.
- `min_games >= 5` reduz a amostra elegivel.
- Segmentos baseados em tercis podem ser instaveis em janelas pequenas.
- Alguns achados exploratorios podem ser contraintuitivos e exigir revisao Quant antes de virar feature modelavel.
- Nao ha correcao automatica para multiplos testes nesta especificacao.
- A classificacao por tercis depende da distribuicao historica disponivel e pode variar conforme a liga/temporada.
- Horarios de kickoff incompletos podem limitar a auditoria fina dentro da mesma data.
- O builder nao substitui validacao estatistica, baseline temporal ou revisao PM/Quant.

---

## 15. Proximas Etapas Autorizadas

Autorizado apos aprovacao desta especificacao:

1. Implementar `Team Profile Segment Feature Builder V1` como script isolado.
2. Gerar features de segmentacao com whitelist explicita.
3. Gerar metadata e validation report.
4. Executar validacao anti-leakage automatica.
5. Submeter outputs ao Quant Research para validacao estatistica.

Nao autorizado por este documento:

- criar modelo;
- executar baseline;
- executar backtesting;
- iniciar producao;
- alterar target;
- alterar schema;
- alterar importer;
- alterar crawler;
- alterar dados brutos;
- combinar essas features com H3/H4/H6/H8/H9 em modelo sem aprovacao explicita.

---

## Status Final

Documento metodologico completo e auditavel.

Status: PRONTO PARA REVISAO PM / QUANT RESEARCH.
