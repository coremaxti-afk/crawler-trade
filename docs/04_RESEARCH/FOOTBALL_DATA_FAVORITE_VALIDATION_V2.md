# FOOTBALL_DATA_FAVORITE_VALIDATION_V2

## Resumo Executivo

Status:

```text
APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL
```

Esta revisão corrige duas leituras metodológicas:

1. Para manter compatibilidade com o estudo histórico SofaScore, a definição operacional usada passa a ser:

```text
favorite_side = menor odd pré-jogo 1X2, sem cutoff rígido de odd.
```

2. Para cálculo operacional com cashout aos 75 minutos, não se deve usar lucro cheio de +100 por acerto. A simulação correta com a curva média é:

```text
Lay Over 60' @1.50
Cashout/Back Over 75' @2.00
Stake lay = 100
Lucro se não sair gol até 75' = +25
Prejuízo se sair gol antes de 75' = -50
```

## Definição Oficial Nesta Revisão

```text
Favorito = menor odd pré-jogo 1X2.
```

Regras:

- Home pode ser favorito.
- Away pode ser favorito.
- Draw não pode ser favorite_side operacional.
- Não aplicar cutoff `<= 1.70` nesta versão.
- O cutoff `<= 1.70` deve ser tratado apenas como segmentação conservadora opcional, não como regra principal.

## Resultados por Temporada

| Estratégia | Temporada | Acertos | Entradas | Taxa sem gol 60-75 | Taxa gol 60-75 |
|---|---|---:|---:|---:|---:|
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 2024/25 | 40 | 54 | 74.1% | 25.9% |
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 2025/26 | 48 | 69 | 69.6% | 30.4% |
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | Consolidado | 88 | 123 | 71.5% | 28.5% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 2024/25 | 29 | 38 | 76.3% | 23.7% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 2025/26 | 30 | 42 | 71.4% | 28.6% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | Consolidado | 59 | 80 | 73.8% | 26.2% |

## Correção Metodológica — Cutoff 1.70

A leitura anterior com `favorite_odd <= 1.70` produziu na 2025/26:

```text
h8_cold_combo_10m_2of3: N=15
h8_pressure_score_10m_bottom25: N=8
```

Essa queda ocorreu porque o corte `<=1.70` eliminou muitos jogos que a metodologia histórica considerava favoritos pela menor odd.

Portanto, para comparabilidade com o SofaScore 2024/25, a média correta deve usar:

```text
2025/26 N=69 e N=42
```

E não:

```text
2025/26 N=15 e N=8
```

## Estimativa Operacional Corrigida — Cashout aos 75

Para Lay Over usando a curva média:

```text
Entrada: Lay Over Próximo Gol 60' @1.50
Saída/cashout: Back Over Próximo Gol 75' @2.00
Stake lay: 100
```

Resultado aproximado:

```text
Acerto: sem gol até 75' = +25
Erro: gol antes de 75' = -50
```

| Estratégia | N consolidado | Acertos | Erros | Lucro estimado | ROI estimado |
|---|---:|---:|---:|---:|---:|
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 123 | 88 | 35 | +450 | +3.7% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 80 | 59 | 21 | +425 | +5.3% |

Cálculo:

```text
Lucro = acertos * 25 - erros * 50
ROI = lucro / (N * 100)
```

## Comparação com Simulação Hold Antiga

A conta antiga usava:

```text
Acerto = +100
Erro = -50
```

Essa conta representa segurar a posição até a liquidação completa do mercado, ou uma simplificação de vitória cheia, não o cashout fixo aos 75 minutos.

Para o protocolo real discutido:

```text
Entrada 60'
Cashout 75'
```

a simulação correta é mais conservadora e fica entre +3.7% e +5.3% de ROI estimado.

## Leitura

### favorite_winning_by_1 + h8_cold_combo_10m_2of3

- Maior amostra consolidada: N=123.
- Taxa consolidada: 71.5%.
- ROI estimado com cashout 60→75: +3.7%.
- Estratégia mais robusta por volume, mas margem operacional real é estreita.

### favorite_winning_by_1 + h8_pressure_score_10m_bottom25

- Menor amostra consolidada: N=80.
- Melhor taxa consolidada: 73.8%.
- ROI estimado com cashout 60→75: +5.3%.
- Melhor margem estimada entre as duas.

## Decisão

```text
APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL
```

As duas estratégias mostram consistência exploratória na Premier League quando o favorito é definido pela menor odd pré-jogo.

Ainda não autoriza:

- robô;
- produção;
- trade real;
- backtesting financeiro real;
- automação operacional.

## Limitações

- Odds de entrada e saída no mercado Próximo Gol ainda são médias observadas/manualizadas.
- Não há odds live históricas por timestamp.
- A validação é Premier League apenas.
- A margem com cashout fixo é sensível à curva de odds usada.
- Comissão, slippage, suspensão de mercado e liquidez ainda não foram considerados.
- Precisa replicação multi-liga para robustez maior.

## Próxima Frente Recomendada

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1
```

Objetivo:

Testar novos combos por time usando SportMonks `trends`:

- time perdendo pressionando;
- favorito perdendo pressionando;
- favorito vencendo e adversário pressionando;
- mandante vencendo por 1 e visitante pressionando;
- dangerous attacks subindo;
- key passes subindo;
- big chances recentes;
- shots on target recentes.
