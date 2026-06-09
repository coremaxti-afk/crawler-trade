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

## Comparacao geral — variacao por amostra

| Amostra | Jogo | Mercado | Periodo | Under inicial | Under final | Queda Under/min | Over eq. inicial | Over eq. final | Subida Over/min |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 001 | Arsenal x Crystal Palace | Proximo gol | 50-75 | 4.90 | 2.34 | -0.1024 | 1.26 | 1.75 | +0.0196 |
| 002 | Crystal Palace x Rayo Vallecano | Proximo gol/pos-gol | 60-85 | 2.78 | 1.38 | -0.0560 | 1.56 | 3.63 | +0.0828 |
| 003 | Brasil x Tunisia | Under/Over 2.5 | 60-85 | 3.50 | 1.42 | -0.0832 | 1.40 | 3.38 | +0.0792 |
| 004 | Montenegro x Croacia | Under/Over 3.5 | 65-70 | 3.20 | 2.54 | -0.1320 | 1.45 | 1.65 | +0.0400 |
| 005 | Armenia x Hungary | Under/Over 1.5 | 65-85 | 2.40 | 1.34 | -0.0530 | 1.71 | 3.94 | +0.1115 |
| 006 | Gremio x Fluminense | Under/Over 3.5 pos-gols | 60-85 | 2.56 | 1.38 | -0.0472 | 1.64 | 3.63 | +0.0796 |

## Media geral atual

```text
Media simples da queda Back Under por minuto:
(-0.1024 -0.0560 -0.0832 -0.1320 -0.0530 -0.0472) / 6 = -0.0790 por minuto

Media simples da subida Back Over equivalente por minuto:
(0.0196 +0.0828 +0.0792 +0.0400 +0.1115 +0.0796) / 6 = +0.0688 por minuto
```

## Media Back Over equivalente por minuto observado

### Media nos pontos com dados disponiveis

| Minuto | Amostras usadas | Media Back Over eq. |
| ---: | ---: | ---: |
| 50 | 1 | 1.26 |
| 60 | 4 | 1.50 |
| 65 | 6 | 1.62 |
| 70 | 6 | 1.84 |
| 75 | 5 | 2.08 |
| 80 | 4 | 2.63 |
| 85 | 4 | 3.64 |

### Media 65-85 usando amostras com dados completos nesse periodo

Amostras usadas: MATCH_ODDS_SAMPLE_002, MATCH_ODDS_SAMPLE_003, MATCH_ODDS_SAMPLE_005 e MATCH_ODDS_SAMPLE_006.

| Minuto | Media Back Over eq. |
| ---: | ---: |
| 65 | 1.68 |
| 70 | 1.91 |
| 75 | 2.17 |
| 80 | 2.63 |
| 85 | 3.64 |

```text
Back Over medio 65->85: 1.68 para 3.64
Subida total media: +1.96
Subida media por minuto: +0.0980
```

---

## Leitura inicial

- A curva de Back Under cai com forca quando nao sai gol, como esperado.
- Convertendo para Back Over equivalente, a odd tende a subir contra uma entrada Back Over sem gol.
- Nas amostras completas de 65 a 85, o Back Over equivalente saiu em media de 1.68 para 3.64.
- A amostra ainda e pequena e mistura mercados diferentes: proximo gol, Under 1.5, Under 2.5 e Under 3.5.
- O ideal e separar as medias por mercado:
  - proximo gol;
  - Under/Over 1.5;
  - Under/Over 2.5;
  - Under/Over 3.5;
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
