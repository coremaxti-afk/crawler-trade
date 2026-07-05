# HT JANELAS CASHOUT V1

Status: **ABERTO**  
Tipo: **nova frente de pesquisa**  
Base conceitual: **HT_GOAL_RESEARCH_V1**  
Uso: **pesquisa, nao operacao real**

Esta frente inicia o estudo de janelas recentes antes da entrada e compara operacao OLD contra cashout estimado.

---

## 1. Objetivo

Estudar se os eventos ocorridos nos 5, 10 e 15 minutos antes do cutoff ajudam a identificar entradas lucrativas em mercados de primeiro tempo.

A pergunta principal:

```text
E melhor segurar ate o HT ou sair antes com cashout estimado?
```

---

## 2. Nome oficial

```text
HT_JANELAS_CASHOUT_V1
```

Esta frente e separada de:

```text
HT_GOAL_RESEARCH_V1
```

A frente anterior esta encerrada. Esta nova frente nasce com escopo proprio.

---

## 3. Ligas iniciais

O estudo comeca com tres ligas:

| Liga | Uso |
| --- | --- |
| Premier League | discovery separado e referencia comparativa |
| La Liga | discovery separado e validacao cruzada |
| Serie A Italia | discovery separado e validacao cruzada |

O resultado deve ser separado por liga antes de qualquer consolidacao global.

Objetivo da comparacao:

```text
Entender se cada liga exige padrao proprio ou se existe sinal replicavel entre ligas.
```

---

## 4. Metodo oficial por liga

O metodo oficial da frente e:

```text
discovery separado por liga + validacao cruzada entre ligas
```

A analise global nao vem primeiro. Ela so pode nascer depois da leitura individual de cada liga.

Fluxo correto:

```text
1. Rodar discovery da Premier League.
2. Rodar discovery da La Liga.
3. Rodar discovery da Serie A Italia.
4. Comparar padroes entre ligas.
5. Classificar replicabilidade.
6. Criar leitura global apenas se houver consistencia entre ligas.
```

Regra proibitiva:

```text
Nao criar candidato global apenas pela media das tres ligas.
```

Motivo:

```text
A media global pode esconder que o lucro veio de apenas uma liga ou que uma liga lucrativa mascarou outra negativa.
```

Classificacoes obrigatorias dos padroes:

| Status | Significado |
| --- | --- |
| GLOBAL_REPLICAVEL | Funciona de forma consistente nas tres ligas ou quase |
| SEMI_REPLICAVEL | Funciona em duas de tres ligas |
| ESPECIFICO_DA_LIGA | Funciona bem em uma liga, mas nao replica |
| CONFLITANTE_ENTRE_LIGAS | Funciona em uma liga e falha/perde em outra |
| BLOQUEADO_GLOBALMENTE | Media global pode parecer boa, mas distribuicao por liga e ruim |

A Premier League pode ser usada como referencia comparativa, mas nao como verdade absoluta.

---

## 5. Cutoffs e final do HT

Cutoffs de entrada:

| Cutoff |
| ---: |
| 15 |
| 20 |
| 25 |
| 30 |
| 35 |
| 40 |

Final do primeiro tempo:

```text
45
```

---

## 6. Mercados

| Mercado | Operacao | Exposicao |
| --- | --- | --- |
| GOAL | Back Over HT | stake fixa R$ 100 |
| NO_GOAL | Lay Over HT | responsabilidade fixa R$ 100 |

Regras:

1. GOAL usa stake fixa de R$ 100.
2. NO_GOAL usa responsabilidade fixa de R$ 100.
3. Cashout usa odd media de entrada e odd media de saida.
4. Odds sao medias, nao odds reais.

---

## 7. Modos financeiros

A frente compara dois modos.

### OLD

Entrada no cutoff e permanencia ate o minuto 45.

Exemplo:

```text
entrada 15 -> saida 45
```

### CASHOUT estimado

Entrada no cutoff e saida estimada apos no minimo 10 minutos.

Exemplo:

```text
entrada 15 -> saida 25, 30, 35 ou 40
```

---

## 8. Matriz de entrada e saida

| Entrada | Cashout estimado | OLD |
| ---: | --- | ---: |
| 15 | 25, 30, 35, 40 | 45 |
| 20 | 30, 35, 40 | 45 |
| 25 | 35, 40 | 45 |
| 30 | 40 | 45 |
| 35 | nao aplica | 45 |
| 40 | nao aplica | 45 |

Entradas 35 e 40 ficam apenas em OLD porque nao ha janela minima de 10 minutos para cashout antes do HT.

---

## 9. Logica do cashout estimado

### Back Over HT

| Movimento da odd | Resultado estimado |
| --- | --- |
| Odd sobe | prejuizo |
| Odd desce | lucro |

### Lay Over HT

| Movimento da odd | Resultado estimado |
| --- | --- |
| Odd sobe | lucro |
| Odd desce | prejuizo |

O calculo precisa ser auditavel e separado para Back e Lay.

---

## 10. Janelas antes da entrada

Para cada cutoff, estudar:

```text
ultimos 5 minutos
ultimos 10 minutos
ultimos 15 minutos
```

A metodologia nao deve dobrar ou triplicar eventos de forma cega.

A leitura sera por blocos de 5 minutos.

Exemplo para entrada 30:

| Janela | Blocos |
| --- | --- |
| 5m | 25-30 |
| 10m | 20-25 + 25-30 |
| 15m | 15-20 + 20-25 + 25-30 |

Perfis esperados:

```text
PRESSAO_RECENTE_FORTE
PRESSAO_SUSTENTADA
PRESSAO_AQUECENDO
PRESSAO_ESFRIANDO
PRESSAO_FRACA
PRESSAO_ZERADA
```

