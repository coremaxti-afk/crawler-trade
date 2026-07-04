# DICIONARIO_PARCIAL_DE_ESTRATEGIAS_E_PRESSOES_HT_MICRO_DISCOVERY_ENGINE_V1

## 1. Objetivo

Este documento é um dicionário parcial dos aliases de estratégias da frente `HT_MICRO_DISCOVERY_ENGINE_V1`.

O foco principal deste dicionário é traduzir:

- aliases usados nos relatórios;
- modo da estratégia;
- mercado;
- minuto de entrada;
- minuto de saída;
- janela estatística `w5`, `w10`, `w15`;
- classe de pressão disponível nos MDs;
- estatísticas financeiras disponíveis nos MDs enviados.

Este documento é parcial porque foi construído apenas com os relatórios Markdown enviados no chat, não com os CSVs completos da frente.

## 2. Aviso de escopo

Este dicionário não valida estratégia, não autoriza operação real, não define staking e não cria robô.

Ele apenas organiza aliases, parâmetros e estatísticas da fase de discovery para futura validação.

## 3. Limitação importante sobre pressão numérica

Os relatórios Markdown enviados trazem a **classe textual de pressão** em alguns relatórios, por exemplo:

- `MUITO_FORTE`
- `FORTE`
- `MODERADA`
- `FRACA`

Mas os MDs enviados não trazem o valor numérico bruto de `pressure_score`, nem os números de cada componente estatístico da pressão, como:

- ataques perigosos;
- finalizações;
- finalizações no alvo;
- escanteios;
- passes-chave;
- grandes chances.

Portanto, neste dicionário parcial:

```text
pressao_classe = classe textual disponível no MD
pressao_score_exato = NAO_DISPONIVEL_NO_MD
componentes_pressao = NAO_DISPONIVEL_NO_MD
```

Para configurar robô futuramente, o dicionário completo deve ser gerado a partir dos CSVs completos e/ou da `micro_base_fixture_cutoff.csv`, incluindo:

```text
pressure_score
dangerous_attacks
shots
shots_on_target
corners
key_passes
big_chances
```

## 4. Tradução das janelas estatísticas

| Código | Tradução humana | Intervalo estatístico em relação à entrada |
|---|---|---|
| `w5` | Últimos 5 minutos antes da entrada | `[entry_minute - 5, entry_minute)` |
| `w10` | Últimos 10 minutos antes da entrada | `[entry_minute - 10, entry_minute)` |
| `w15` | Últimos 15 minutos antes da entrada | `[entry_minute - 15, entry_minute)` |

Exemplo:

| Entrada | Janela | Intervalo estatístico |
|---:|---|---|
| 20 | `w5` | 15 a 19 |
| 20 | `w10` | 10 a 19 |
| 20 | `w15` | 5 a 19 |
| 30 | `w5` | 25 a 29 |
| 30 | `w10` | 20 a 29 |
| 30 | `w15` | 15 a 29 |
| 40 | `w5` | 35 a 39 |
| 40 | `w10` | 30 a 39 |
| 40 | `w15` | 25 a 39 |

Observação: a implementação oficial deve confirmar se o intervalo é fechado/aberto exatamente como `[start, end)` no script.

## 5. Dicionário de abreviações dos aliases

| Abreviação | Significado técnico | Significado humano |
|---|---|---|
| `NS` | `NO_SCORE` | Sem placar |
| `SC` | `WITH_SCORE` | Com placar |
| `OLD` | `OLD` | Manter até o HT |
| `CO` | `CASHOUT` | Cashout estimado |
| `G` | `GOAL` | Gol / Back Over HT |
| `NG` | `NO_GOAL` | Sem gol / Lay Over HT |
| `EMP` | `EMPATE` | Empate |
| `QTG` | `QUALQUER_TIME_GANHANDO` | Qualquer time ganhando |
| `MEV` | `MANDANTE_EM_VANTAGEM` | Mandante em vantagem |
| `VEV` | `VISITANTE_EM_VANTAGEM` | Visitante em vantagem |
| `W5` | `w5` | Últimos 5 minutos |
| `W10` | `w10` | Últimos 10 minutos |
| `W15` | `w15` | Últimos 15 minutos |

## 6. Buckets de placar

| Bucket técnico | Nome humano | Regra |
|---|---|---|
| `EMPATE` | Empate | `score_home_at_entry == score_away_at_entry` |
| `QUALQUER_TIME_GANHANDO` | Qualquer time ganhando | `score_home_at_entry != score_away_at_entry` |
| `MANDANTE_EM_VANTAGEM` | Mandante em vantagem | `score_home_at_entry > score_away_at_entry` |
| `VISITANTE_EM_VANTAGEM` | Visitante em vantagem | `score_away_at_entry > score_home_at_entry` |

