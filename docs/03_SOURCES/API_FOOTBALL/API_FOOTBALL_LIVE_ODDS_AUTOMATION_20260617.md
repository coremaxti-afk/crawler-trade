# API_FOOTBALL_LIVE_ODDS_AUTOMATION_20260617

## Status

Decisao: **APROVADO COMO REFERENCIA OPERACIONAL DA COLETA AO VIVO API-FOOTBALL**

Objetivo: registrar a arquitetura de coleta ao vivo da API-Football para jogos da Copa do Mundo 2026, com foco em live odds e automacao de disparo do coletor.

## Escopo

A frente cobre:

- live odds durante a partida;
- mercados de 1x2;
- mercados de gols;
- mercados de escanteios;
- mercados de cartoes;
- contexto live de fixture, eventos e estatisticas;
- automacao que agenda e dispara coletas por fixture.

Fora do escopo desta versao:

- backtesting financeiro real;
- garantia de cobertura por bookmaker especifico;
- coleta simultanea multi-fixture dentro de um unico processo;
- reconstruir live odds depois do fim da partida.

## Conclusao principal

A API-Football entrega `odds/live` durante o jogo, mas nao preserva historico completo depois do fim da partida.

Logo:

```text
live odds precisam ser coletadas durante a partida
```

Depois do `FT`, o endpoint pode retornar vazio.

## Validacoes praticas realizadas

### Iraq vs Norway

Fixture:

```text
1539016
```

Resultado:

- teste positivo forte durante o jogo;
- `live_odds` retornou mercados como `Over/Under Line`, `Match Goals`, `Home Team Goals`, `Away Team Goals` e `Next 10 Minutes Total`.

Conclusao:

```text
odds/live funciona quando a coleta ocorre durante o jogo
```

### France vs Senegal

Fixture:

```text
1489383
```

Resultado:

- teste pos-jogo;
- depois do `FT`, `live_odds.json` veio vazio.

Conclusao:

```text
nao confiar em coleta pos-jogo para recuperar live odds
```

### Fortaleza EC vs America Mineiro

Fixture:

```text
1520725
```

Resultado:

- havia live odds perto do fim;
- mercado disponivel estava reduzido.

Conclusao:

```text
cobertura live varia por competicao, momento do jogo e mercado
```

## Pontos relevantes da documentacao oficial

### odds/live

Pontos registrados:

- atualizacao teorica a cada 5 segundos;
- na pratica pode variar ate 60 segundos;
- fixtures entram entre 15 e 5 minutos antes do inicio;
- fixtures saem entre 5 e 20 minutos depois do fim;
- nao ha armazenamento historico garantido.

Filtros documentados:

- `fixture`
- `league`
- `bet`

Limite importante:

```text
odds/live nao documenta filtro oficial por bookmaker
```

Portanto, a V2 nao consegue garantir apenas Bet365, Betfair Exchange ou Betfair Sportsbook por parametro oficial. O coletor foca nos mercados corretos.

### odds/live/bets

Uso:

- retornar catalogo de `bet ids` compativeis com `odds/live`;
- permitir que a V2 descubra quais mercados pode consultar via filtro `bet`.

### fixtures e fixtures/events

Atualizacao tipica:

```text
15 segundos
```

### fixtures/statistics

Atualizacao tipica:

```text
1 minuto
```

## Status relevantes

### Em jogo

```text
1H
HT
2H
ET
BT
P
SUSP
INT
LIVE
```

### Finalizados ou encerrados

```text
FT
AET
PEN
CANC
ABD
AWD
WO
```

## Scripts oficiais desta frente

### Lista da fase de grupos

Script:

```text
C:\LateGoalResearch\Crawler\ApiFootball\api_football_world_cup_group_stage_fixtures_v1.py
```

Tutorial:

```text
C:\LateGoalResearch\docs\03_SOURCES\API_FOOTBALL\API_FOOTBALL_WORLD_CUP_GROUP_STAGE_FIXTURES_V1.md
```

Saidas:

```text
C:\LateGoalResearch\data\raw\api_football\world_cup_group_stage\league_1_season_2026\world_cup_group_stage_fixtures.csv
C:\LateGoalResearch\data\raw\api_football\world_cup_group_stage\league_1_season_2026\world_cup_group_stage_fixtures.json
```

### Coletor live V1

Script:

```text
C:\LateGoalResearch\Crawler\ApiFootball\api_football_live_match_collector_v1.py
```

Tutorial:

```text
C:\LateGoalResearch\docs\03_SOURCES\API_FOOTBALL\API_FOOTBALL_LIVE_MATCH_COLLECTOR_V1.md
```

Caracteristicas:

- uma fixture por execucao;
- coleta fixture;
- coleta fixture statistics;
- coleta fixture events;
- coleta live odds;
- opcionalmente coleta lineups, players, predictions e odds;
- encerra sozinha no `FT`.

### Coletor live V2

Script:

```text
C:\LateGoalResearch\Crawler\ApiFootball\api_football_live_match_collector_v2.py
```

Tutorial:

```text
C:\LateGoalResearch\docs\03_SOURCES\API_FOOTBALL\API_FOOTBALL_LIVE_MATCH_COLLECTOR_V2.md
```

Caracteristicas:

