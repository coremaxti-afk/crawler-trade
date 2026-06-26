# ENCERRAMENTO CIENTIFICO — PIPELINE DE GOLS TARDIOS V1

**Rotulo Mandatorio:** ESTIMATIVA OPERACIONAL COM ODDS MEDIAS  
**Data do Relatorio:** 2026-06-26  
**Decisao Cientifica Final:** PESQUISA V1 CONCLUIDA COM RESSALVAS ESTATISTICAS

> [!WARNING]
> **AVISO DE LEITURA CAUTELOSA E OPERACIONAL:**
> Os resultados e simulacoes apresentados neste documento constituem simulacoes retrospectivas sob premissas teoricas.
> - Nao constitui recomendacao de trading ou aposta esportiva.
> - Nao autoriza operacao real com capital financeiro.
> - Nao utiliza odds reais em tempo real com timestamps exatos de mercado.
> - Nao considera liquidez, spread, delay de sinal, slippage, suspensao temporaria de mercado ou comissao real.

---

## 1. Resumo executivo

O projeto de Gols Tardios V1 esta cientificamente concluido como pesquisa retrospectiva e prospectiva simulada. Nao ha evidencia de leakage temporal critico nos artefatos auditados apos as correcoes metodologicas aplicadas na classificacao de sinais do Radar Preditivo.

A versao corrigida do Radar Preditivo e da Validacao Prospectiva foi executada com barreira temporal explicita: o Radar emite sinais apenas com metricas iniciais (`ini_*`) e a confirmacao posterior usa metricas `post_*` apenas para avaliacao retrospectiva.

O projeto permanece sem autorizacao para operacao real. Sua utilidade pratica esta na esteira metodologica, na auditoria anti-leakage e na arquitetura reaproveitavel para novos estudos quantitativos.

---

## 2. Objetivo original do projeto

O projeto foi concebido para:

1. Identificar padroes recorrentes de gols tardios ou ausencia de gols tardios em mercados live.
2. Agrupar variacoes em familias logicas de comportamento semelhante.
3. Avaliar estabilidade temporal entre ligas e temporadas.
4. Testar se metricas acumuladas em rodadas iniciais poderiam antecipar o desempenho posterior da temporada.
5. Gerar uma esteira replicavel de triagem, validacao, auditoria e documentacao.

---

## 3. Escopo final analisado

O escopo final foi estruturado exclusivamente por `season_id`:

```text
23614 — Premier League 2024/2025
25583 — Premier League 2025/2026
23745 — 2. Bundesliga 2024/2025
25652 — 2. Bundesliga 2025/2026
```

---

## 4. Matriz de artefatos finais por temporada

| season_id | Liga / Temporada | Radar MD | Radar CSVs | Validacao Prosp. MD | Validacao Prosp. CSVs | Auditoria Anti-Leakage | Playbook | Status Artefatos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23614 | Premier League 24/25 | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO |
| 25583 | Premier League 25/26 | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO |
| 23745 | 2. Bundesliga 24/25 | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO |
| 25652 | 2. Bundesliga 25/26 | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO | COMPLETO |

---

## 5. Pipeline final consolidado

```text
1. Discovery
2. Drawdown
3. Agrupamento por familias e variacoes
4. Maturidade de liga por rodada
5. Forca do favorito por estrategia
6. Comparacao multi-liga/temporada
7. Anatomia numerica das familias
8. Selecao das variacoes oficiais
9. Validacao Operacional Final V1
10. Radar Preditivo de Temporada V1 sem leakage
11. Validacao Prospectiva do Radar V1
12. Auditoria Final Anti-Leakage V1
13. Playbook Operacional V1
14. Encerramento Cientifico
```

---

## 6. Scripts oficiais da pesquisa V1

| Script / Componente | Funcao | Status | Observacao |
| --- | --- | --- | --- |
| `pipeline_temporada_completa_v1.py` | Pipeline de Discovery | OFICIAL | Base de mineracao original |
| `run_strategy_drawdown.py` | Calculo de drawdown | OFICIAL | Mapeamento de risco |
| `run_agrupamento_por_familia_e_variacoes_v1.py` | Agrupamento logico | OFICIAL | Organiza variacoes por familia |
| `run_analise_maturidade_liga_por_rodada_v1.py` | Maturidade temporal | AUXILIAR | Suporte metodologico |
| `run_analise_forca_favorito_por_estrategia_v1.py` | Favoritos | AUXILIAR | Contexto, nao filtro automatico |
| `comparacao_multi_liga_temporada_qualidade_e_oscilacao_v1.py` | Comparacao temporal | AUXILIAR | Estabilidade entre temporadas |
| `validacao_operacional_final_v1.py` | Triagem operacional simulada | OFICIAL | Nao aprova operacao real |
| `radar_preditivo_de_temporada_v1.py` | Emissao de sinais sem leakage | OFICIAL | Usa apenas `ini_*` para sinal inicial |
| `validacao_prospectiva_do_radar_v1.py` | Validacao prospectiva simulada | OFICIAL | Mede `W+1` ate fim |
| `run_auditoria_final_anti_leakage_v1.py` | Auditoria anti-leakage | OFICIAL | Verifica barreira temporal |
| `gerador_playbook_operacional_v1.py` | Playbook | OFICIAL | Consolida diretrizes de observacao |

