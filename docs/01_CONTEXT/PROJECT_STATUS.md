# PROJECT STATUS

## Etapas do Projeto

1. Organizacao
2. Inventario das Fontes
3. Coleta Bruta
4. Banco de Dados
5. Integracao Multi-Fonte
6. Catalogo de Features
7. Engenharia de Features
8. Definicao do Alvo
9. Dataset Analitico
10. Pesquisa Quantitativa
11. Modelagem
12. Producao

---

## Concluido

- Estrutura documental do projeto consolidada.
- Governanca de agentes criada em `docs/00_AGENTS/AGENT_COORDINATION.md`.
- Perfil do PM criado em `docs/00_AGENTS/PM_PROFILE.md`.
- Documento base de hipoteses criado em `docs/04_RESEARCH/LATE_GOAL_HYPOTHESES.md`.
- Understat integrado.
- FotMob integrado parcialmente.
- EPL 2024/2025 descoberta via SofaScore com 381 partidas no inventory.
- Match Mapping criado.
- PostgreSQL configurado.
- SQLAlchemy configurado.
- Tabelas `match_mapping`, `matches_master`, `match_statistics`, `match_incidents` e `match_graph` criadas.
- Coletor SofaScore v2 endurecido operacionalmente no commit `54bbb14`.
- Coletor SofaScore v3 core criado para reduzir volume de requests.
- Coleta SofaScore validada via 5G sem novo HTTP 403 em mais de 100 partidas.
- Auditoria local SofaScore EPL concluida.
- `sofascore_importer.py` implementado no commit `84e641f`.
- PostgreSQL populado com 380 partidas SofaScore importaveis.
- Idempotencia do importer validada com segunda execucao sem duplicacao.

---

## Estado Atual da Coleta SofaScore

Resultado auditado:

- Total no inventory: 381 partidas.
- Total de pastas locais: 381.
- Partidas full: 192.
- Partidas core: 188.
- Total importavel: 380.
- Partidas faltantes: 0.
- Partidas incompletas relevantes: 1.
- Partida descartada da importacao atual: `12436452`.

Observacoes:

- A partida `12436449` foi corrigida/coletada e entrou como importavel.
- `lineups.json` e `h2h.json` permanecem preservados como dados brutos complementares.
- A estrategia core reduziu o volume de requests por partida de 5 para 3.

---

## Estado Atual da Importacao PostgreSQL

Tabelas populadas nesta etapa:

- `matches_master`
- `match_statistics`
- `match_incidents`

Contagens finais:

- `matches_master`: 380 eventos distintos.
- `match_statistics`: 380 eventos distintos.
- `match_incidents`: 7647 registros, cobrindo 380 eventos.
- Registros para `12436452`: 0.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.
- Partidas importadas sem estatisticas: 0.

Fora do escopo desta importacao:

- `match_graph`
- lineups
- h2h
- features
- dataset analitico
- modelagem

---

## Em Andamento

### Validacao de Dados Importados

Objetivo:

Validar qualidade, consistencia e completude dos dados SofaScore importados.

Pontos iniciais:

- Conferir amostras em `matches_master`.
- Validar campos principais de `match_statistics`.
- Validar gols, cartoes, substituicoes e eventos de periodo em `match_incidents`.
- Confirmar que dados core sao suficientes para a proxima etapa autorizada.

---

### API-Football

Objetivo:

Avaliar como fonte alternativa/complementar ao SofaScore.

Status:

- Spikes controlados executados.
- API-Football permanece como complemento candidato, nao como substituta oficial do SofaScore.

---

## Proximas Etapas

1. Validar amostras importadas no PostgreSQL.
2. Revisar qualidade de `match_statistics` e `match_incidents`.
3. CTO/Data Engineer decidir proxima frente: graph, importacao complementar ou catalogo de features.
4. Implementar coleta/importacao de graph apenas se aprovada.
5. Consolidar integracao multi-fonte.
6. Construir catalogo de features.
7. Gerar dataset analitico.
8. Pesquisa quantitativa.
9. Modelagem preditiva.
10. Backtesting.
11. Producao.

---

## Descobertas Recentes

- SofaScore fornece dados suficientes para base core EPL em 380 partidas.
- Perfil core reduziu volume de requests e funcionou operacionalmente via 5G.
- A partida `12436452` deve permanecer fora da importacao atual.
- Importer SofaScore core e retomavel/idempotente.
- `match_graph` segue pendente porque ainda nao ha `graph.json` coletado.