Atenção: `QUALQUER_TIME_GANHANDO` é um bucket agregado. Ele pode compartilhar fixtures com `MANDANTE_EM_VANTAGEM` e `VISITANTE_EM_VANTAGEM`. Não somar lucros entre esses buckets.

## 7. Mercados e modos

| Código | Significado |
|---|---|
| `GOAL` | Gol / Back Over HT |
| `NO_GOAL` | Sem gol / Lay Over HT |
| `OLD` | Manter até o intervalo, minuto 45 |
| `CASHOUT` | Cashout estimado em minuto de saída definido |

## 8. Fórmula esperada da pressão

A fórmula de pressão esperada da frente é:

```text
pressure_score =
1.0 * dangerous_attacks
+ 2.0 * shots
+ 3.0 * shots_on_target
+ 1.5 * corners
+ 1.5 * key_passes
+ 4.0 * big_chances
```

Este documento parcial não possui os valores exatos desses componentes por alias.

Para robô futuro, cada estratégia precisa trazer:

```text
window_type
pressure_class
pressure_score_min
pressure_score_max
ou regra exata de classificação usada no script
```

## 9. Dicionário parcial de aliases — Sem placar CASHOUT

Fonte: `02_SEM_PLACAR_CASHOUT_HT_MICRO_DISCOVERY_ENGINE_V1.md`.

| Alias | Tradução humana | Pressão | Pressão numérica | N | Lucro | ROI | EV | DD | Max LS | Status |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `NS-CO-G-20-40-W10-01` | Sem placar; Cashout; Gol / Back Over HT; entrada 20; saída 40; últimos 10 minutos | MUITO_FORTE | NAO_DISPONIVEL_NO_MD | 76 | R$ 1.576,85 | 20,8% | R$ 20,75 | R$ -157,65 | 3 | CANDIDATA_DISCOVERY |
| `NS-CO-G-20-40-W15-02` | Sem placar; Cashout; Gol / Back Over HT; entrada 20; saída 40; últimos 15 minutos | MUITO_FORTE | NAO_DISPONIVEL_NO_MD | 91 | R$ 1.565,90 | 17,2% | R$ 17,21 | R$ -266,40 | 4 | CANDIDATA_DISCOVERY |
| `NS-CO-G-25-40-W10-03` | Sem placar; Cashout; Gol / Back Over HT; entrada 25; saída 40; últimos 10 minutos | FORTE | NAO_DISPONIVEL_NO_MD | 66 | R$ 1.458,70 | 22,1% | R$ 22,10 | R$ -376,30 | 5 | CANDIDATA_DISCOVERY |
| `NS-CO-G-20-35-W10-05` | Sem placar; Cashout; Gol / Back Over HT; entrada 20; saída 35; últimos 10 minutos | MUITO_FORTE | NAO_DISPONIVEL_NO_MD | 76 | R$ 1.205,47 | 15,9% | R$ 15,86 | R$ -181,65 | 5 | CANDIDATA_DISCOVERY |
| `NS-CO-G-15-40-W15-06` | Sem placar; Cashout; Gol / Back Over HT; entrada 15; saída 40; últimos 15 minutos | MUITO_FORTE | NAO_DISPONIVEL_NO_MD | 39 | R$ 1.175,67 | 30,1% | R$ 30,15 | R$ -168,09 | 3 | CANDIDATA_DISCOVERY |
| `NS-CO-G-15-40-W10-07` | Sem placar; Cashout; Gol / Back Over HT; entrada 15; saída 40; últimos 10 minutos | MUITO_FORTE | NAO_DISPONIVEL_NO_MD | 35 | R$ 1.159,73 | 33,1% | R$ 33,14 | R$ -112,06 | 2 | CANDIDATA_DISCOVERY |
| `NS-CO-G-15-30-W15-08` | Sem placar; Cashout; Gol / Back Over HT; entrada 15; saída 30; últimos 15 minutos | MODERADA | NAO_DISPONIVEL_NO_MD | 57 | R$ 1.133,88 | 19,9% | R$ 19,89 | R$ -103,16 | 4 | CANDIDATA_DISCOVERY |
| `NS-CO-G-15-40-W15-09` | Sem placar; Cashout; Gol / Back Over HT; entrada 15; saída 40; últimos 15 minutos | MODERADA | NAO_DISPONIVEL_NO_MD | 57 | R$ 1.127,37 | 19,8% | R$ 19,78 | R$ -112,06 | 2 | CANDIDATA_DISCOVERY |
| `NS-CO-G-15-30-W10-10` | Sem placar; Cashout; Gol / Back Over HT; entrada 15; saída 30; últimos 10 minutos | MODERADA | NAO_DISPONIVEL_NO_MD | 46 | R$ 1.058,41 | 23,0% | R$ 23,01 | R$ -77,37 | 3 | CANDIDATA_DISCOVERY |
| `NS-CO-G-20-40-W5-11` | Sem placar; Cashout; Gol / Back Over HT; entrada 20; saída 40; últimos 5 minutos | FORTE | NAO_DISPONIVEL_NO_MD | 44 | R$ 1.056,10 | 24,0% | R$ 24,00 | R$ -157,65 | 3 | CANDIDATA_DISCOVERY |

