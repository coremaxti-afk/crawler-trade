# Lessons Learned – LateGoalResearch

## Objetivo

Este documento registra os principais obstáculos encontrados durante a construção do projeto LateGoalResearch e as soluções adotadas.

---

# 1. Dependência do Endpoint FotMob Antigo

## Problema

O Match Mapper original utilizava:

https://www.fotmob.com/api/matches?date=YYYYMMDD

Durante os testes o endpoint passou a retornar:

HTTP 404

Impossibilitando a descoberta de partidas por data.

## Tentativas

* HTTP direto
* Playwright
* Reprodução da abordagem do worldfootballR

Todas falharam.

## Solução

Descobrimos que o endpoint:

https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025

continua ativo e contém:

* leagueOverviewMatches
* home team
* away team
* utcTime
* fotmob_match_id

O Match Mapper passou a utilizar esse endpoint.

## Status

Resolvido.

---

# 2. Dependência do Cache worldfootballR

## Problema

O Match Mapper desenvolvido inicialmente dependia do arquivo:

47_matches_by_date.rds

Utilizado pelo projeto worldfootballR.

O arquivo não estava presente no repositório.

## Impacto

Impossibilidade de reproduzir os testes realizados anteriormente.

## Solução

Abandonamos a dependência do cache externo.

A obtenção dos fotmob_match_id passou a ser feita diretamente pela API:

/api/data/leagues

## Status

Resolvido.

---

# 3. Problema com psycopg

## Problema

O script fotmob_match_mapper.py exibia:

"psycopg is not installed"

mesmo após instalação do pacote.

## Diagnóstico

O pacote estava instalado, porém sem backend funcional.

Erro encontrado:

ImportError: no pq wrapper available

## Solução

Instalação:

pip install "psycopg[binary]"

## Status

Resolvido.

---

# 4. Descoberta do Endpoint League API

## Problema

Não existia forma confiável de obter fotmob_match_id.

## Investigação

Utilização do DevTools do navegador.

Análise das chamadas realizadas pela página da Premier League.

## Descoberta

Endpoint:

https://www.fotmob.com/api/data/leagues?id=47

Suporte a temporada:

https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025

## Resultado

Acesso aos 380 jogos da EPL 2024/25.

## Status

Resolvido.

---

# 5. Matching Understat ↔ FotMob

## Problema

Os nomes dos times não são idênticos.

Exemplos:

* Manchester United → Man United
* Manchester City → Man City
* Wolverhampton Wanderers → Wolves
* Newcastle United → Newcastle

## Solução

Criação de tabela de aliases.

## Resultado

369 partidas encontradas em 380.

Cobertura:

97,1%

## Status

Parcialmente resolvido.

11 partidas remarcadas ainda precisam de tratamento específico.

---

# 6. Estratégia de Segurança para Atualizações

## Problema

Risco de atualizar o banco incorretamente.

## Solução

Implementação de:

DRY_RUN = True

Antes de qualquer UPDATE.

## Benefício

Validação completa do matching antes da gravação.

## Status

Adotado como padrão do projeto.

---

# 7. Armazenamento de Dados FotMob

## Problema

Dependência futura da API.

## Decisão

Criar armazenamento local dos JSONs retornados pelo endpoint:

/api/data/matchDetails

## Objetivo

Construir um cache permanente para análises futuras.

## Status

Planejado.

---

# Estado Atual do Projeto

Concluído:

* Importação Understat
* Banco PostgreSQL
* Events V2
* Snapshot Builder
* Momentum
* Touches Box
* Match Mapper
* FotMob Match IDs

Cobertura atual:

* 380 partidas Understat
* 369 partidas com fotmob_match_id

Próximo Marco:

Batch MatchDetails Capture.
