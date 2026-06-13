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
* Trade Operations Quant
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
* Consolida parecer estatístico e operacional.
* Decide se uma estratégia continua, replica ou é arquivada.

### CTO

* Aprova arquitetura.
* Aprova mudanças estruturais.
* Aprova mudanças de schema.

### Quant Research / Data Science

Responsável por:

* descobrir padrões;
* validar sinais;
* medir taxa de acerto;
* comparar baseline;
* testar significância estatística.

Entrega ao agente 06:

* estratégia;
* N;
* taxa;
* baseline;
* target.

### Trade Operations Quant

Responsável por:

* calcular lucro/prejuízo;
* calcular ROI e EV;
* calcular break-even;
* comparar hold vs cashout;
* avaliar drawdown e risco operacional;
* analisar sensibilidade de odds;
* separar Back Over, Back Under e Lay Over.

Vereditos oficiais:

* APROVADO OPERACIONALMENTE
* APROVADO COM RESSALVAS
* NAO COMPENSA FINANCEIRAMENTE

Proibido:

* criar estratégias;
* coletar dados;
* alterar banco;
* criar features;
* executar modelos;
* executar trade real;
* criar robôs.

### Especialistas

* Produzem análises e recomendações.
* Não alteram arquitetura por conta própria.
* Devem atuar apenas dentro do próprio escopo.

### Codex

* Apenas implementa tarefas aprovadas.
* Não toma decisões arquiteturais.
* Não interpreta resultados financeiros.
* Deve seguir regras documentadas.

## Fluxos Oficiais

### Descoberta Estatística

PM → Quant Research → Codex → Quant Research → Trade Operations Quant → PM

### Pesquisa Operacional

PM → Trade Operations Quant → PM

### Coleta de Dados

PM → Data Acquisition → CTO → Codex → Data Acquisition → PM

### Banco de Dados

PM → Data Engineer → CTO → Codex → Data Engineer → PM

### Produção de Estratégia

Data Science → Trade Operations Quant → PM → CTO (quando necessário)