Para robo futuro, cada perfil precisara virar regra numerica exata.

---

## 11. Regra sobre scripts

Esta frente nao deve repetir a sujeira de versoes paralelas.

Proibido criar sequencias como:

```text
08.py
08_1.py
08_2.py
score_05.py
score_05_1.py
```

Regra oficial:

```text
um script oficial por etapa
ajustes entram no proprio script original
runner desde o inicio
multi season_id desde o inicio
```

Se precisar registrar evolucao, usar campos nos outputs:

```text
run_version
methodology_version
executed_at
```

Nao criar novo script para cada correcao metodologica.

---

## 12. Runner obrigatorio

A frente deve nascer com runner oficial:

```text
scripts/research/primeiro_tempo/ht_janelas_cashout/run_ht_janelas_cashout_pipeline.py
```

Requisitos:

1. Aceitar um `season_id`.
2. Aceitar multiplos `season_id`.
3. Aceitar `--all-seasons`.
4. Aceitar `--all-leagues` se houver catalogo confiavel.
5. Mostrar progresso no PowerShell.
6. Mostrar erro completo se falhar.
7. Salvar logs.
8. Salvar summary por season.
9. Validar outputs esperados.
10. Nao misturar CSV e Markdown.

Exemplos:

```powershell
python scripts/research/primeiro_tempo/ht_janelas_cashout/run_ht_janelas_cashout_pipeline.py --season-id 25583
python scripts/research/primeiro_tempo/ht_janelas_cashout/run_ht_janelas_cashout_pipeline.py --season-id 25583 25584 25585
python scripts/research/primeiro_tempo/ht_janelas_cashout/run_ht_janelas_cashout_pipeline.py --all-seasons
python scripts/research/primeiro_tempo/ht_janelas_cashout/run_ht_janelas_cashout_pipeline.py --all-seasons --all-leagues
```

---

## 13. Roadmap

### ETAPA 00 — Contrato do projeto

Registrar escopo, ligas, cutoffs, modos financeiros, stake, responsabilidade, cashout, metodo league-first e regras de diretorio.

### ETAPA 01 — Catalogo multi season_id

Criar/validar catalogo com season_id, liga, temporada e disponibilidade.

### ETAPA 02 — Base fixture/cutoff

Criar base por fixture, liga, season_id e cutoff.

### ETAPA 03 — Blocos de 5 minutos

Criar blocos antes da entrada:

```text
cutoff-5 ate cutoff
cutoff-10 ate cutoff-5
cutoff-15 ate cutoff-10
```

### ETAPA 04 — Classificacao das janelas

Transformar blocos em perfis numericos auditaveis.

### ETAPA 05 — Targets OLD

Calcular resultado de entrada ate o minuto 45.

### ETAPA 06 — Targets CASHOUT

Calcular cashout estimado para saidas intermediarias.

### ETAPA 07 — Odds medias

Criar tabela oficial de odds medias por liga/minuto.

### ETAPA 08 — Discovery por liga

Rodar descoberta separada para Premier League, La Liga e Serie A.

Nao consolidar antes de validar cada liga isoladamente.

### ETAPA 09 — Validacao financeira OLD por liga

Validar lucro, ROI, EV, DD e sequencia negativa segurando ate HT para cada liga.

### ETAPA 10 — Validacao financeira CASHOUT por liga

Validar lucro, ROI, EV e DD para saidas estimadas em cada liga.

### ETAPA 11 — OLD vs CASHOUT por liga

Comparar se e melhor segurar ate HT ou sair antes dentro de cada liga.

### ETAPA 12 — Validacao cruzada entre ligas

Comparar Premier League, La Liga e Serie A.

Classificar cada padrao como:

```text
GLOBAL_REPLICAVEL
SEMI_REPLICAVEL
ESPECIFICO_DA_LIGA
CONFLITANTE_ENTRE_LIGAS
BLOQUEADO_GLOBALMENTE
```

### ETAPA 13 — Selecao final

Selecionar candidatos por lucro, ROI, EV, DD, N, sensibilidade, consistencia por liga e replicabilidade.

Candidato global so pode existir se passar pela validacao cruzada.

### ETAPA 14 — Relatorio financeiro final

Gerar Markdown legivel com aliases, tabelas curtas e foco financeiro.

O relatorio final deve separar:

```text
candidatos por liga
candidatos semi-replicaveis
candidatos globais replicaveis
candidatos bloqueados globalmente
```

### ETAPA 15 — Checklist de reprodutibilidade

Registrar scripts, outputs, ordem oficial, proibicoes metodologicas e regra contra media global cega.

---

## 14. Outputs esperados

Markdown:

```text
docs/04_RESEARCH/ACTIVE/HT_JANELAS_CASHOUT_V1.md
```

Futuros relatórios Markdown da frente devem ficar em:

```text
docs/04_RESEARCH/primeiro_tempo/ht_janelas_cashout/
```

CSVs devem ficar em:

```text
data/processed/reports/primeiro_tempo/ht_janelas_cashout/
```

Regra:

```text
Markdown = analise humana
CSV = tabela auditavel
```

---

## 15. Limitacoes iniciais

1. Odds medias, nao odds reais.
2. Cashout estimado, nao cashout real.
3. Sem liquidez, spread, delay, slippage e suspensao.
4. Sem robo nesta fase.
5. Sem operacao real.
6. Sem staking.
7. Sem carteira.
8. Sem candidato global por media cega das ligas.

---

## 16. Status

```text
HT_JANELAS_CASHOUT_V1_ABERTO_COM_ROADMAP_LEAGUE_FIRST
```
