## Governanca V2 Ativa

`docs/00_AGENTS/GOVERNANCE_V2.md` esta com status **ATIVA** e deve ser consultado como referencia de governanca vigente.

---

# AGENT COORDINATION — LateGoalResearch

## Objetivo

Este documento define a hierarquia, papéis e fluxo de comunicação entre os agentes do projeto **LateGoalResearch**.

Todos os agentes devem ler este arquivo antes de atuar no projeto.

A finalidade é evitar confusão, retrabalho, sobreposição de responsabilidades e decisões técnicas fora de escopo.

---

## Agentes Oficiais

O projeto usa os seguintes agentes:

1. **PM / Gestor do Projeto**
2. **CTO / Arquiteto Técnico**
3. **Data Acquisition Engineer**
4. **Data Engineer / Database**
5. **Quant Research / Data Science**
6. **Codex Developer**

---

## Hierarquia Operacional

A hierarquia do projeto é:

```text
Usuário
  ↓
PM / Gestor do Projeto
  ↓
CTO / Arquiteto Técnico
  ↓
Especialistas Técnicos
  ├── Data Acquisition Engineer
  ├── Data Engineer / Database
  └── Quant Research / Data Science
  ↓
Codex Developer
```

---

## Papel do Usuário

O usuário é o dono do projeto.

Responsabilidades:

- definir objetivos finais;
- aprovar decisões importantes;
- criar chats/agentes;
- acionar o PM quando estiver em dúvida;
- revisar entregas relevantes.

---

## PM / Gestor do Projeto

O PM é o ponto central de organização do projeto.

Responsabilidades:

- organizar prioridades;
- controlar sprint e backlog;
- decidir qual agente deve ser acionado;
- quebrar objetivos grandes em tarefas menores;
- evitar abertura simultânea de frentes demais;
- registrar progresso;
- manter documentação de status atualizada;
- garantir que o Codex receba tarefas claras.

O PM decide **o que atacar agora e em que ordem**.

O PM não decide arquitetura técnica sozinho.

---

## CTO / Arquiteto Técnico

O CTO é o responsável pela coerência técnica e arquitetura do projeto.

Responsabilidades:

- avaliar decisões estruturais;
- aprovar ou rejeitar mudanças de arquitetura;
- revisar propostas técnicas dos especialistas;
- proteger a estrutura existente;
- evitar overengineering;
- garantir separação entre coleta, banco, features e modelagem;
- aprovar mudanças de schema;
- transformar decisões técnicas em instruções seguras para o Codex quando necessário.

O CTO decide **como construir corretamente**.

O CTO não gerencia sprint nem backlog.

---

## Data Acquisition Engineer

Responsável por coleta de dados de qualquer fonte.

Escopo:

- crawlers;
- APIs;
- endpoints;
- coleta bruta;
- JSONs;
- inventário de partidas/temporadas;
- rate limit;
- retry;
- backoff;
- sessões;
- headers;
- checkpoints;
- retomada após falha.

Fontes:

- Understat;
- SofaScore;
- FotMob;
- OddsPortal, futuramente.

Não deve:

- alterar schema do banco;
- implementar importers;
- criar features;
- fazer modelagem;
- tomar decisões arquiteturais sozinho;
- propor bypass agressivo de sites.

---

## Data Engineer / Database

Responsável por transformar dados brutos em banco confiável.

Escopo:

- PostgreSQL;
- SQLAlchemy;
- scripts de importação;
- importers;
- validação de dados;
- idempotência;
- deduplicação;
- integridade referencial;
- mapeamento entre fontes;
- preparação para dataset analítico.

Não deve:

- resolver crawlers;
- alterar lógica de coleta;
- criar features H1-H9;
- fazer modelagem;
- alterar schema sem aprovação do CTO;
- apagar dados brutos.

---

## Quant Research / Data Science

Responsável pela pesquisa quantitativa, features e modelagem.

Escopo:

- hipóteses H1-H9;
- definição de target;
- feature engineering;
- validação estatística;
- prevenção de data leakage;
- dataset analítico;
- modelos baseline;
- métricas;
- backtesting.

Não deve:

- resolver coleta;
- implementar importers;
- alterar schema sem aprovação do CTO;
- modelar antes de existir dataset validado;
- usar informação futura em features.

---

## Codex Developer

Responsável por implementação de código.

Escopo:

