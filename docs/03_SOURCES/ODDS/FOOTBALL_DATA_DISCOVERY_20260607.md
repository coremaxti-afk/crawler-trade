# Football-Data.co.uk Discovery - 20260607

## Escopo

Spike controlado da fonte Football-Data.co.uk para avaliar odds historicas gratuitas da Premier League 2024/25.

Esta tarefa e apenas Data Acquisition / discovery. Nao implementa importer, nao altera banco, nao altera schema, nao cria dataset analitico, nao cria features, nao modela e nao faz backtesting.

## CSV Utilizado

- URL: `https://www.football-data.co.uk/mmz4281/2425/E0.csv`
- Arquivo bruto local: `data/raw/football_data/england/premier_league_2024_2025/E0_2024_2025.csv`
- Data da execucao: 2026-06-07
- HTTP: 200

## Resumo Executivo

- Existe CSV da EPL 2024/25: **sim**.
- Total de linhas no arquivo: **380**.
- Total de partidas validas: **380**.
- Total de colunas: **120**.
- Total de colunas de odds inferidas: **96**.
- Possui Match Odds / 1X2: **sim**.
- Possui Over/Under 2.5: **sim**.
- Possui BTTS: **nao**.
- Possui Asian Handicap: **sim**.
- Possui colunas de opening/pre-close snapshot: **sim**.
- Possui colunas de closing snapshot: **sim**.
- Possui odds live/minuto a minuto: **nao**.
- Recomendacao final: **ALTO POTENCIAL**.

## Amostra de Partidas

| Date | Time | HomeTeam | AwayTeam | FTHG | FTAG | FTR |
|---|---|---|---|---:|---:|---|
| 16/08/2024 | 20:00 | Man United | Fulham | 1 | 0 | H |
| 17/08/2024 | 12:30 | Ipswich | Liverpool | 0 | 2 | A |
| 17/08/2024 | 15:00 | Arsenal | Wolves | 2 | 0 | H |
| 17/08/2024 | 15:00 | Everton | Brighton | 0 | 3 | A |
| 17/08/2024 | 15:00 | Newcastle | Southampton | 1 | 0 | H |

## Lista de Colunas

- `Div`
- `Date`
- `Time`
- `HomeTeam`
- `AwayTeam`
- `FTHG`
- `FTAG`
- `FTR`
- `HTHG`
- `HTAG`
- `HTR`
- `Referee`
- `HS`
- `AS`
- `HST`
- `AST`
- `HF`
- `AF`
- `HC`
- `AC`
- `HY`
- `AY`
- `HR`
- `AR`
- `B365H`
- `B365D`
- `B365A`
- `BWH`
- `BWD`
- `BWA`
- `BFH`
- `BFD`
- `BFA`
- `PSH`
- `PSD`
- `PSA`
- `WHH`
- `WHD`
- `WHA`
- `1XBH`
- `1XBD`
- `1XBA`
- `MaxH`
- `MaxD`
- `MaxA`
- `AvgH`
- `AvgD`
- `AvgA`
- `BFEH`
- `BFED`
- `BFEA`
- `B365>2.5`
- `B365<2.5`
- `P>2.5`
- `P<2.5`
- `Max>2.5`
- `Max<2.5`
- `Avg>2.5`
- `Avg<2.5`
- `BFE>2.5`
- `BFE<2.5`
- `AHh`
- `B365AHH`
- `B365AHA`
- `PAHH`
- `PAHA`
- `MaxAHH`
- `MaxAHA`
- `AvgAHH`
- `AvgAHA`
- `BFEAHH`
- `BFEAHA`
- `B365CH`
- `B365CD`
- `B365CA`
- `BWCH`
- `BWCD`
- `BWCA`
- `BFCH`
- `BFCD`
- `BFCA`
- `PSCH`
- `PSCD`
- `PSCA`
- `WHCH`
- `WHCD`
- `WHCA`
- `1XBCH`
- `1XBCD`
- `1XBCA`
- `MaxCH`
- `MaxCD`
- `MaxCA`
- `AvgCH`
- `AvgCD`
- `AvgCA`
- `BFECH`
- `BFECD`
- `BFECA`
- `B365C>2.5`
- `B365C<2.5`
- `PC>2.5`
- `PC<2.5`
- `MaxC>2.5`
- `MaxC<2.5`
- `AvgC>2.5`
- `AvgC<2.5`
- `BFEC>2.5`
- `BFEC<2.5`
- `AHCh`
- `B365CAHH`
- `B365CAHA`
- `PCAHH`
- `PCAHA`
- `MaxCAHH`
- `MaxCAHA`
- `AvgCAHH`
- `AvgCAHA`
- `BFECAHH`
- `BFECAHA`

## Colunas de Odds Encontradas

