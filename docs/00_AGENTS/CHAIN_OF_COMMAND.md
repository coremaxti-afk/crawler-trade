# CHAIN_OF_COMMAND

## Autoridade do Projeto

Sponsor / Product Owner (Usuário)
↓
PM
↓
CTO
↓
Especialistas

* Data Acquisition Engineer
* Data Engineer / Database
* Quant Research / Data Science
  ↓
  Codex Developer

## Regras

### Usuário

* Define objetivos.
* Aprova decisões relevantes.
* Pode acionar qualquer agente.

### PM

* Define prioridades.
* Controla sprint.
* Define qual agente deve atuar.
* Atualiza status do projeto.

### CTO

* Aprova arquitetura.
* Aprova mudanças estruturais.
* Aprova mudanças de schema.

### Especialistas

* Produzem análises e recomendações.
* Não alteram arquitetura por conta própria.

### Codex

* Apenas implementa tarefas aprovadas.
* Não toma decisões arquiteturais.

## Fluxos Oficiais

### Nova Funcionalidade

PM → CTO → Especialista → Codex → Especialista → PM

### Coleta de Dados

PM → Data Acquisition → CTO → Codex → Data Acquisition → PM

### Banco de Dados

PM → Data Engineer → CTO → Codex → Data Engineer → PM

### Pesquisa

PM → Quant Research → CTO (quando necessário) → Codex → Quant Research → PM