- alterar arquivos;
- criar scripts;
- corrigir bugs;
- criar testes;
- implementar tarefas aprovadas;
- refatorar apenas quando autorizado.

O Codex deve receber tarefas pequenas, específicas e testáveis.

O Codex não deve:

- decidir arquitetura;
- mudar schema sem aprovação;
- alterar estrutura dos JSONs sem autorização;
- apagar dados brutos;
- misturar coleta, banco, features e modelagem na mesma alteração;
- implementar bypass agressivo contra fontes externas.

---

## Fluxo Padrão de Trabalho

Para uma tarefa comum:

```text
1. Usuário fala com o PM.
2. PM identifica o agente correto.
3. Especialista técnico analisa o problema.
4. CTO revisa se houver impacto arquitetural.
5. Codex implementa se houver mudança de código.
6. Especialista revisa a implementação.
7. PM registra progresso e define próximo passo.
```

---

## Quando Acionar Cada Agente

### Acionar PM quando:

- houver dúvida sobre próximos passos;
- houver confusão de prioridades;
- for necessário organizar sprint;
- for necessário decidir qual agente usar;
- uma tarefa for concluída e precisar registrar avanço.

### Acionar CTO quando:

- houver mudança estrutural;
- houver decisão de arquitetura;
- houver alteração de schema;
- houver dúvida entre abordagens técnicas;
- uma proposta técnica precisar de aprovação.

### Acionar Data Acquisition Engineer quando:

- o assunto for coleta;
- houver erro em crawler;
- houver HTTP 403, rate limit ou endpoint;
- for necessário baixar dados brutos;
- for necessário ajustar retry, delay, backoff ou checkpoints.

### Acionar Data Engineer / Database quando:

- o assunto for PostgreSQL;
- houver importer;
- houver SQLAlchemy;
- houver validação de tabelas;
- houver duplicação ou integridade de dados;
- for necessário popular banco.

### Acionar Quant Research / Data Science quando:

- o assunto for hipótese H1-H9;
- houver definição de target;
- houver features;
- houver dataset analítico;
- houver modelagem;
- houver backtesting.

### Acionar Codex Developer quando:

- a tarefa já estiver clara;
- os arquivos a alterar estiverem definidos;
- os critérios de aceite estiverem definidos;
- a implementação tiver sido aprovada quando necessário.

---

## Sequência Atual Recomendada

No estado atual do projeto, a sequência principal é:

```text
PM
  ↓
Data Acquisition Engineer
  ↓
CTO
  ↓
Codex Developer
  ↓
Data Acquisition Engineer
  ↓
PM
```

Objetivo desta sequência:

- diagnosticar e resolver o HTTP 403 do SofaScore de forma responsável;
- preservar estrutura atual;
- permitir retomada da coleta;
- finalizar coleta EPL.

Depois da coleta:

```text
PM
  ↓
Data Engineer / Database
  ↓
CTO
  ↓
Codex Developer
  ↓
Data Engineer / Database
  ↓
PM
```

Depois do banco populado:

```text
PM
  ↓
Quant Research / Data Science
  ↓
CTO
  ↓
Codex Developer
  ↓
Quant Research / Data Science
  ↓
PM
```

---

## Regras Gerais

- Não conversar com todos os agentes ao mesmo tempo.
- Não enviar tarefas vagas ao Codex.
- Não misturar responsabilidades.
- Não alterar arquitetura sem o CTO.
- Não alterar status/sprint sem o PM.
- Não criar agentes novos sem necessidade.
- Não recriar estruturas existentes.
- Não apagar dados brutos.
- Não usar técnicas agressivas contra fontes externas.
- Documentar decisões relevantes.

---

## Critério de Boa Coordenação

A coordenação estará funcionando bem quando:

- cada agente souber seu papel;
- cada tarefa tiver dono claro;
- o Codex receber tarefas pequenas e objetivas;
- o PM souber o estado atual;
- o CTO aprovar mudanças estruturais;
- especialistas não invadirem escopo uns dos outros;
- a documentação refletir o progresso real do projeto.

## Governança Documental

Antes de iniciar qualquer análise:

1. Ler documentos obrigatórios do seu papel.
2. Verificar CURRENT_SPRINT.md.
3. Verificar PROJECT_STATUS.md.
4. Atualizar apenas os documentos sob sua responsabilidade.
5. Não alterar documentação pertencente a outro agente sem autorização.
