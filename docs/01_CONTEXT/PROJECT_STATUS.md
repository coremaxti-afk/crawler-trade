# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
PESQUISA_GOLS_TARDIOS_V1_ENCERRADA_COM_RESSALVAS_ESTATISTICAS
FRENTE_COMPLEMENTAR_ATIVA: ESTUDO_FORCA_ESTADO_TEMPERATURA_JOGO_V1
```

Status oficial:

```text
ENCERRAMENTO_CIENTIFICO_GOLS_TARDIOS_V1 CONCLUIDO
SEM EVIDENCIA DE LEAKAGE CRITICO NOS ARTEFATOS AUDITADOS
RADAR_PREDITIVO_DE_TEMPORADA_V1 CORRIGIDO PARA USAR APENAS METRICAS INICIAIS ini_*
VALIDACAO_PROSPECTIVA_DO_RADAR_V1 REEXECUTADA APOS CORRECAO ANTI-LEAKAGE
NENHUMA OPERACAO REAL APROVADA
FRENTE_COMPLEMENTAR_ATIVA: VALIDACAO_MATRIZ_FORCA_ESTADO_TEMPERATURA_JOGO_V1
PROXIMA FRENTE MACRO SUGERIDA: GOLS_1_TEMPO_DISCOVERY_V1
```

O projeto de gols tardios V1 permanece encerrado como pesquisa retrospectiva e prospectiva simulada, com ressalvas estatisticas. A nova frente de forca/estado/temperatura e uma validacao complementar metodologica, nao uma reabertura operacional e nao uma autorizacao de trading.

---

## Governanca obrigatoria

Documento oficial:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central ativa:

```text
Nenhum agente deve concordar com o usuario apenas para agradar.
```

Se uma solicitacao pular etapas, misturar objetivos, fragilizar a metodologia, inflar lucro/ROI/robustez ou gerar falsa confianca operacional, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

---

## Escopo final analisado no encerramento Gols Tardios V1

As execucoes finais foram estruturadas por `season_id`:

```text
Premier League 2024/2025 — season_id 23614
Premier League 2025/2026 — season_id 25583
2. Bundesliga 2024/2025 — season_id 23745
2. Bundesliga 2025/2026 — season_id 25652
```

---

## Ordem final do pipeline de Gols Tardios V1

```text
1. DISCOVERY
2. DRAWDOWN
3. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
4. ANALISE_MATURIDADE_LIGA_POR_RODADA_V1
5. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
6. COMPARACAO_MULTI_LIGA_TEMPORADA_QUALIDADE_E_OSCILACAO_V1
7. ANATOMIA_NUMERICA_DAS_FAMILIAS_APROVADAS_V1
8. SELECAO_DAS_VARIACOES_OFICIAIS_POR_FAMILIA_V1
9. VALIDACAO_OPERACIONAL_FINAL_V1
10. RADAR_PREDITIVO_DE_TEMPORADA_V1 SEM LEAKAGE
11. VALIDACAO_PROSPECTIVA_DO_RADAR_V1
12. AUDITORIA_FINAL_ANTI_LEAKAGE_V1
13. PLAYBOOK_OPERACIONAL_V1
14. ENCERRAMENTO_CIENTIFICO_GOLS_TARDIOS_V1
```

Observacao cientifica:

```text
O Radar Preditivo V1 inicialmente apresentou leakage porque usava post_* na emissao de sinais.
A versao corrigida removeu post_* da tomada de decisao e passou a emitir sinais usando apenas ini_*.
post_* fica restrito a confirmacao posterior retrospectiva.
```

---

## Entregas finais oficiais

```text
VALIDACAO_OPERACIONAL_FINAL_V1
RADAR_PREDITIVO_DE_TEMPORADA_V1
VALIDACAO_PROSPECTIVA_DO_RADAR_V1
AUDITORIA_FINAL_ANTI_LEAKAGE_V1
PLAYBOOK_OPERACIONAL_V1
ENCERRAMENTO_CIENTIFICO_GOLS_TARDIOS_V1
```

Status:

```text
PESQUISA V1 CONCLUIDA COM RESSALVAS ESTATISTICAS
SEM AUTORIZACAO PARA OPERACAO REAL
```

---

## Resultado consolidado por temporada

```text
season_id 23614 — Premier League 24/25
Status: VALIDACAO INCONCLUSIVA
Motivo: sem sinais suficientes na melhor janela.

season_id 25583 — Premier League 25/26
Status: VALIDADO COM BAIXA AMOSTRA
Motivo: sinais iniciais confirmados, mas com volume reduzido.

season_id 23745 — 2. Bundesliga 24/25
Status: VALIDADO COM BAIXA AMOSTRA
Motivo: sinal isolado confirmado.