- `B365H`
- `B365D`
- `B365A`
- `BWH`
- `BWD`
- `BWA`
- `BFH`
- `BFD`
- `BFA`
- `PSH`
- `PSD`
- `PSA`
- `WHH`
- `WHD`
- `WHA`
- `1XBH`
- `1XBD`
- `1XBA`
- `MaxH`
- `MaxD`
- `MaxA`
- `AvgH`
- `AvgD`
- `AvgA`
- `BFEH`
- `BFED`
- `BFEA`
- `B365>2.5`
- `B365<2.5`
- `P>2.5`
- `P<2.5`
- `Max>2.5`
- `Max<2.5`
- `Avg>2.5`
- `Avg<2.5`
- `BFE>2.5`
- `BFE<2.5`
- `AHh`
- `B365AHH`
- `B365AHA`
- `PAHH`
- `PAHA`
- `MaxAHH`
- `MaxAHA`
- `AvgAHH`
- `AvgAHA`
- `BFEAHH`
- `BFEAHA`
- `B365CH`
- `B365CD`
- `B365CA`
- `BWCH`
- `BWCD`
- `BWCA`
- `BFCH`
- `BFCD`
- `BFCA`
- `PSCH`
- `PSCD`
- `PSCA`
- `WHCH`
- `WHCD`
- `WHCA`
- `1XBCH`
- `1XBCD`
- `1XBCA`
- `MaxCH`
- `MaxCD`
- `MaxCA`
- `AvgCH`
- `AvgCD`
- `AvgCA`
- `BFECH`
- `BFECD`
- `BFECA`
- `B365C>2.5`
- `B365C<2.5`
- `PC>2.5`
- `PC<2.5`
- `MaxC>2.5`
- `MaxC<2.5`
- `AvgC>2.5`
- `AvgC<2.5`
- `BFEC>2.5`
- `BFEC<2.5`
- `AHCh`
- `B365CAHH`
- `B365CAHA`
- `PCAHH`
- `PCAHA`
- `MaxCAHH`
- `MaxCAHA`
- `AvgCAHH`
- `AvgCAHA`
- `BFECAHH`
- `BFECAHA`

## Bookmakers Encontrados

Bookmakers/series inferidos por prefixo de coluna:

- `1XB`: 1xBet
- `Avg`: Market average
- `B365`: Bet365
- `BF`: Betfair Sportsbook
- `BFE`: Betfair Exchange
- `BW`: Bwin
- `Max`: Market maximum
- `P`: Pinnacle
- `PC`: Pinnacle closing
- `PS`: Pinnacle Sports
- `WH`: William Hill

Observacao:

- `Avg` e `Max` nao sao casas; representam agregados de media e maxima de mercado.
- `P`, `PC` e `PS` sao tratados como familias Pinnacle/Pinnacle closing conforme convencao de colunas da fonte.

## Mercados Disponiveis

| Mercado | Colunas | Partidas com algum valor | Cobertura | Exemplos de colunas |
|---|---:|---:|---:|---|
| 1X2 closing | 27 | 380 | 100.00% | `B365CH, B365CD, B365CA, BWCH, BWCD, BWCA, BFCH, BFCD, BFCA, PSCH, PSCD, PSCA, WHCH, WHCD...` |
| 1X2 pre-close/opening-like | 27 | 380 | 100.00% | `B365H, B365D, B365A, BWH, BWD, BWA, BFH, BFD, BFA, PSH, PSD, PSA, WHH, WHD...` |
| Asian Handicap line | 2 | 380 | 100.00% | `AHh, AHCh` |
| Asian Handicap odds | 20 | 380 | 100.00% | `B365AHH, B365AHA, PAHH, PAHA, MaxAHH, MaxAHA, AvgAHH, AvgAHA, BFEAHH, BFEAHA, B365CAHH, B365CAHA, PCAHH, PCAHA...` |
| Over/Under 2.5 | 20 | 380 | 100.00% | `B365>2.5, B365<2.5, P>2.5, P<2.5, Max>2.5, Max<2.5, Avg>2.5, Avg<2.5, BFE>2.5, BFE<2.5, B365C>2.5, B365C<2.5, PC>2.5, PC<2.5...` |

### 1X2 / Match Odds

Disponivel com cobertura completa para 380 partidas.

Exemplos:

- `B365H`, `B365D`, `B365A`
- `BWH`, `BWD`, `BWA`
- `BFH`, `BFD`, `BFA`
- `PSH`, `PSD`, `PSA`
- `WHH`, `WHD`, `WHA`
- `1XBH`, `1XBD`, `1XBA`
- `MaxH`, `MaxD`, `MaxA`
- `AvgH`, `AvgD`, `AvgA`
- `B365CH`, `B365CD`, `B365CA`
- `MaxCH`, `MaxCD`, `MaxCA`
- `AvgCH`, `AvgCD`, `AvgCA`

### Over/Under 2.5

Disponivel com cobertura completa para 380 partidas.

Exemplos:

- `B365>2.5`, `B365<2.5`
- `P>2.5`, `P<2.5`
- `Max>2.5`, `Max<2.5`
- `Avg>2.5`, `Avg<2.5`
- `BFE>2.5`, `BFE<2.5`
- `B365C>2.5`, `B365C<2.5`
- `PC>2.5`, `PC<2.5`
- `MaxC>2.5`, `MaxC<2.5`
- `AvgC>2.5`, `AvgC<2.5`

