# Codebase Documentation

Esta pasta contém a documentação técnica dos scripts do projeto LateGoalResearch.

## Objetivos

- Catalogar todos os scripts do projeto.
- Registrar responsabilidades, entradas e saídas.
- Facilitar manutenção futura por humanos e agentes de IA.
- Servir como referência para futuras integrações com agentes e automações.

## Estrutura Atual

- FILE_INDEX.md -> índice geral dos arquivos.
- FILE_CATALOG.md -> catálogo dos componentes documentados.
- collectors/ -> coletores Understat, SofaScore e futuros importadores.
- config/ -> configuração compartilhada do projeto.
- analytics/ -> rotinas analíticas e geração de datasets.

## Componentes Principais

### Collectors

- sofascore_client
- sofascore_collector
- sofascore_season_collector
- sofascore_match_collector
- sofascore_importer (planejado)

### Config

- database.py

## Status

Documentação ativa e em expansão conforme novos componentes são adicionados ao projeto.