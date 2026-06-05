# SofaScore Endpoint Discovery - 2026-06-05

## Objetivo

Registrar a investigacao controlada de endpoints SofaScore alem de `graph`, usando apenas uma partida ja coletada da Premier League, para avaliar se existem fontes adicionais de dados temporais/minuto a minuto para H8.

Este documento nao autoriza importer, schema, feature engineering, dataset, baseline ou modelagem.

## Escopo executado

- Fonte: SofaScore API v1.
- Partida usada: `12436870`.
- Jogo: Manchester United x Fulham.
- Competicao: Premier League 2024/25.
- Criterio da partida: ja possuia `event.json`, `incidents.json`, `statistics.json` e `graph.json` localmente.
- Execucao: discovery controlado, lista pequena e explicita de endpoints.
- Sem brute force, sem paralelismo, sem rotacao de IP e sem bypass agressivo.

Artefatos locais:

```text
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\
```

Arquivos gerados localmente:

- `request_log.jsonl`
- `summary.md`
- `responses/*.json`
- `errors/*.json`

## Endpoints uteis confirmados

| Endpoint | Status | Utilidade |
|---|---:|---|
| `/graph` | 200 | Serie temporal de momentum/pressao, com `graphPoints`. |
| `/shotmap` | 200 | Finalizacoes com minuto, acrescimo, `timeSeconds`, xG, xGOT e coordenadas. |
| `/statistics` | 200 | Estatisticas agregadas por `ALL`, `1ST` e `2ND`. Nao e minuto a minuto. |
| `/incidents` | 200 | Eventos com minuto: gols, substituicoes, periodos, etc. |
| `/lineups` | 200 | Escalacoes, formacoes e contexto pre/in-game. |
| `/average-positions` | 200 | Posicoes medias por jogador e substituicoes. Agregado, nao serie temporal. |
| `/votes` | 200 | Votos/enquetes de usuarios. Baixo valor para modelagem. |
| `/best-players` | 200 | Melhores jogadores pos-jogo. Alto risco de leakage. |
| `/managers` | 200 | Tecnicos. Contexto, baixo valor para H8. |

## Endpoints 404 no padrao testado

| Endpoint | Resultado |
|---|---|
| `/statistics/overall` | 404 |
| `/statistics/period/1` | 404 |
| `/statistics/period/2` | 404 |
| `/lineups/confirmed` | 404 |
| `/player-statistics` | 404 |
| `/players/statistics` | 404 |
| `/heatmap` | 404 |
| `/momentum` | 404 |
| `/attack-momentum` | 404 |
| `/win-probability` | 404 |
| `/details` | 404 |
| `/shotmap/period/1` | 404 |
| `/shotmap/period/2` | 404 |
| `/shotmap/overall` | 404 |
| `/statistics/1` | 404 |
| `/statistics/2` | 404 |
| `/match-statistics` | 404 |
| `/timeline` | 404 |

## Endpoints de pressao/ataques investigados

Durante a segunda rodada, o endpoint abaixo retornou HTTP 403 dentro do script e a execucao foi interrompida conforme regra operacional:

```text
https://www.sofascore.com/api/v1/event/12436870/attacks
```

Links testados manualmente pelo usuario:

```text
https://www.sofascore.com/api/v1/event/12436870/attacks
https://www.sofascore.com/api/v1/event/12436870/dangerous-attacks
https://www.sofascore.com/api/v1/event/12436870/possession
https://www.sofascore.com/api/v1/event/12436870/field-tilt
https://www.sofascore.com/api/v1/event/12436870/pressure
```

Evolucao observada:

1. Durante a sessao de discovery, `attacks` retornou HTTP 403.
2. O usuario tambem observou HTTP 403 ao acessar endpoints relacionados e, em seguida, o site SofaScore passou a retornar 403 de forma geral na conexao.
3. Apos reiniciar o notebook e reconectar o 5G, os links voltaram a responder HTTP 404.

Interpretacao operacional:

- O HTTP 403 pareceu estar associado a bloqueio temporario de sessao/IP/conexao apos sequencia de testes.
- Apos reset de ambiente/rede, os mesmos endpoints passaram a 404, indicando que provavelmente nao existem como endpoints publicos simples nesse padrao.
- Nao ha evidencia segura de endpoint publico operacional para `attacks`, `dangerous-attacks`, `possession`, `field-tilt` ou `pressure` nesse formato.

## Diferenca entre 403 e 404 nesta investigacao

- 404: endpoint provavelmente inexistente nesse padrao para o evento testado.
- 403: bloqueio temporario, rota protegida ou rejeicao da sessao/IP. Nao deve ser contornado agressivamente.

Apos reconexao, os endpoints de ataques/pressao retornaram 404. Portanto, para a documentacao atual, eles devem ser tratados como **nao confirmados / nao operacionais**.

## Dados relevantes para H8

O conjunto util para H8 permanece:

```text
graph + shotmap + incidents + statistics
```

Complementos contextuais:

```text
lineups + average-positions + managers
```

Baixo valor ou risco de leakage:

```text
votes + best-players
```

## Lacunas ainda existentes

Nao foram encontrados endpoints publicos simples para:

- ataques perigosos minuto a minuto;
- posse minuto a minuto;
- field tilt minuto a minuto;
- pressao ofensiva direta;
- heatmap temporal;
- timeline adicional rica;
- estatisticas de jogador por endpoint direto.

Essas dimensoes devem ser inferidas, se necessario, a partir de:

- `graph` para pressao/momentum;
- `shotmap` para finalizacoes, xG/xGOT e coordenadas;
- `incidents` para eventos discretos;
- `statistics` para contexto agregado por tempo.

## Decisao operacional

Status: DISCOVERY PAUSADO.

Motivos:

- A lista controlada ja identificou os endpoints publicos simples mais uteis.
- As tentativas focadas em ataques/pressao causaram ou coincidiram com bloqueio 403 temporario.
- Apos reconexao, os endpoints de ataques/pressao retornaram 404.
- Continuar tentando variacoes aumentaria risco operacional e se aproximaria de brute force, o que esta fora do escopo.

## Recomendacao

- Nao insistir em `attacks`, `dangerous-attacks`, `possession`, `field-tilt` e `pressure` no formato testado.
- Usar `graph`, `shotmap`, `incidents` e `statistics` como base candidata para H8.
- Se houver nova investigacao, ela deve ser feita via inspecao controlada de chamadas reais da pagina no navegador, nao por tentativa de nomes de endpoints.
- Nao usar bypass agressivo, rotacao de IP ou automacao paralela.

## Restricoes respeitadas

- Nenhum banco foi alterado.
- Nenhum schema foi alterado.
- Nenhum importer foi criado ou alterado.
- Nenhum dataset foi criado.
- Nenhuma feature foi criada.
- Nenhum baseline foi executado.
- Nenhuma modelagem foi feita.
- Nenhum coletor SofaScore v2/v3/graph foi alterado para coleta massiva.
- Nenhum dado bruto existente valido foi sobrescrito.
