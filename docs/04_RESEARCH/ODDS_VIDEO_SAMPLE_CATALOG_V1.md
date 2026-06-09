# ODDS_VIDEO_SAMPLE_CATALOG_V1

## Objetivo

Catalogar odds coletadas manualmente em videos gravados para criar uma nocao media de variacao das odds em mercados de Under/Over nos minutos finais.

Este documento e exploratorio e nao representa backtesting financeiro real.

## Premissas

- As odds foram informadas manualmente a partir de videos.
- As odds originais foram registradas como Back Under.
- Quando necessario, a conversao para Back Over equivalente usa mercado binario sem margem:

```text
Back Over equivalente = Back Under / (Back Under - 1)
```

- As odds reais de mercado podem ter margem, spread, delay, suspensao e liquidez diferente.
- O objetivo aqui e medir comportamento medio aproximado da curva de odds sem gol.
- Amostras com mudanca de linha durante a coleta ficam catalogadas como `linha variavel` e nao devem ser misturadas diretamente com medias de linha fixa.

---

## Catalogo de amostras

### MATCH_ODDS_SAMPLE_001 — Arsenal x Crystal Palace

```text
Jogo: Arsenal x Crystal Palace
Identificacao provavel: Arsenal 3 x 2 Crystal Palace
Competicao provavel: Carabao Cup / EFL Cup
Data provavel: 18/12/2024
Mercado observado: Back Under proximo gol
Gol observado: Arsenal aos 79'
Observacao: usuario informou gol de escanteio; nao confirmado aqui.
```

#### Odds Back Under

| Minuto | Back Under |
| ---: | ---: |
| 50 | 4.90 |
| 60 | 3.45 |
| 65 | 2.86 |
| 70 | 2.36 |
| 75 | 2.34 |

#### Back Over equivalente

| Minuto | Back Under | Back Over eq. |
| ---: | ---: | ---: |
| 50 | 4.90 | 1.26 |
| 60 | 3.45 | 1.41 |
| 65 | 2.86 | 1.54 |
| 70 | 2.36 | 1.74 |
| 75 | 2.34 | 1.75 |

#### Variacao

```text
Back Under 50->75: 4.90 para 2.34
Queda total: -2.56
Queda percentual: -52.24%
Queda media por minuto: -0.1024

Back Over eq. 50->75: 1.26 para 1.75
Subida total: +0.49
Subida media por minuto: +0.0196
```

---

### MATCH_ODDS_SAMPLE_002 — Crystal Palace x Rayo Vallecano

```text
Jogo: Crystal Palace x Rayo Vallecano
Placar informado/catalogado: Crystal Palace 1 x 0 Rayo Vallecano
Mercado observado: Back Under apos gol / proximo gol
Gol observado: Crystal Palace por volta de 50'
Observacao: identificacao externa ainda deve ser tratada como nao validada.
```

#### Odds Back Under

| Minuto | Back Under |
| ---: | ---: |
| 60 | 2.78 |
| 65 | 2.40 |
| 70 | 2.14 |
| 75 | 1.87 |
| 80 | 1.66 |
| 85 | 1.38 |

#### Back Over equivalente

| Minuto | Back Under | Back Over eq. |
| ---: | ---: | ---: |
| 60 | 2.78 | 1.56 |
| 65 | 2.40 | 1.71 |
| 70 | 2.14 | 1.88 |
| 75 | 1.87 | 2.15 |
| 80 | 1.66 | 2.52 |
| 85 | 1.38 | 3.63 |

#### Variacao

```text
Back Under 60->85: 2.78 para 1.38
Queda total: -1.40
Queda percentual: -50.36%
Queda media por minuto: -0.0560

Back Over eq. 60->85: 1.56 para 3.63
Subida total: +2.07
Subida media por minuto: +0.0828
```

---

### MATCH_ODDS_SAMPLE_003 — Brasil x Tunisia

```text
Jogo: Brasil 1 x 1 Tunisia
Mercado observado: Back Under 2.5
Periodo observado: 60' ate 85'
Placar final informado pelo usuario: 1 x 1
```

#### Odds Back Under 2.5

| Minuto | Back Under |
| ---: | ---: |
| 60 | 3.50 |
| 65 | 2.90 |
| 70 | 2.38 |
| 75 | 2.10 |
| 80 | 1.74 |
| 85 | 1.42 |