---

## 7. Resultado consolidado por temporada

| season_id | Liga / Temporada | Melhor Janela Radar | Sinais Emitidos | Confirmados | Falsos Positivos | Inconclusivos | Assertividade Prospectiva | ROI Radar | ROI Baseline | Lucro Radar | Lucro Baseline | Status Temporada | Observacao |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 23614 | Premier League 24/25 | Rodada 5 | 0 | 0 | 0 | 0 | NA | 0,0% | 7,2% | 0,00 | 3.906,31 | VALIDACAO INCONCLUSIVA | Sem sinais suficientes na janela inicial. |
| 25583 | Premier League 25/26 | Rodada 5 | 2 | 2 | 0 | 0 | 100,0% | 10,0% | 9,7% | 2.059,25 | 4.448,51 | VALIDADO COM BAIXA AMOSTRA | Sinais confirmados, volume baixo. |
| 23745 | 2. Bundesliga 24/25 | Rodada 8 | 1 | 1 | 0 | 0 | 100,0% | 8,1% | 8,7% | 380,00 | 2.490,44 | VALIDADO COM BAIXA AMOSTRA | Sinal isolado confirmado. |
| 25652 | 2. Bundesliga 25/26 | Rodada 5 | 2 | 2 | 0 | 0 | 100,0% | 11,5% | 9,3% | 1.929,55 | 3.419,77 | VALIDADO COM BAIXA AMOSTRA | Dois sinais confirmados, volume baixo. |

---

## 8. Principais descobertas

- Os padroes mais relevantes ficaram concentrados em familias No Goal/Under tardias.
- O cluster recorrente envolve desaceleracao do jogo, adversario sem pressao real e baixa criacao ofensiva na reta final.
- O Radar anterior apresentou leakage ao usar `post_*` na emissao de sinais; a versao corrigida removeu esse problema.
- A assertividade perfeita inicial desaparece quando o fluxo e auditado corretamente em algumas janelas, mostrando comportamento mais realista.
- Ha sobreposicao relevante entre familias. Lucros nao devem ser somados como se as familias fossem independentes.

---

## 9. Familias finais observaveis

| Familia | Direcao | Status final | Evidencia consolidada | Temporadas/season_id com sinal | Risco principal | Proxima acao |
| --- | --- | --- | --- | --- | --- | --- |
| `both_teams_cold_2of3__no_goal` | Under | OBSERVACAO_PROSPECTIVA | ROI alto em amostras reduzidas | 25583, 23745, 25652 | Amostra reduzida | Simulacao cega de longo prazo |
| `team_winning_by_1_low_dangerous_attacks_against__no_goal` | Under | OBSERVACAO_PROSPECTIVA | ROI positivo, mas sensivel a odds | 25583, 25652 | Decaimento de EV | Monitorar sem operar |
| `team_winning_by_1_opp_cold_2of3__no_goal` | Under | OBSERVACAO_PROSPECTIVA | Boa recorrencia, oscilacao por liga | 25583, 25652 | Oscilacao | Deduplicar com familias proximas |
| `favorite_winning_by_1_opp_cold_2of3__no_goal` | Under | OBSERVACAO_PROSPECTIVA | Sinal dependente de contexto de favorito | 25583, 25652 | Reversao a media | Monitorar drawdown |
| `team_winning_by_1_no_sot_against__no_goal` | Under | CANDIDATA_COM_RESSALVAS | N maior e ROI positivo moderado | 25583, 25652 | Drawdown historico | Monitoramento de limite de risco |
| `opponent_no_recent_key_passes__no_goal` | Under | CANDIDATA_COM_RESSALVAS | ROI positivo, instabilidade temporal | 25583, 25652 | Instabilidade | Revalidar em novas temporadas |
| `opponent_no_big_chances__no_goal` | Under | CANDIDATA_FRACA_POR_BAIXO_ROI | N alto, ROI baixo | 25583, 25652 | ROI baixo sob odds reais | Excluir de carteiras ativas |

