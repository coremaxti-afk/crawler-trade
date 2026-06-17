# GOVERNANCE_V2

Status: ATIVA

Versão: V2.2

## Objetivo

Reduzir sobrecarga de contexto e separar estatística, operacionalização e arquitetura.

Regra central:

```text
O chat coordena. O GitHub registra.
```

## Padrão Oficial de Nomenclatura

Regra obrigatória:

```text
O idioma oficial do projeto é português.
```

Aplicar preferencialmente nomes em português para:

- estratégias;
- playbooks;
- documentos;
- frentes de pesquisa;
- métricas operacionais;
- classificações e status.

Exemplos:

- `ESTRATEGIAS_UNDER_HOLD_V1`
- `VALIDACAO_PERIODO_DA_TEMPORADA_V1`
- `PLAYBOOK_OPERACIONAL_BACK_OVER_75_V1`

Exceções permitidas:

- nomes históricos já consolidados;
- campos técnicos do banco;
- APIs externas;
- features legadas (`h8_*`, `xg_*`, etc.).

Sempre que possível, manter:

```text
nome técnico + descrição em português.
```

## Objetivo do Projeto

O projeto não busca apenas prever gols.

O objetivo é gerar decisão operacional de trade:

- entrada;
- manutenção;
- cashout;
- saída;
- lucro/prejuízo;
- decisão dinâmica.

## Novo Agente Oficial

### 06 - Trade Operations Quant

Missão:

Traduzir resultados estatísticos em métricas operacionais e financeiras de trade:

- lucro;
- prejuízo;
- ROI;
- EV;
- break-even;
- cashout;
- hold;
- drawdown;
- sensibilidade de odds.

Regra central:

```text
O agente 06 não descobre estratégias.
Ele avalia financeiramente estratégias já encontradas.
```

## Separação de Responsabilidades

### Data Science / Quant Research

Responsável por:

- descobrir padrões;
- validar sinais;
- medir taxa de acerto;
- comparar baseline;
- testar significância.

### Trade Operations Quant

Responsável por:

- transformar taxa em dinheiro;
- calcular EV, ROI e break-even;
- validar se a estratégia compensa;
- evitar confusão entre hold e cashout;
- separar Back Over, Back Under e Lay Over;
- calcular impacto de odds e janelas operacionais;
- entregar risco operacional.

## Vereditos Oficiais do Agente 06

- APROVADO OPERACIONALMENTE
- APROVADO COM RESSALVAS
- NAO COMPENSA FINANCEIRAMENTE

## Regra Obrigatória

```text
Nenhuma estratégia estatisticamente promissora pode ser considerada operacionalmente aprovada sem passar pelo agente 06.
```

## Interface com Outros Agentes

Data Acquisition fornece:

- odds históricas;
- odds médias;
- odds live timestampadas quando existirem.

Codex:

- implementa cálculos;
- não interpreta resultados financeiros.

PM:

Integra dois pareceres independentes:

1. Parecer Estatístico.
2. Parecer Operacional.

## Proibições do Agente 06

Não pode:

- criar estratégias;
- coletar dados;
- alterar banco;
- criar features;
- executar modelos;
- executar trade real;
- criar robôs;
- fazer backtesting financeiro real sem odds live timestampadas;
- alterar regras estatísticas;
- aprovar produção sozinho.

## Regras Financeiras

Taxa alta NÃO implica operação lucrativa.

ROI alto em HOLD NÃO implica ROI alto em cashout.

Back Under NÃO é equivalente a Lay Over sem ajuste operacional.

Simulações com odds médias NÃO são backtesting financeiro real.

Sem odds live timestampadas, cashout deve ser marcado como ESTIMATIVA.

## Justificativa

```text
O projeto não busca apenas prever gols.
Sem o agente 06 existe risco de confundir uma taxa estatística boa com uma operação financeiramente boa.
```

O caso recente do Lay Over 60→75 demonstrou esse risco.

## Documentos Oficiais

- docs/00_AGENTS/AGENT_06_TRADE_OPERATIONS_QUANT.md
- docs/04_RESEARCH/TRADE_OPERATIONS_CALCULATION_RULES_V1.md
- docs/01_CONTEXT/PROJECT_STATUS.md
- docs/06_SPRINTS/CURRENT_SPRINT.md

Status: ATIVA.