# API_FOOTBALL_WORLD_CUP_LIVE_MONITOR_LAUNCHER

## Objetivo

Documentar o launcher:

```text
C:\LateGoalResearch\scripts\api_football_world_cup_live_monitor_launcher.py
```

O launcher nao coleta o jogo diretamente. Ele apenas avalia fixtures elegiveis da Copa do Mundo 2026 e dispara o coletor live V2 quando uma partida deve ser monitorada.

## Arquitetura

```text
lista oficial de fixtures -> launcher -> coletor live V2 -> snapshots por fixture
```

Entrada padrao:

```text
C:\LateGoalResearch\data\raw\api_football\world_cup_group_stage\league_1_season_2026\world_cup_group_stage_fixtures.csv
```

Coletor padrao:

```text
C:\LateGoalResearch\Crawler\ApiFootball\api_football_live_match_collector_v2.py
```

Saida padrao:

```text
C:\LateGoalResearch\data\raw\api_football\live_monitor_v2
```

## Comandos

Conferir sem iniciar processos:

```powershell
python C:\LateGoalResearch\scripts\api_football_world_cup_live_monitor_launcher.py --dry-run
```

Mostrar proxima agenda:

```powershell
python C:\LateGoalResearch\scripts\api_football_world_cup_live_monitor_launcher.py --print-next-schedule
```

Executar:

```powershell
python C:\LateGoalResearch\scripts\api_football_world_cup_live_monitor_launcher.py
```

## Variaveis de API key

O launcher procura a chave em:

```text
API_FOOTBALL_KEY
APIFOOTBALL_API_KEY
API_SPORTS_KEY
```

Tambem tenta ler arquivos locais:

```text
C:\LateGoalResearch\.env
C:\LateGoalResearch\.env.local
C:\LateGoalResearch\config\.env
C:\LateGoalResearch\config\api_football.env
```

## Regras de elegibilidade

O launcher ignora:

- fixture sem `fixture_id`;
- fixture ja finalizada;
- fixture com coletor ja rodando;
- fixture futura com kickoff ainda nao alcancado;
- fixture com status nao suportado.

O launcher dispara:

- fixture com status live;
- fixture `NS` cujo kickoff ja foi alcancado.

## Status finalizados

```text
FT
AET
PEN
CANC
ABD
AWD
WO
```

## Status live

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

## Saidas do launcher

O launcher grava resumos em:

```text
data/raw/api_football/live_monitor_v2/_launcher_runs/
```

Cada fixture disparada tambem recebe:

```text
fixture_<fixture_id>/collector_process.json
fixture_<fixture_id>/collector_stdout.log
fixture_<fixture_id>/collector_stderr.log
```

## Decisao operacional

A automacao deve acordar no horario planejado, rodar o launcher e encerrar.

O coletor V2 continua trabalhando sozinho ate o encerramento da fixture.