### BTTS

Nao encontrado no CSV EPL 2024/25 analisado.

### Asian Handicap

Disponivel.

Exemplos:

- `AHh`
- `B365AHH`, `B365AHA`
- `PAHH`, `PAHA`
- `MaxAHH`, `MaxAHA`
- `AvgAHH`, `AvgAHA`
- `BFEAHH`, `BFEAHA`
- `AHCh`
- `B365CAHH`, `B365CAHA`
- `PCAHH`, `PCAHA`
- `MaxCAHH`, `MaxCAHA`
- `AvgCAHH`, `AvgCAHA`

## Opening Odds

Football-Data nao rotula explicitamente todas as colunas como `opening`.

Na estrutura recente do arquivo, ha pares sem `C` e com `C`:

- colunas sem `C`, como `B365H`, `B365D`, `B365A`, `B365>2.5`, `B365<2.5`;
- colunas com `C`, como `B365CH`, `B365CD`, `B365CA`, `B365C>2.5`, `B365C<2.5`.

Interpretacao operacional:

- as colunas com `C` devem ser tratadas como closing snapshot;
- as colunas sem `C` devem ser tratadas como snapshot pre-close/opening-like, mas precisam de confirmacao metodologica antes de serem chamadas oficialmente de opening odds.

Status: **parcialmente encontrado**.

## Closing Odds

Closing odds estao presentes por meio das colunas com `C` para 1X2, Over/Under 2.5 e Asian Handicap.

Status: **encontrado**.

## Odds Medias e Maximas

Disponiveis.

Agregados encontrados:

- `Max*`: melhor/maior odd observada no mercado.
- `Avg*`: odd media do mercado.

Status: **encontrado**.

## Odds Live

Nao ha dados live ou minuto a minuto no CSV.

Status: **nao encontrado**.

## Cobertura Para EPL 2024/25

O arquivo contem **380 partidas validas**, que corresponde ao tamanho esperado de uma temporada completa da Premier League.

Isso e suficiente para cruzamento inicial com as 380 partidas SofaScore importaveis.

## Potencial de Match com SofaScore

Chaves disponiveis para pareamento:

- `Date`
- `Time`
- `HomeTeam`
- `AwayTeam`
- `FTHG`
- `FTAG`
- `FTR`

Potencial de match:

- Alto para pareamento por data, mandante, visitante e placar.
- Necessario criar tabela de normalizacao de nomes de times antes de importer oficial.
- Pode haver diferenca de formato de data/hora e nomes abreviados.

## Artefatos Gerados

- `data/raw/football_data/england/premier_league_2024_2025/E0_2024_2025.csv`
- `data/raw/football_data/england/premier_league_2024_2025/columns_profile.json`
- `data/raw/football_data/england/premier_league_2024_2025/coverage_summary.json`
- `docs/03_SOURCES/ODDS/FOOTBALL_DATA_DISCOVERY_20260607.md`

## Limitacoes

- CSV nao possui odds live.
- CSV nao possui movimento minuto a minuto.
- BTTS nao foi encontrado.
- Opening odds nao aparecem com rotulo explicito; colunas sem `C` precisam de confirmacao metodologica.
- Fonte e arquivo sao estaticos; nao ha garantia de disponibilidade futura sem espelhamento bruto.
- Nao ha IDs SofaScore; cruzamento exige match por data/time/team/placar.
- Antes de uso analitico, sera necessario validar se as colunas sem `C` representam opening, odds iniciais, odds medias no periodo ou snapshot pre-close conforme documentacao da fonte.

## Recomendacao Final

Classificacao: **ALTO POTENCIAL**.

Justificativa:

- O CSV EPL 2024/25 existe e contem 380 partidas.
- Ha ampla cobertura de odds 1X2, Over/Under 2.5 e Asian Handicap.
- Ha colunas de closing odds e agregados `Avg`/`Max`.
- A fonte e gratuita, simples e altamente compativel com match por data/time/team/placar.
- Ausencias relevantes: BTTS, live odds e historico de movimento minuto a minuto.

Recomendacao operacional:

- Football-Data.co.uk deve entrar como **fonte candidata forte para odds historicas pre-match/closing**.
- Proximo passo deve ser especificacao de match mapping e, somente depois, proposta de importer sob aprovacao CTO/Data Engineer.
- Nao usar ainda para features/modelagem ate validar semantica das colunas opening/pre-close e executar auditoria de pareamento com SofaScore.

## Restricoes Respeitadas

- Apenas 1 CSV publico baixado.
- Nenhum importer criado.
- Nenhum banco alterado.
- Nenhum schema alterado.
- Nenhum dataset analitico criado.
- Nenhuma feature criada.
- Nenhuma modelagem executada.
- Nenhum backtesting executado.
- Nenhum coletor SofaScore alterado.