#### Back Over equivalente

| Minuto | Back Under | Back Over eq. |
| ---: | ---: | ---: |
| 60 | 3.50 | 1.40 |
| 65 | 2.90 | 1.53 |
| 70 | 2.38 | 1.72 |
| 75 | 2.10 | 1.91 |
| 80 | 1.74 | 2.35 |
| 85 | 1.42 | 3.38 |

#### Variacao

```text
Back Under 60->85: 3.50 para 1.42
Queda total: -2.08
Queda percentual: -59.43%
Queda media por minuto: -0.0832

Back Over eq. 60->85: 1.40 para 3.38
Subida total: +1.98
Subida media por minuto: +0.0792
```

---

### MATCH_ODDS_SAMPLE_004 — Montenegro x Croacia

```text
Jogo: Montenegro x Croacia
Mercado observado: Back Under 3.5
Periodo observado: 65' ate 70'
Gol observado: 71'
```

#### Odds Back Under 3.5

| Minuto | Back Under |
| ---: | ---: |
| 65 | 3.20 |
| 70 | 2.54 |

#### Back Over equivalente

| Minuto | Back Under | Back Over eq. |
| ---: | ---: | ---: |
| 65 | 3.20 | 1.45 |
| 70 | 2.54 | 1.65 |

#### Variacao

```text
Back Under 65->70: 3.20 para 2.54
Queda total: -0.66
Queda percentual: -20.63%
Queda media por minuto: -0.1320

Back Over eq. 65->70: 1.45 para 1.65
Subida total: +0.20
Subida media por minuto: +0.0400
```

---

### MATCH_ODDS_SAMPLE_005 — Armenia x Hungary

```text
Jogo: Armenia x Hungary
Placar final informado: 1 x 0 para algum time
Mercado observado: Back Under 1.5
Periodo observado: 65' ate 85'
Gol observado no periodo: nao informado
```

#### Odds Back Under 1.5

| Minuto | Back Under |
| ---: | ---: |
| 65 | 2.40 |
| 70 | 1.96 |
| 75 | 1.80 |
| 80 | 1.52 |
| 85 | 1.34 |

#### Back Over equivalente

| Minuto | Back Under | Back Over eq. |
| ---: | ---: | ---: |
| 65 | 2.40 | 1.71 |
| 70 | 1.96 | 2.04 |
| 75 | 1.80 | 2.25 |
| 80 | 1.52 | 2.92 |
| 85 | 1.34 | 3.94 |

#### Variacao

```text
Back Under 65->85: 2.40 para 1.34
Queda total: -1.06
Queda percentual: -44.17%
Queda media por minuto: -0.0530

Back Over eq. 65->85: 1.71 para 3.94
Subida total: +2.23
Subida media por minuto: +0.1115
```

---

### MATCH_ODDS_SAMPLE_006 — Gremio x Fluminense

```text
Jogo: Gremio x Fluminense
Identificacao confirmada pelo usuario: Gremio 1 x 2 Fluminense
Data: 02/12/2025
Competicao: Campeonato Brasileiro
Mercado observado: Back Under 3.5
Periodo observado: 60' ate 85'
Gols informados: Fluminense aos 51' e Gremio aos 53'
Contexto: coleta pos-gols, placar provavelmente 1 x 1 aos 60'
```

#### Odds Back Under 3.5

| Minuto | Back Under |
| ---: | ---: |
| 60 | 2.56 |
| 65 | 2.30 |
| 70 | 2.02 |
| 75 | 1.74 |
| 80 | 1.58 |
| 85 | 1.38 |

#### Back Over equivalente

| Minuto | Back Under | Back Over eq. |
| ---: | ---: | ---: |
| 60 | 2.56 | 1.64 |
| 65 | 2.30 | 1.77 |
| 70 | 2.02 | 1.98 |
| 75 | 1.74 | 2.35 |
| 80 | 1.58 | 2.72 |
| 85 | 1.38 | 3.63 |

#### Variacao

```text
Back Under 60->85: 2.56 para 1.38
Queda total: -1.18
Queda percentual: -46.09%
Queda media por minuto: -0.0472

Back Over eq. 60->85: 1.64 para 3.63
Subida total: +1.99
Subida media por minuto: +0.0796
```

