# ROADMAP_OPERACIONAL_ATUAL_V1

## Status

```text
GOLS_TARDIOS_V1 ENCERRADO COMO PESQUISA
DECISAO FINAL: PESQUISA V1 CONCLUIDA COM RESSALVAS ESTATISTICAS
PROXIMA FRENTE SUGERIDA: GOLS_1_TEMPO_DISCOVERY_V1
```

Este documento substitui a leitura antiga de pre-ranking. O projeto de gols tardios ja passou por discovery, ranking/selecao, validacao operacional, radar preditivo sem leakage, validacao prospectiva, auditoria anti-leakage, playbook e encerramento cientifico.

---

## Governanca obrigatoria

Antes de executar qualquer nova frente, todos os agentes devem seguir:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central: nenhum agente deve concordar com o usuario apenas para agradar. Se uma solicitacao pular etapas, misturar objetivos, fragilizar a metodologia, inflar lucro/ROI/robustez ou gerar falsa confianca operacional, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

---

## Pipeline final de gols tardios V1

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

---

## Entregas registradas como concluidas

```text
AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
ANALISE_REGIME_POR_FASE_V1
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
COMPARACAO_MULTI_LIGA_TEMPORADA_QUALIDADE_E_OSCILACAO_V1.1
ANATOMIA_NUMERICA_DAS_FAMILIAS_APROVADAS_V1
SELECAO_DAS_VARIACOES_OFICIAIS_POR_FAMILIA_V1
VALIDACAO_OPERACIONAL_FINAL_V1
RADAR_PREDITIVO_DE_TEMPORADA_V1
VALIDACAO_PROSPECTIVA_DO_RADAR_V1
AUDITORIA_FINAL_ANTI_LEAKAGE_V1
PLAYBOOK_OPERACIONAL_V1
GERADOR_PLAYBOOK_OPERACIONAL_V1
ENCERRAMENTO_CIENTIFICO_GOLS_TARDIOS_V1
```

Observacoes:

```text
VALIDACAO_OPERACIONAL_FINAL_V1_1 foi auditoria/correcao documental historica.
RADAR_PREDITIVO_DE_TEMPORADA_V1 anterior com leakage foi substituido pela versao corrigida sem post_* na emissao de sinais.
VALIDACAO_PROSPECTIVA_DO_RADAR_V1 foi reexecutada apos correcao anti-leakage.
```

---

## Resultado consolidado da pesquisa V1

```text
Status cientifico: PESQUISA V1 CONCLUIDA COM RESSALVAS ESTATISTICAS
Status anti-leakage: SEM EVIDENCIA DE LEAKAGE CRITICO NOS ARTEFATOS AUDITADOS
Status operacional: NENHUMA OPERACAO REAL APROVADA
```

Escopo final por `season_id`:

```text
23614 — Premier League 2024/25 — validacao inconclusiva por ausencia de sinais suficientes
25583 — Premier League 2025/26 — validado com baixa amostra
23745 — 2. Bundesliga 2024/25 — validado com baixa amostra
25652 — 2. Bundesliga 2025/26 — validado com baixa amostra
```

---

## Familias finais observaveis

As familias finais permanecem apenas como observacao cientifica ou candidatas com ressalvas:

```text
both_teams_cold_2of3__no_goal
team_winning_by_1_low_dangerous_attacks_against__no_goal
team_winning_by_1_opp_cold_2of3__no_goal
favorite_winning_by_1_opp_cold_2of3__no_goal
team_winning_by_1_no_sot_against__no_goal
opponent_no_recent_key_passes__no_goal
opponent_no_big_chances__no_goal
```

Status permitido:

```text
OBSERVACAO_PROSPECTIVA
CANDIDATA_COM_RESSALVAS
CANDIDATA_FRACA_POR_BAIXO_ROI
```

Status proibido:

```text
APROVADA_PARA_OPERAR
```

---

## Regra final sobre odds e resultado financeiro

Todos os resultados com odds medias devem permanecer rotulados como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

Nao usar:

```text
BACKTESTING FINANCEIRO REAL
ODDS LIVE REAIS
SISTEMA LUCRATIVO VALIDADO
OPERACAO APROVADA
```

---

## Pos-pesquisa de gols tardios

Apos o encerramento cientifico, o unico caminho aceitavel para gols tardios seria uma fase futura separada de:

```text
MONITORAMENTO_PROSPECTIVO_SEM_DINHEIRO_REAL
```

Status:

```text
NAO INICIADO
NAO OBRIGATORIO
NAO DEVE BLOQUEAR NOVOS PROJETOS
```

---

## Proxima frente sugerida

```text
GOLS_1_TEMPO_DISCOVERY_V1
```

Objetivo inicial sugerido:

```text
Iniciar pesquisa exploratoria do zero para gols no 1º tempo, reaproveitando a esteira metodologica de separacao temporal e anti-leakage, mas sem carregar familias, filtros ou conclusoes de gols tardios.
```

---

## Ideias futuras — nao aprovadas ainda

```text
MONITORAMENTO_PROSPECTIVO_GOLS_TARDIOS_SEM_DINHEIRO_REAL
DASHBOARD_DE_OBSERVACAO_PROSPECTIVA
ALERTAS_INFORMATIVOS_SEM_EXECUCAO
PADROES_MACRO_OPERACIONAIS_V1
```

Status:

```text
HIPOTESES FUTURAS
NAO EXECUTAR AGORA SEM SOLICITACAO EXPLICITA
```

---

## Regra final

Nenhuma estrategia, filtro, perfil de time, contexto de favorito, rodada ou fase deve entrar como regra operacional definitiva.

O projeto de gols tardios V1 esta encerrado como pesquisa. Qualquer novo mercado deve recomecar no Discovery.