Nenhuma familia esta aprovada para operacao real.

---

## 10. Familias rejeitadas ou inconclusivas

Estrategias estritamente Over/Goal tardio ativo foram rejeitadas ou mantidas apenas como historico por:

1. Instabilidade temporal.
2. Drawdown severo.
3. Baixo N em filtros muito restritivos.
4. Dependencia excessiva de regime/fase.
5. Ausencia de validacao prospectiva suficiente.

---

## 11. Resultado do Radar Preditivo sem leakage

Status:

```text
RADAR SEM EVIDENCIA DE LEAKAGE CRITICO APOS CORRECAO
```

Regra final:

```text
Sinal inicial: apenas ini_*
Confirmacao posterior: apenas post_* em avaliacao retrospectiva
```

O Radar deve ser lido como filtro conservador de observacao, nao como aprovador operacional.

---

## 12. Resultado da Validacao Prospectiva

A Validacao Prospectiva confirmou sinais em baixa amostra nas temporadas em que o Radar emitiu sinais suficientes.

Leitura consolidada:

- Premier League 24/25: inconclusiva por ausencia de sinais suficientes.
- Premier League 25/26: validada com baixa amostra.
- 2. Bundesliga 24/25: validada com baixa amostra.
- 2. Bundesliga 25/26: validada com baixa amostra.

O Radar mostrou valor informacional como filtro conservador, mas reduz lucro absoluto quando comparado a carteiras completas e deixa familias lucrativas fora por N inicial baixo.

---

## 13. Resultado da Auditoria Anti-Leakage

Status final:

```text
SEM EVIDENCIA DE LEAKAGE CRITICO NOS ARTEFATOS AUDITADOS
```

Ressalva:

```text
A auditoria foi estatica e programatica, baseada nos scripts e CSVs gerados localmente.
Ela nao valida odds live reais por timestamp, execucao em mercado, liquidez, spread ou slippage.
```

---

## 14. Limitacoes estatisticas

- Baixa amostra nas primeiras janelas.
- Poucas temporadas auditadas.
- Sensibilidade aos thresholds de `ini_ROI`, `ini_EV` e `ini_N`.
- Sobrevivencia por selecao.
- Sobreposicao entre familias.
- Instabilidade de regimes de liga.
- Resultados retrospectivos podem nao se repetir.

---

## 15. Limitacoes operacionais

- Nao usa odds live reais por timestamp.
- Nao considera liquidez.
- Nao considera spread.
- Nao considera delay.
- Nao considera slippage.
- Nao considera suspensao de mercado.
- Nao considera comissao real.
- Nao constitui recomendacao de trading.
- Nao autoriza operacao real.

---

## 16. O que NAO foi aprovado

- Operacao em contas reais.
- Robo automatico.
- Comercializacao de sinais.
- Generalizacao para ligas nao auditadas.
- Soma de lucros de familias sobrepostas como se fossem independentes.
- Uso em mercados diferentes sem novo Discovery.

---

## 17. O que pode ser reaproveitado

- Esteira de separacao temporal.
- Auditoria anti-leakage.
- Validacao prospectiva por `season_id`.
- Drawdown e controle de risco simulado.
- Estrutura de documentacao por artefatos.
- Pipeline como base para novos estudos, desde que cada novo mercado comece no Discovery.

---

## 18. Como usar o projeto no futuro

Processo cientifico recomendado para futuras temporadas:

```text
1. Definir season_id
2. Rodar Discovery e Drawdown
3. Agrupar familias e selecionar variacoes
4. Executar Validacao Operacional Final
5. Rodar Radar sem leakage com ini_*
6. Executar Validacao Prospectiva com post_*
7. Rodar Auditoria Anti-Leakage
8. Gerar Playbook de observacao
9. Atualizar documentacao de encerramento ou nova versao de pesquisa
```

---

## 19. Decisao cientifica final

```text
PESQUISA V1 CONCLUIDA COM RESSALVAS ESTATISTICAS
```

O projeto demonstrou consistencia estrutural nos artefatos auditados, remocao de leakage critico apos correcao e validacao prospectiva simulada com baixa amostra. Permanece como estudo metodologicamente auditado nos artefatos disponiveis, sem qualquer autorizacao de transicao para operacao real.

---

## 20. Proximos projetos sugeridos

```text
GOLS_1_TEMPO_DISCOVERY_V1
```

Objetivo sugerido:

```text
Iniciar uma pesquisa exploratoria do zero para gols no 1º tempo, reaproveitando a esteira anti-leakage e de validacao temporal, sem carregar filtros, familias ou conclusoes de gols tardios.
```
