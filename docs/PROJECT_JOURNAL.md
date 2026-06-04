# PROJECT JOURNAL – FOTMOB INTEGRATION

## Objetivo

Enriquecer a base Understat com dados do FotMob para pesquisa de gols tardios, momentum, eventos e snapshots de partidas.

---

# Conquistas

## 1. Estruturação da Base

Tabela `matches` criada e populada.

Campos relevantes:

* understat_match_id
* match_date
* home_team
* away_team
* home_goals
* away_goals
* home_xg
* away_xg

---

## 2. Integração FotMob

Adicionado campo:

```sql
fotmob_match_id BIGINT
```

Criado índice:

```sql
idx_matches_fotmob
```

Resultado:

* 369 partidas mapeadas com sucesso
* 11 partidas não mapeadas inicialmente

---

## 3. Descoberta do Endpoint de Liga

Endpoint funcional:

https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025

Informações disponíveis:

* fixtures
* tabela
* estatísticas
* leagueOverviewMatches
* ids das partidas

Resultado:

Mapeamento completo da Premier League 2024/2025.

---

## 4. Match Mapping

Objetivo:

Relacionar:

Understat Match
↓
FotMob Match ID

Resultado:

369 partidas associadas com sucesso.

Considerado concluído.

---

# Desafios Encontrados

## Desafio 1

Endpoint antigo:

https://www.fotmob.com/api/matches

Problema:

Retornando HTML ou 404.

Solução:

Migrar para:

https://www.fotmob.com/api/data/leagues

Status:

Resolvido.

---

## Desafio 2

Biblioteca psycopg instalada porém não funcional.

Erro:

libpq library not found

Solução:

Instalação do pacote:

psycopg[binary]

Status:

Resolvido.

---

## Desafio 3

Mapeamento de nomes de equipes.

Exemplos:

* Man United
* Manchester United
* Man Utd

Solução:

Criação de aliases.

Status:

Resolvido.

---

## Desafio 4

Captura automática do endpoint matchDetails.

Endpoint:

https://www.fotmob.com/api/data/matchDetails

Problema:

Retorno:

403
TURNSTILE_REQUIRED

Status:

Não resolvido.

---

## Desafio 5

Playwright interceptando matchDetails.

Resultado observado:

URL encontrada:

matchDetails?matchId=4506263

Porém resposta:

403

Status:

Não resolvido.

---

## Desafio 6

Diferença entre captura histórica e captura atual.

Evidência:

Arquivo matchdetails.json foi gerado anteriormente.

Contém:

* momentum
* playerStats
* events
* shotmap
* attackingZones

Problema:

Método atualmente não reproduzível.

Status:

Investigação em aberto.

---

# Hipóteses Investigadas

## Hipótese: Header x-mas

Resultado:

Não suficiente.

Continua retornando 403.

---

## Hipótese: Playwright

Resultado:

URL detectada.

Payload bloqueado.

---

## Hipótese: Cache Local

Evidência:

DevTools mostrou:

200 OK (from disk cache)

Possível explicação para sucesso anterior.

Status:

Provável.

---

# Decisão Arquitetural

Não bloquear o projeto por causa do FotMob MatchDetails.

Prioridade:

1. Consolidar banco histórico.
2. Construir modelos quantitativos.
3. Investigar snapshots paralelamente.

---

# Plano A

Continuar tentando reproduzir:

matchDetails
↓
fotmob_raw_matches

Automação completa.

---

# Plano B

Captura manual.

Fluxo:

1. Abrir endpoint da liga.
2. Salvar JSON.
3. Processar localmente.

Uso apenas para casos específicos.

---

# Próximas Etapas

## Curto Prazo

* Consolidar temporadas EPL 21/22 até 25/26.
* Expandir para outras ligas.
* Consolidar odds históricas.
* Construir primeiro modelo de gols tardios.

## Médio Prazo

Pesquisar fontes alternativas:

* SofaScore
* Flashscore
* FBref
* StatsBomb Open Data
* SoccerNet

## Longo Prazo

Substituir dependência exclusiva do FotMob por múltiplas fontes de snapshots.
