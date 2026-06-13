# FOOTBALL_DATA_FAVORITE_VALIDATION_V2

## Resumo Executivo

Status:

```text
APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL
```

Esta revisao corrige a leitura anterior que usava `favorite_odd <= 1.70` na temporada 2025/26. Para manter compatibilidade com o estudo historico SofaScore, a definicao operacional usada passa a ser:

```text
favorite_side = menor odd pre-jogo 1X2, sem cutoff rigido de odd.
```

Com essa regra, a amostra correta para 2025/26 volta a usar:

```text
h8_cold_combo_10m_2of3: N=69, sem gol 60-75 = 69.6%
h8_pressure_score_10m_bottom25: N=42, sem gol 60-75 = 71.4%
```

A media consolidada entre EPL 2024/25 e EPL 2025/26 fica:

```text
h8_cold_combo_10m_2of3: 88/123 = 71.5%
h8_pressure_score_10m_bottom25: 59/80 = 73.8%
```

## Definicao Oficial Nesta Revisao

```text
Favorito = menor odd pre-jogo 1X2.
```

Regras:

- Home pode ser favorito.
- Away pode ser favorito.
- Draw nao pode ser favorite_side operacional.
- Nao aplicar cutoff `<= 1.70` nesta versao.
- O cutoff `<= 1.70` deve ser tratado apenas como segmentacao conservadora opcional, nao como regra principal.

## Resultados por Temporada

| Estrategia | Temporada | Acertos | Entradas | Taxa sem gol 60-75 | Taxa gol 60-75 |
|---|---|---:|---:|---:|---:|
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 2024/25 | 40 | 54 | 74.1% | 25.9% |
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 2025/26 | 48 | 69 | 69.6% | 30.4% |
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | Consolidado | 88 | 123 | 71.5% | 28.5% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 2024/25 | 29 | 38 | 76.3% | 23.7% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 2025/26 | 30 | 42 | 71.4% | 28.6% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | Consolidado | 59 | 80 | 73.8% | 26.2% |

## Correcao Metodologica

A leitura anterior com `favorite_odd <= 1.70` produziu na 2025/26:

```text
h8_cold_combo_10m_2of3: N=15
h8_pressure_score_10m_bottom25: N=8
```

Essa queda ocorreu porque o corte `<=1.70` eliminou muitos jogos que a metodologia historica considerava favoritos pela menor odd.

Portanto, para comparabilidade com o SofaScore 2024/25, a media correta deve usar:

```text
2025/26 N=69 e N=42
```

E nao:

```text
2025/26 N=15 e N=8
```

## Estimativa Operacional com Odd Media Proximo Gol

Para Lay Over usando odd media 1.50:

```text
Lucro se sem gol: +100
Perda se gol: -50
```

| Estrategia | N consolidado | Acertos | Erros | Lucro estimado | ROI estimado |
|---|---:|---:|---:|---:|---:|
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 123 | 88 | 35 | +7050 | +57.3% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 80 | 59 | 21 | +4850 | +60.6% |

Calculo:

```text
Lucro = acertos * 100 - erros * 50
ROI = lucro / (N * 100)
```

## Leitura

### favorite_winning_by_1 + h8_cold_combo_10m_2of3

- Maior amostra consolidada: N=123.
- Taxa consolidada: 71.5%.
- Estrategia mais robusta por volume.
- Caiu de 74.1% em 2024/25 para 69.6% em 2025/26, mas permaneceu acima de 69%.

### favorite_winning_by_1 + h8_pressure_score_10m_bottom25

- Menor amostra consolidada: N=80.
- Melhor taxa consolidada: 73.8%.
- Manteve consistencia entre 76.3% e 71.4%.
- Melhor ROI estimado no consolidado com odd media.

## Decisao

```text
APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL
```

As duas estrategias mostram consistencia exploratoria na Premier League quando o favorito e definido pela menor odd pre-jogo.

Ainda nao autoriza:

- robo;
- producao;
- trade real;
- backtesting financeiro real;
- automacao operacional.

## Limitacoes

- Odds de entrada no mercado Proximo Gol ainda sao medias observadas/manualizadas, nao odds live historicas por timestamp.
- A validacao e Premier League apenas.
- Precisa replicacao multi-liga para robustez maior.
- A definicao `menor odd = favorito` deve ser mantida para comparabilidade historica; cortes como `<=1.70` devem ser usados apenas como segmentacao secundaria.

## Proxima Frente Recomendada

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1
```

Objetivo:

Testar novos combos por time usando SportMonks `trends`:

- time perdendo pressionando;
- favorito perdendo pressionando;
- favorito vencendo e adversario pressionando;
- mandante vencendo por 1 e visitante pressionando;
- dangerous attacks subindo;
- key passes subindo;
- big chances recentes;
- shots on target recentes.