---

### MATCH_ODDS_SAMPLE_007 — Hammarby x Halmstads

```text
Jogo: Hammarby x Halmstads
Data: nao identificada ainda
Competicao: nao identificada ainda
Mercado observado: Back Under 2.5
Periodo observado: 60' ate 85'
Gol informado: entre 57' e 59'
Contexto: coleta pos-gol; depois nao saiu mais gol segundo o usuario.
Status de identificacao: pendente; busca inicial nao encontrou correspondencia confiavel pelo minuto do gol.
```

#### Odds Back Under 2.5

| Minuto | Back Under |
| ---: | ---: |
| 60 | 3.30 |
| 65 | 3.00 |
| 70 | 2.60 |
| 75 | 2.14 |
| 80 | 1.83 |
| 85 | 1.49 |

#### Back Over equivalente

| Minuto | Back Under | Back Over eq. |
| ---: | ---: | ---: |
| 60 | 3.30 | 1.43 |
| 65 | 3.00 | 1.50 |
| 70 | 2.60 | 1.63 |
| 75 | 2.14 | 1.88 |
| 80 | 1.83 | 2.20 |
| 85 | 1.49 | 3.04 |

#### Variacao

```text
Back Under 60->85: 3.30 para 1.49
Queda total: -1.81
Queda percentual: -54.85%
Queda media por minuto: -0.0724

Back Over eq. 60->85: 1.43 para 3.04
Subida total: +1.61
Subida media por minuto: +0.0644
```

---

### MATCH_ODDS_SAMPLE_008 — Juventus x Manchester City

```text
Jogo: Juventus 2 x 5 Manchester City
Competicao: Mundial de Clubes 2025
Fase: Grupos — Grupo G
Mercado observado: Back Under com linha variavel
Periodo observado: 60' ate 80'
Gols informados no periodo/recentes: 52', 69', 75' e 84'
Observacao: a linha mudou de Under 4.5 para Under 5.5 e depois Under 6.5; nao misturar diretamente com curvas de linha fixa.
```

#### Odds Back Under — linha variavel

| Minuto | Mercado | Back Under |
| ---: | --- | ---: |
| 60 | Under 4.5 | 3.95 |
| 65 | Under 4.5 | 3.15 |
| 70 | Under 5.5 | 2.64 |
| 75 | Under 5.5 | 2.18 |
| 80 | Under 6.5 | 1.99 |

#### Back Over equivalente

| Minuto | Mercado | Back Under | Back Over eq. |
| ---: | --- | ---: | ---: |
| 60 | Over 4.5 eq. | 3.95 | 1.34 |
| 65 | Over 4.5 eq. | 3.15 | 1.47 |
| 70 | Over 5.5 eq. | 2.64 | 1.61 |
| 75 | Over 5.5 eq. | 2.18 | 1.85 |
| 80 | Over 6.5 eq. | 1.99 | 2.01 |

#### Variacao observada na linha variavel

```text
Back Under 60->80: 3.95 para 1.99
Queda total: -1.96
Queda media por minuto: -0.0980

Back Over eq. 60->80: 1.34 para 2.01
Subida total: +0.67
Subida media por minuto: +0.0335

Amostra marcada como linha variavel, pois a linha mudou de 4.5 para 5.5 e 6.5 apos gols.
```

---

## Comparacao geral — variacao por amostra de linha fixa

| Amostra | Jogo | Mercado | Periodo | Under inicial | Under final | Queda Under/min | Over eq. inicial | Over eq. final | Subida Over/min |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 001 | Arsenal x Crystal Palace | Proximo gol | 50-75 | 4.90 | 2.34 | -0.1024 | 1.26 | 1.75 | +0.0196 |
| 002 | Crystal Palace x Rayo Vallecano | Proximo gol/pos-gol | 60-85 | 2.78 | 1.38 | -0.0560 | 1.56 | 3.63 | +0.0828 |
| 003 | Brasil x Tunisia | Under/Over 2.5 | 60-85 | 3.50 | 1.42 | -0.0832 | 1.40 | 3.38 | +0.0792 |
| 004 | Montenegro x Croacia | Under/Over 3.5 | 65-70 | 3.20 | 2.54 | -0.1320 | 1.45 | 1.65 | +0.0400 |
| 005 | Armenia x Hungary | Under/Over 1.5 | 65-85 | 2.40 | 1.34 | -0.0530 | 1.71 | 3.94 | +0.1115 |
| 006 | Gremio x Fluminense | Under/Over 3.5 pos-gols | 60-85 | 2.56 | 1.38 | -0.0472 | 1.64 | 3.63 | +0.0796 |
| 007 | Hammarby x Halmstads | Under/Over 2.5 pos-gol | 60-85 | 3.30 | 1.49 | -0.0724 | 1.43 | 3.04 | +0.0644 |

