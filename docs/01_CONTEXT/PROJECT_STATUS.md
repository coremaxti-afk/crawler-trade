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
- Documento base de hipoteses criado em `docs/04_RESEARCH/ACTIVE/LATE_GOAL_HYPOTHESES.md`.
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
- Validacao leve de qualidade concluida com status: APTO COM RESSALVAS.
- Desenho metodologico do Dataset Analitico v1 definido em `docs/04_RESEARCH/ANALYTICAL_DATASET_V1.md`.

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

- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.
- Registros para `12436452`: 0.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.
- Partidas importadas sem estatisticas: 0.

Fora do escopo desta importacao:

- `match_graph`
- lineups
- h2h
- features
- modelagem

---

## Validacao Leve de Qualidade

Status:

- APTO COM RESSALVAS.

Resultados:

- Nao existem orfaos.
- Nao existem divergencias entre placar e incidentes.
- 16 partidas sem gols sao compativeis com o placar.
- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.

Interpretacao:

- A base esta apta para desenho metodologico do Dataset Analitico v1.
- As colunas `big_chances_home` e `big_chances_away` devem ser tratadas com ressalva e nao devem ser usadas como feature obrigatoria sem regra documentada de nulos.
- `match_graph`, lineups e h2h permanecem fora do core v1.

---

## Em Andamento

### Dataset Analitico v1

Objetivo:

Definir o desenho metodologico do Dataset Analitico v1 antes de criar codigo, features ou modelos.

Status:

- Desenho metodologico definido.
- Nenhum codigo criado nesta etapa.
- Nenhum modelo criado nesta etapa.
- Feature engineering ainda nao iniciada.

Documento:

- `docs/04_RESEARCH/ANALYTICAL_DATASET_V1.md`

---

### API-Football

Objetivo:

Avaliar como fonte alternativa/complementar ao SofaScore.

Status:

- Spikes controlados executados.
- API-Football permanece como complemento candidato, nao como substituta oficial do SofaScore.

---

## Proximas Etapas

1. PM registrar conclusao da validacao leve e transicao para Dataset Analitico v1.
2. Quant Research revisar o desenho metodologico do Dataset Analitico v1.
3. CTO avaliar se o desenho exige impacto estrutural antes de qualquer implementacao.
4. Codex somente deve ser acionado quando houver tarefa pequena, aprovada e com criterios de aceite.
5. Construir catalogo de features sem usar dados futuros.
6. Gerar Dataset Analitico v1 somente apos aprovacao metodologica.
7. Validar H1-H9 na ordem recomendada.
8. Iniciar modelagem apenas depois de dataset validado.
9. Backtesting apenas depois de baseline validado.
10. Producao apenas em etapa futura.

---

## Descobertas Recentes

- SofaScore fornece dados suficientes para base core EPL em 380 partidas.
- Perfil core reduziu volume de requests e funcionou operacionalmente via 5G.
- A partida `12436452` deve permanecer fora da importacao atual.
- Importer SofaScore core e retomavel/idempotente.
- Base PostgreSQL esta apta com ressalvas para desenho do Dataset Analitico v1.
- `big_chances_home` e `big_chances_away` possuem 7 nulos cada.
- `match_graph` segue pendente porque ainda nao ha `graph.json` coletado.
- Lineups e h2h permanecem complementares, fora do core v1.