- uma fixture por processo;
- adiciona `fixtures?live=all` em cada ciclo;
- usa `odds/live/bets` para descobrir `bet ids`;
- adiciona retries e backoff;
- foca em mercados de 1x2, gols, escanteios e cartoes;
- nao garante filtro por bookmaker.

### Launcher da automacao

Script:

```text
C:\LateGoalResearch\scripts\api_football_world_cup_live_monitor_launcher.py
```

Funcao:

- ler a lista oficial da fase de grupos;
- identificar fixtures elegiveis;
- disparar o coletor live V2;
- registrar logs e processo;
- sugerir a proxima agenda.

## Sincronizacao GitHub

Documentacao publicada no GitHub:

- `docs/03_SOURCES/API_FOOTBALL/API_FOOTBALL_LIVE_ODDS_AUTOMATION_20260617.md`
- `docs/03_SOURCES/API_FOOTBALL/API_FOOTBALL_LIVE_MATCH_COLLECTOR_V2.md`
- `docs/03_SOURCES/API_FOOTBALL/API_FOOTBALL_WORLD_CUP_LIVE_MONITOR_LAUNCHER.md`

Pendencia de sincronizacao de codigo no GitHub:

- `Crawler/ApiFootball/api_football_world_cup_group_stage_fixtures_v1.py`
- `Crawler/ApiFootball/api_football_live_match_collector_v1.py`
- `Crawler/ApiFootball/api_football_live_match_collector_v2.py`
- `scripts/api_football_world_cup_live_monitor_launcher.py`

Motivo:

```text
os scripts existem localmente e sao referenciados pela documentacao, mas ainda nao estavam presentes no remoto no momento desta atualizacao
```

## Desenho aprovado da automacao

A automacao nao deve acompanhar o jogo.

Ela deve apenas:

1. ler a lista oficial da fase de grupos;
2. identificar a proxima fixture elegivel;
3. disparar o script live V2;
4. nao esperar o `FT`;
5. catalogar o proximo jogo;
6. encerrar;
7. voltar apenas no horario da proxima fixture.

Resumo:

```text
automacao agenda e dispara
script live V2 coleta sozinho ate FT
```

## Entrada oficial da automacao

Lista de fixtures:

```text
C:\LateGoalResearch\data\raw\api_football\world_cup_group_stage\league_1_season_2026\world_cup_group_stage_fixtures.csv
```

Coletor disparado:

```text
C:\LateGoalResearch\Crawler\ApiFootball\api_football_live_match_collector_v2.py
```

Output recomendado:

```text
C:\LateGoalResearch\data\raw\api_football\live_monitor_v2
```

Parametros recomendados:

```text
--poll-seconds 60
--capture-context
```

## Exemplo manual

```powershell
$env:API_FOOTBALL_KEY="SUA_CHAVE"
python C:\LateGoalResearch\Crawler\ApiFootball\api_football_live_match_collector_v2.py `
  --fixture-id 1489381 `
  --poll-seconds 60 `
  --capture-context `
  --output-root C:\LateGoalResearch\data\raw\api_football\live_monitor_v2
```

## Exemplo do launcher

Conferir sem iniciar processos:

```powershell
python C:\LateGoalResearch\scripts\api_football_world_cup_live_monitor_launcher.py --dry-run
```

Ver a proxima agenda:

```powershell
python C:\LateGoalResearch\scripts\api_football_world_cup_live_monitor_launcher.py --print-next-schedule
```

Rodar automacao de disparo:

```powershell
python C:\LateGoalResearch\scripts\api_football_world_cup_live_monitor_launcher.py
```

## Regras operacionais

- 1 script = 1 jogo.
- Jogos simultaneos exigem multiplas execucoes paralelas.
- Nao e obrigatorio coletar todos os jogos da Copa.
- Para uma liga com jogos simultaneos, usar um processo por fixture.
- Uma V3 multi-fixture pode ser criada no futuro, mas nao e requisito da arquitetura atual.

## Riscos e limites

### Live odds sao temporais

Como nao ha historico garantido:

```text
coleta atrasada pode perder mercados live
```

### Cobertura varia

Mesmo durante o jogo, mercados podem variar por:

- competicao;
- momento da partida;
- status da fixture;
- disponibilidade do provedor;
- bet id disponivel no catalogo live.

### Bookmaker nao e filtro oficial

Nomes como Bet365 e Betfair ficam como preferencia operacional, nao como garantia tecnica.

### Simultaneidade

O desenho atual evita complexidade em excesso:

```text
um processo por fixture
```

## Decisao operacional

Arquitetura recomendada para a proxima fase:

1. manter a lista oficial da Copa do Mundo 2026 atualizada;
2. usar o launcher apenas como disparador;
3. rodar o coletor live V2 por fixture;
4. salvar snapshots em `data/raw/api_football/live_monitor_v2`;
5. avaliar qualidade dos mercados depois da coleta;
6. so criar V3 multi-fixture se a operacao exigir muitos jogos simultaneos.

## Conclusao

A frente de coleta live API-Football esta tecnicamente validada para uso operacional controlado.

O ponto mais importante permanece:

```text
live odds devem ser coletadas durante a partida
```

O uso recomendado e combinar:

- lista oficial de fixtures;
- automacao que apenas dispara;
- coletor V2 que coleta ate o encerramento da fixture;
- analise posterior dos snapshots gerados.