## Amostras de linha variavel — nao inclusas na media geral de linha fixa

| Amostra | Jogo | Mercados | Periodo | Under inicial | Under final | Over eq. inicial | Over eq. final | Observacao |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 008 | Juventus x Manchester City | U4.5/U5.5/U6.5 | 60-80 | 3.95 | 1.99 | 1.34 | 2.01 | gols aos 69, 75 e 84; linha mudou |

## Media geral atual — linha fixa

```text
Media simples da queda Back Under por minuto:
(-0.1024 -0.0560 -0.0832 -0.1320 -0.0530 -0.0472 -0.0724) / 7 = -0.0780 por minuto

Media simples da subida Back Over equivalente por minuto:
(0.0196 +0.0828 +0.0792 +0.0400 +0.1115 +0.0796 +0.0644) / 7 = +0.0653 por minuto
```

## Media Back Over equivalente por minuto observado — linha fixa

### Media nos pontos com dados disponiveis

| Minuto | Amostras usadas | Media Back Over eq. |
| ---: | ---: | ---: |
| 50 | 1 | 1.26 |
| 60 | 5 | 1.49 |
| 65 | 7 | 1.60 |
| 70 | 7 | 1.81 |
| 75 | 6 | 2.05 |
| 80 | 5 | 2.54 |
| 85 | 5 | 3.52 |

### Media 65-85 usando amostras com dados completos nesse periodo

Amostras usadas: MATCH_ODDS_SAMPLE_002, MATCH_ODDS_SAMPLE_003, MATCH_ODDS_SAMPLE_005, MATCH_ODDS_SAMPLE_006 e MATCH_ODDS_SAMPLE_007.

| Minuto | Media Back Over eq. |
| ---: | ---: |
| 65 | 1.64 |
| 70 | 1.85 |
| 75 | 2.11 |
| 80 | 2.54 |
| 85 | 3.52 |

```text
Back Over medio 65->85: 1.64 para 3.52
Subida total media: +1.88
Subida media por minuto: +0.0940
```

---

## Leitura inicial

- A curva de Back Under cai com forca quando nao sai gol, como esperado.
- Convertendo para Back Over equivalente, a odd tende a subir contra uma entrada Back Over sem gol.
- Nas amostras completas de 65 a 85, o Back Over equivalente saiu em media de 1.64 para 3.52.
- A amostra ainda e pequena e mistura mercados diferentes: proximo gol, Under 1.5, Under 2.5 e Under 3.5.
- A amostra Juventus x Manchester City foi separada por ser linha variavel, com gols que alteraram a linha de mercado.
- O ideal e separar as medias por mercado:
  - proximo gol;
  - Under/Over 1.5;
  - Under/Over 2.5;
  - Under/Over 3.5;
  - linha variavel;
  - apos gol;
  - antes de gol.

---

## Template para novas amostras

```text
MATCH_ODDS_SAMPLE_XXX
Jogo:
Competicao:
Data:
Placar final:
Mercado observado:
Minuto/placar no inicio da coleta:
Gol saiu? sim/nao
Minuto do gol:
Time do gol:
Observacoes:

Odds Back Under:
50=
55=
60=
65=
70=
75=
80=
85=
90=
```

## Proximos passos

1. Continuar adicionando amostras dos videos.
2. Manter separado o tipo de mercado observado.
3. Marcar se houve gol e o minuto do gol.
4. Depois de pelo menos 20 amostras, calcular medias por grupo de mercado e periodo.
5. Evitar usar esses dados como estrategia ate ter amostra suficiente e odds historicas mais consistentes.