season_id 25652 — 2. Bundesliga 25/26
Status: VALIDADO COM BAIXA AMOSTRA
Motivo: dois sinais iniciais confirmados, com ressalva de amostra.
```

---

## Principais descobertas consolidadas

```text
1. Os clusters mais relevantes ficaram concentrados em familias No Goal/Under tardias.
2. O padrao recorrente e jogo frio/desacelerado, adversario sem pressao real e baixa criacao ofensiva na reta final.
3. O Radar sem leakage funciona como filtro conservador, nao como aprovador operacional.
4. A validacao prospectiva confirmou sinais em baixa amostra.
5. A auditoria anti-leakage nao encontrou evidencia de leakage critico nos artefatos auditados apos a correcao.
6. As familias possuem sobreposicao relevante e nao devem ter lucros somados como estrategias independentes sem deduplicacao.
```

---

## Familias finais observaveis

Status cientifico final:

```text
OBSERVACAO_PROSPECTIVA / CANDIDATA_COM_RESSALVAS
```

Familias No Goal relevantes:

```text
both_teams_cold_2of3__no_goal
team_winning_by_1_low_dangerous_attacks_against__no_goal
team_winning_by_1_opp_cold_2of3__no_goal
favorite_winning_by_1_opp_cold_2of3__no_goal
team_winning_by_1_no_sot_against__no_goal
opponent_no_recent_key_passes__no_goal
opponent_no_big_chances__no_goal
```

Nenhuma familia esta aprovada para operacao real.

---

## Frente complementar ativa — Forca, Estado e Temperatura do Jogo

Documento de planejamento:

```text
docs/04_RESEARCH/PLANO_ESTUDO_FORCA_ESTADO_TEMPERATURA_JOGO_V1.md
```

Status:

```text
FRENTE_COMPLEMENTAR_ATIVA
PLANEJAMENTO_ESTRUTURADO
NAO OPERACIONAL
NAO INVALIDA O ENCERRAMENTO_CIENTIFICO_GOLS_TARDIOS_V1
```

Tese a validar:

```text
FAVORITO_FORTE/MEDIO + JOGO_QUENTE + ESTADO DO FAVORITO -> Goal
FAVORITO_FRACO/SEM_FAVORITO_CLARO + JOGO_FRIO + ESTADO DO LADO/TIME -> No Goal
```

Cronograma oficial:

```text
1. classificar_contexto_forca_estado_temperatura_v1.py
2. validacao_matriz_forca_estado_temperatura_v1.py
3. analise_familias_blocos_matriz_v1.py
4. analise_mandante_visitante_blocos_v1.py
5. agregar_estudo_forca_estado_temperatura_temporada_v1.py
6. analise_times_blocos_promissores_v1.py, somente depois
7. executar_pipeline_estudo_forca_estado_temperatura_v1.py, somente depois das etapas 1 a 5 validadas
```

Regra metodologica:

```text
primeiro provar o fenomeno macro
depois explicar por familia
depois investigar casa/fora
depois investigar time especifico apenas nos blocos sobreviventes
```

Cashout:

```text
FORA DO ESCOPO DA V1
HOLD COMO BASE PRINCIPAL
```

---

## Politica Oficial de Odds

Todos os resultados financeiros seguem como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

Ressalvas obrigatorias:

```text
Nao constitui backtesting financeiro real.
Nao usa odds live reais por timestamp.
Nao considera liquidez, spread, delay, slippage, suspensao de mercado ou comissao real.
Nao constitui recomendacao de trading.
Nao autoriza operacao real.
```

---

## Decisao Operacional Atual

Nenhuma estrategia, time, perfil de favorito, fase, rodada, filtro, alerta, carteira ou familia esta aprovado para operacao real.

A frente de forca/estado/temperatura e apenas pesquisa complementar com deduplicacao obrigatoria e isolamento por `season_id`.

---

## Proxima frente macro sugerida

```text
GOLS_1_TEMPO_DISCOVERY_V1
```

Status:

```text
SUGERIDO
PAUSADO ENQUANTO A FRENTE COMPLEMENTAR DE FORCA/ESTADO/TEMPERATURA E ESTRUTURADA
DEVE COMECAR DO ZERO NO DISCOVERY QUANDO FOR ABERTO
```

---

## Restricoes permanentes

- Nao criar robo a partir desta pesquisa.
- Nao criar producao operacional.
- Nao chamar simulacao com odds medias de backtesting financeiro real.
- Nao usar odds live inexistentes.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao transformar baixa amostra em robustez.
- Nao comercializar sinais derivados do pipeline.
- Nao generalizar para outras ligas ou mercados sem reexecutar a esteira completa.
- Nao usar time especifico como filtro antes de validar blocos macro.
- Nao transformar melhor cutoff retrospectivo em regra final.