## 10. Dicionário parcial de aliases — Sem placar OLD

Fonte: `01_SEM_PLACAR_OLD_HT_MICRO_DISCOVERY_ENGINE_V1.md` enviado anteriormente.  
Observação: a versão do MD disponível neste chat não continha EV e Max LS nas tabelas. Se a versão corrigida existir no repositório, o dicionário completo deve usar a versão corrigida ou o CSV.

| Alias | Tradução humana | Pressão | Pressão numérica | N | Lucro | ROI | EV | DD | Max LS | Status |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `NS-OLD-NG-40-W15-01` | Sem placar; Manter até HT; Sem gol / Lay Over HT; entrada 40; saída 45; últimos 15 minutos | MUITO_FORTE | NAO_DISPONIVEL_NO_MD | 101 | R$ 2.060,07 | 20,4% | NAO_DISPONIVEL_NO_MD | R$ -200,00 | NAO_DISPONIVEL_NO_MD | CANDIDATA_DISCOVERY |
| `NS-OLD-NG-20-W15-02` | Sem placar; Manter até HT; Sem gol / Lay Over HT; entrada 20; saída 45; últimos 15 minutos | FORTE | NAO_DISPONIVEL_NO_MD | 26 | R$ 1.997,40 | 76,8% | NAO_DISPONIVEL_NO_MD | R$ -300,00 | NAO_DISPONIVEL_NO_MD | CANDIDATA_DISCOVERY |
| `NS-OLD-NG-20-W10-03` | Sem placar; Manter até HT; Sem gol / Lay Over HT; entrada 20; saída 45; últimos 10 minutos | FORTE | NAO_DISPONIVEL_NO_MD | 24 | R$ 1.507,79 | 62,8% | NAO_DISPONIVEL_NO_MD | R$ -200,00 | NAO_DISPONIVEL_NO_MD | CANDIDATA_DISCOVERY |
| `NS-OLD-NG-20-W5-04` | Sem placar; Manter até HT; Sem gol / Lay Over HT; entrada 20; saída 45; últimos 5 minutos | FORTE | NAO_DISPONIVEL_NO_MD | 29 | R$ 1.467,53 | 50,6% | NAO_DISPONIVEL_NO_MD | R$ -300,00 | NAO_DISPONIVEL_NO_MD | CANDIDATA_DISCOVERY |
| `NS-OLD-NG-40-W10-05` | Sem placar; Manter até HT; Sem gol / Lay Over HT; entrada 40; saída 45; últimos 10 minutos | MUITO_FORTE | NAO_DISPONIVEL_NO_MD | 69 | R$ 1.434,43 | 20,8% | NAO_DISPONIVEL_NO_MD | R$ -100,00 | NAO_DISPONIVEL_NO_MD | CANDIDATA_DISCOVERY |
| `NS-OLD-G-15-W10-06` | Sem placar; Manter até HT; Gol / Back Over HT; entrada 15; saída 45; últimos 10 minutos | MUITO_FORTE | NAO_DISPONIVEL_NO_MD | 35 | R$ 1.420,00 | 40,6% | NAO_DISPONIVEL_NO_MD | R$ -236,00 | NAO_DISPONIVEL_NO_MD | CANDIDATA_DISCOVERY |

## 11. Dicionário parcial de aliases — Com placar OLD

Fonte: `03_COM_PLACAR_OLD_HT_MICRO_DISCOVERY_ENGINE_V1.md`.  
Observação: o MD enviado não contém a coluna `Pressão`, então a pressão fica como `NAO_DISPONIVEL_NO_MD`.

