# COLLECTIONS

## Objetivo

Controlar e documentar todas as coletas realizadas pelo projeto.

---

## Fontes

### Understat

Status:
Ativo

Função:
Dados pré-jogo.

---

### SofaScore

Status:
Ativo

Função:
Dados in-game e eventos.

---

### FotMob

Status:
Bloqueado temporariamente

Função:
Fonte complementar para eventos.

---

## Regras

- Toda coleta deve ser reproduzível.
- Dados brutos devem ser preservados.
- Não sobrescrever dados sem versionamento.
- Toda falha operacional deve ser documentada.

---

# Premier League 2024/25

Season ID:
61627

Fonte:
SofaScore

Status:
Em andamento

---

## Artefatos Gerados

### Descoberta da Temporada

Gerados com sucesso:

- inventory.json
- rounds.json
- round_01_events.json
- ...
- round_38_events.json

---

## Estrutura da Temporada

premier_league_61627/

- inventory.json
- rounds.json
- round_01_events.json
- ...
- round_38_events.json

---

## Coleta por Partida

Estrutura:

matches/{event_id}/

- event.json
- statistics.json
- incidents.json
- lineups.json
- h2h.json

---

## Status Atual

Partidas coletadas:

50

Resultado:

Sucesso

---

## Limitação Encontrada

Após aproximadamente:

- 50 partidas
- 250 requisições

O SofaScore passou a retornar:

HTTP 403

Status:

Em investigação

---

## Hipóteses

- Rate Limiting
- Session Limiting
- IP Limiting

---

## Próximas Ações

1. Resolver bloqueio HTTP 403
2. Finalizar EPL
3. Implementar importação PostgreSQL
4. Construir features
5. Validar hipóteses H1-H9

---

## Ligas Planejadas

### Inglaterra

- Premier League
- Championship

### Espanha

- La Liga
- La Liga 2

### Alemanha

- Bundesliga
- Bundesliga 2

### Itália

- Serie A
- Serie B

### França

- Ligue 1
- Ligue 2

### Holanda

- Eredivisie

### Noruega

- Eliteserien

### Suécia

- Allsvenskan

### Suíça

- Super League

### Brasil

- Brasileirão Série A
- Brasileirão Série B

### Bélgica

- Pro League

### Estados Unidos

- MLS
