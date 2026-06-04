# BACKLOG

## STATUS ATUAL

### Concluído

* [x] Estruturar banco PostgreSQL
* [x] Importar dados históricos Understat
* [x] Criar tabela matches
* [x] Descobrir endpoint FotMob de ligas
* [x] Mapear Understat → FotMob
* [x] Adicionar fotmob_match_id
* [x] Popular 369 partidas EPL 2024/2025
* [x] Validar correspondência dos Match IDs
* [x] Investigar endpoint MatchDetails
* [x] Documentar limitações atuais do FotMob

---

## Alta Prioridade

### Expansão Histórica

* [ ] EPL 2021/2022
* [ ] EPL 2022/2023
* [ ] EPL 2023/2024
* [ ] EPL 2025/2026

---

### Expansão de Ligas

* [ ] La Liga
* [ ] Bundesliga
* [ ] Serie A
* [ ] Ligue 1
* [ ] Brasileirão

---

### Odds

* [ ] Avaliar fontes históricas
* [ ] Criar tabela de odds
* [ ] Vincular odds às partidas

---

## Média Prioridade

### Pesquisa de Snapshots

Avaliar:

* [ ] SofaScore
* [ ] Flashscore
* [ ] FBref
* [ ] StatsBomb Open Data
* [ ] SoccerNet
* [ ] AiScore

Objetivo:

Encontrar substitutos para o MatchDetails do FotMob.

---

### Padronização de Snapshot

Criar estrutura única contendo:

* minuto
* placar
* momentum
* ataques
* ataques perigosos
* xG acumulado
* estatísticas temporais

---

## Pesquisa Paralela

### FotMob MatchDetails

Status:

BLOCKED

Problema:

403 TURNSTILE_REQUIRED

Evidências:

* Endpoint identificado
* matchdetails.json histórico existe
* Captura não reproduzível atualmente

Decisão:

Não bloquear o projeto.

Continuar investigação em paralelo.
