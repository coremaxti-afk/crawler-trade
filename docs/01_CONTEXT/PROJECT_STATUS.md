# PROJECT STATUS

## Etapas do Projeto

1. Organização
2. Inventário das Fontes
3. Coleta Bruta
4. Banco de Dados
5. Integração Multi-Fonte
6. Catálogo de Features
7. Engenharia de Features
8. Definição do Alvo
9. Dataset Analítico
10. Pesquisa Quantitativa
11. Modelagem
12. Produção

---

## Concluído

- Estrutura documental do projeto consolidada.
- Understat integrado.
- FotMob integrado parcialmente.
- EPL 2024/2025 descoberta via SofaScore (381 partidas).
- Match Mapping criado.
- SofaScore validado como fonte operacional.
- inventory.json gerado.
- rounds.json gerado.
- 50 partidas coletadas com sucesso.
- PostgreSQL configurado.
- SQLAlchemy configurado.
- Tabelas match_mapping, matches_master, match_statistics, match_incidents e match_graph criadas.
- Documentação técnica ampliada e auditada.

---

## Em Andamento

### Coleta SofaScore

Objetivo:

Finalizar a coleta histórica da Premier League.

Status:

- 50 partidas coletadas.
- HTTP 403 identificado após alto volume de requisições.
- Investigação em andamento.

---

### Importação PostgreSQL

Objetivo:

Implementar sofascore_importer.py para popular:

- matches_master
- match_statistics
- match_incidents
- match_graph

Status:

Planejado.

---

## Próximas Etapas

1. Resolver HTTP 403.
2. Finalizar EPL completa.
3. Implementar sofascore_importer.py.
4. Popular PostgreSQL.
5. Consolidar integração multi-fonte.
6. Construir catálogo de features.
7. Gerar dataset analítico.
8. Pesquisa quantitativa.
9. Modelagem preditiva.
10. Backtesting.
11. Produção.

---

## Descobertas Recentes

- Mapeamento Understat → FotMob concluído.
- SofaScore fornece incidents.
- Estrutura para momentum (match_graph) preparada.
- Arquitetura multi-fonte consolidada.
- Coleta histórica SofaScore validada.
- Projeto entrando na fase de engenharia de dados.