# MATCH MAPPER - Understat x FotMob

## Objetivo

Descobrir `fotmob_match_id` a partir de:

- `home_team`
- `away_team`
- `match_date`

sem alterar scripts ja validados e sem alterar schema de banco.

## Script

Arquivo:

- `fotmob/fotmob_match_mapper.py`

Uso para partida unica:

```bash
python fotmob/fotmob_match_mapper.py --home "Manchester United" --away Fulham --date 2024-08-16
```

Uso com cache CSV/RDS:

```bash
python fotmob/fotmob_match_mapper.py --cache-file 47_matches_by_date.rds --home "Manchester United" --away Fulham --date 2024-08-16
```

Uso com CSV:

```bash
python fotmob/fotmob_match_mapper.py --input-csv matches.csv --output-csv mapped.csv
```

Uso opcional com banco:

```bash
python fotmob/fotmob_match_mapper.py --from-db --database-url postgresql://user:pass@host:5432/late_goal_research
```

Para gravar no banco, usar explicitamente:

```bash
python fotmob/fotmob_match_mapper.py --from-db --database-url postgresql://user:pass@host:5432/late_goal_research --update-db
```

## Metodo principal investigado

Endpoint historicamente usado por bibliotecas publicas:

```text
https://www.fotmob.com/api/matches?date=YYYYMMDD
```

Estrutura esperada:

```text
leagues[].matches[]
```

Campos usados:

- `match_id` ou `id`
- `home.name`
- `away.name`
- `status.utcTime`
- nome da liga

O mapper normaliza nomes de times, aplica aliases conhecidos da EPL e calcula similaridade entre os nomes Understat e FotMob. O criterio padrao aceita match com confianca minima `0.92`.

## Limitacao encontrada

Em 2026-06-02, a chamada direta ao endpoint `api/matches` retornou HTML/404 no ambiente testado, inclusive via Playwright headless.

Por isso, o script suporta dois caminhos:

1. Endpoint FotMob ao vivo (`--transport auto`, `direct` ou `playwright`).
2. Cache local CSV/RDS com campos `date`, `home_name`, `away_name`, `match_id`.

O cache RDS publico `worldfootballR_data` da Premier League foi usado para validacao historica.

## Validacao manual

Fonte da validacao:

- Cache `worldfootballR_data` para Premier League, liga FotMob `47`.

Periodo:

- Rodada inicial da EPL 2024/25.

Resultado:

- 10 partidas testadas
- 10 partidas mapeadas
- Taxa de sucesso: 100%
- Confianca media: 1.0

| Data | Understat home | Understat away | FotMob home | FotMob away | fotmob_match_id | Confianca |
| --- | --- | --- | --- | --- | ---: | ---: |
| 2024-08-16 | Manchester United | Fulham | Man United | Fulham | 4506263 | 1.0 |
| 2024-08-17 | Ipswich Town | Liverpool | Ipswich | Liverpool | 4506264 | 1.0 |
| 2024-08-17 | Arsenal | Wolverhampton Wanderers | Arsenal | Wolves | 4506265 | 1.0 |
| 2024-08-17 | Everton | Brighton and Hove Albion | Everton | Brighton | 4506266 | 1.0 |
| 2024-08-17 | Newcastle United | Southampton | Newcastle | Southampton | 4506267 | 1.0 |
| 2024-08-17 | Nottingham Forest | AFC Bournemouth | Nottm Forest | Bournemouth | 4506268 | 1.0 |
| 2024-08-17 | West Ham United | Aston Villa | West Ham | Aston Villa | 4506269 | 1.0 |
| 2024-08-18 | Brentford | Crystal Palace | Brentford | Crystal Palace | 4506270 | 1.0 |
| 2024-08-18 | Chelsea | Manchester City | Chelsea | Man City | 4506271 | 1.0 |
| 2024-08-19 | Leicester City | Tottenham Hotspur | Leicester | Tottenham | 4506272 | 1.0 |

## Recomendacao operacional

Para batch historico da EPL 2024/25, usar `--cache-file` com cache FotMob confiavel quando disponivel. Para partidas novas, tentar `--transport auto`; se o endpoint continuar bloqueado, gerar ou atualizar cache via processo Playwright ja validado no projeto.