| Alias | Tradução humana | Pressão | Pressão numérica | N | Lucro | ROI | EV | DD | Max LS | Status |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `SC-OLD-NG-35-EMP-W15-01` | Com placar; Manter até HT; Sem gol / Lay Over HT; Empate; entrada 35; saída 45; últimos 15 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 32 | R$ 1.329,22 | 41,5% | R$ 41,54 | R$ -200,00 | 2 | CANDIDATA_DISCOVERY |
| `SC-OLD-NG-20-EMP-W15-02` | Com placar; Manter até HT; Sem gol / Lay Over HT; Empate; entrada 20; saída 45; últimos 15 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 13 | R$ 1.228,57 | 94,5% | R$ 94,51 | R$ -100,00 | 1 | BOA_COM_RESSALVA_DISCOVERY |
| `SC-OLD-NG-35-QTG-W5-03` | Com placar; Manter até HT; Sem gol / Lay Over HT; Qualquer time ganhando; entrada 35; saída 45; últimos 5 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 35 | R$ 1.185,40 | 33,9% | R$ 33,87 | R$ -200,00 | 2 | CANDIDATA_DISCOVERY |
| `SC-OLD-G-30-MEV-W5-09` | Com placar; Manter até HT; Gol / Back Over HT; Mandante em vantagem; entrada 30; saída 45; últimos 5 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 15 | R$ 931,00 | 62,1% | R$ 62,07 | R$ -200,00 | 2 | BOA_COM_RESSALVA_DISCOVERY |
| `SC-OLD-G-30-EMP-W10-10` | Com placar; Manter até HT; Gol / Back Over HT; Empate; entrada 30; saída 45; últimos 10 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 22 | R$ 894,00 | 40,6% | R$ 40,64 | R$ -200,00 | 2 | CANDIDATA_DISCOVERY |

## 12. Dicionário parcial de aliases — Com placar CASHOUT

Fonte: `04_COM_PLACAR_CASHOUT_HT_MICRO_DISCOVERY_ENGINE_V1.md`.  
Observação: o MD enviado não contém a coluna `Pressão`, então a pressão fica como `NAO_DISPONIVEL_NO_MD`.

| Alias | Tradução humana | Pressão | Pressão numérica | N | Lucro | ROI | EV | DD | Max LS | Status |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `SC-CO-G-30-40-EMP-W10-01` | Com placar; Cashout; Gol / Back Over HT; Empate; entrada 30; saída 40; últimos 10 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 22 | R$ 882,75 | 40,1% | R$ 40,12 | R$ -81,50 | 2 | CANDIDATA_DISCOVERY |
| `SC-CO-G-20-40-EMP-W10-02` | Com placar; Cashout; Gol / Back Over HT; Empate; entrada 20; saída 40; últimos 10 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 40 | R$ 877,65 | 21,9% | R$ 21,94 | R$ -161,30 | 3 | CANDIDATA_DISCOVERY |
| `SC-CO-G-25-40-QTG-W15-03` | Com placar; Cashout; Gol / Back Over HT; Qualquer time ganhando; entrada 25; saída 40; últimos 15 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 46 | R$ 829,75 | 18,0% | R$ 18,04 | R$ -237,25 | 5 | CANDIDATA_DISCOVERY |
| `SC-CO-G-20-35-EMP-W10-04` | Com placar; Cashout; Gol / Back Over HT; Empate; entrada 20; saída 35; últimos 10 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 40 | R$ 813,40 | 20,3% | R$ 20,34 | R$ -108,99 | 3 | CANDIDATA_DISCOVERY |
| `SC-CO-G-20-40-EMP-W15-05` | Com placar; Cashout; Gol / Back Over HT; Empate; entrada 20; saída 40; últimos 15 minutos | NAO_DISPONIVEL_NO_MD | NAO_DISPONIVEL_NO_MD | 44 | R$ 797,00 | 18,1% | R$ 18,11 | R$ -185,75 | 3 | CANDIDATA_DISCOVERY |

## 13. Campos mínimos que o dicionário completo deve ter para robô futuro

O CSV completo do dicionário deve conter, no mínimo:

```text
alias
traducao_humana
score_scope
score_bucket
market
mode
entry_minute
exit_minute
cashout_minute
window_type
window_start_minute
window_end_minute
pressure_class
pressure_score
pressure_score_min
pressure_score_max
dangerous_attacks
shots
shots_on_target
corners
key_passes
big_chances
N
wins
losses
profit_brl
ROI_pct
EV_brl
max_drawdown_brl
max_losing_streak
avg_entry_odd
avg_exit_odd
status
status_reason
futura_configuracao_robo
```

Valor obrigatório para esta fase:

```text
futura_configuracao_robo = NAO_AUTORIZADO_DISCOVERY_APENAS
```

## 14. Pendências para o dicionário completo

Para transformar este dicionário parcial em completo, é necessário:

1. usar os CSVs completos `01/02/03/04`;
2. usar a `micro_base_fixture_cutoff.csv`;
3. incluir `pressure_score` por estratégia;
4. incluir componentes de pressão por janela;
5. incluir thresholds reais usados na classificação;
6. garantir que a pressão aparece nos relatórios com placar;
7. gerar CSV e, se possível, JSON para futura parametrização.

## 15. Status

```text
DICIONARIO_PARCIAL_CRIADO_COM_PRESSAO_TEXTUAL_E_JANELAS_ESTATISTICAS
```
