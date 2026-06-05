# AGENT MASTER

## Objetivo

Late Goal Research é um projeto de pesquisa quantitativa para identificar padrões associados a gols tardios no futebol através da integração de múltiplas fontes de dados.

## Governança

Documento oficial:

- docs/00_AGENTS/GOVERNANCE_V2.md

Princípios:

- Chat = Comunicação Executiva
- GitHub = Fonte Oficial da Verdade
- Em caso de conflito, GitHub prevalece

Todos os agentes devem seguir a GOVERNANCE_V2 enquanto ela estiver ativa.

## Fontes Principais

1. Understat
2. SofaScore

## Fontes Secundárias

1. FotMob
2. OddsPortal

## Ordem de Leitura para Novos Agentes

1. docs/00_AGENTS/AGENT_MASTER.md
2. docs/01_CONTEXT/PROJECT_STATE_2026-06.md
3. docs/01_CONTEXT/PROJECT_STATUS.md
4. docs/06_SPRINTS/CURRENT_SPRINT.md
5. Documentação específica da área de atuação

## Regras

- Não repetir pesquisas já concluídas.
- Registrar novas descobertas.
- Priorizar evolução do dataset.
- Evitar dependência de uma única fonte.
- Consultar a documentação antes de propor mudanças estruturais.

## Estado Atual do Projeto

Concluído:

- PostgreSQL operacional.
- Understat operacional.
- SofaScore Season Collector implementado.
- SofaScore Match Collector implementado.
- 50 partidas da EPL coletadas.
- Documentação consolidada.

Em andamento:

- Investigação do HTTP 403 do SofaScore.
- Finalização da coleta histórica da EPL.

Próximos marcos:

- Implementar sofascore_importer.py.
- Popular PostgreSQL.
- Construir features H1-H9.
- Iniciar pesquisa quantitativa avançada.

## Objetivo Imediato

Concluir a transição da fase de coleta para a fase de engenharia de dados.