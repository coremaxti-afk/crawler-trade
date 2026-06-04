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
- Governança de agentes criada em `docs/00_AGENTS/AGENT_COORDINATION.md`.
- Perfil do PM criado em `docs/00_AGENTS/PM_PROFILE.md`.
- Documento base de hipóteses criado em `docs/04_RESEARCH/LATE_GOAL_HYPOTHESES.md`.
- Understat integrado.
- FotMob integrado parcialmente.
- EPL 2024/2025 descoberta via SofaScore (381 partidas).
- Match Mapping criado.
- SofaScore validado como fonte operacional em nível de collector.
- inventory.json gerado.
- rounds.json gerado.
- 50 partidas coletadas com sucesso.
- PostgreSQL configurado.
- SQLAlchemy configurado.
- Tabelas match_mapping, matches_master, match_statistics, match_incidents e match_graph criadas.
- Correção operacional do coletor SofaScore v2 implementada no commit `54bbb14`.
- Teste controlado confirmou que o coletor v2 registra HTTP 403 e encerra o lote com segurança.

---

## Em Andamento

### Coleta SofaScore

Objetivo:

Finalizar a coleta histórica da Premier League.

Status:

- 50 partidas coletadas.
- HTTP 403 identificado após alto volume de requisições.
- Correção operacional do coletor v2 implementada e revisada.
- Na retomada da partida 51, o HTTP 403 persistiu.
- A coleta massiva está pausada até nova decisão operacional.

Decisão pendente:

- Avaliar com Data Acquisition Engineer e CTO se a coleta deve seguir em perfil core, com apenas 3 JSONs principais por partida:
  - `event.json`
  - `statistics.json`
  - `incidents.json`

Observação:

- `lineups.json` e `h2h.json` seguem como dados complementares e não devem ser removidos da arquitetura.

---

### Coleta Minuto a Minuto / Graph

Status:

- Ainda não implementada.

Observação:

- `incidents.json` possui eventos com minuto, mas não representa série temporal minuto a minuto completa.
- Para momentum/pressão temporal, será necessário coletar `graph.json` ou endpoint equivalente.
- Se o graph for um endpoint por partida, a estimativa inicial é de 1 request adicional por partida.

---

### API-Football

Objetivo:

Avaliar como fonte alternativa/complementar ao SofaScore.

Status:

- Em avaliação.

Premissa operacional:

- Plano gratuito possui limite de 100 requests/dia.
- Deve ser tratado como spike pequeno, não substituição imediata de fonte.

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

Observação:

- Pode ser considerado iniciar importer com as 50 partidas já coletadas, caso PM/CTO aprovem mudar temporariamente de frente enquanto a coleta SofaScore permanece bloqueada.

---

## Próximas Etapas

1. Data Acquisition Engineer avaliar coleta core de 3 JSONs por partida.
2. CTO aprovar ou rejeitar mudança operacional para perfil core.
3. Decidir se SofaScore permanece pausado ou se haverá novo teste com menor volume.
4. Avaliar spike API-Football como fonte complementar.
5. Considerar iniciar Data Engineer / Database com as 50 partidas já coletadas.
6. Implementar sofascore_importer.py.
7. Popular PostgreSQL.
8. Consolidar integração multi-fonte.
9. Construir catálogo de features.
10. Gerar dataset analítico.
11. Pesquisa quantitativa.
12. Modelagem preditiva.
13. Backtesting.
14. Produção.

---

## Descobertas Recentes

- Mapeamento Understat → FotMob concluído.
- SofaScore fornece incidents.
- Estrutura para momentum (match_graph) preparada.
- Arquitetura multi-fonte consolidada.
- Coleta histórica SofaScore validada em amostra inicial.
- HTTP 403 persistiu mesmo após correção operacional e teste controlado.
- Reduzir coleta para perfil core pode diminuir requests por partida de 5 para 3.
- Projeto pode avançar parcialmente para engenharia de dados com as 50 partidas já coletadas.
- `docs/04_RESEARCH/LATE_GOAL_HYPOTHESES.md` foi criado para estabilizar H1-H9.
