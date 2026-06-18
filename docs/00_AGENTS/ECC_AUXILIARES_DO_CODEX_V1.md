# ECC_AUXILIARES_DO_CODEX_V1

Status: ATIVO

## Objetivo

Documentar o uso dos recursos auxiliares do ECC no projeto Crawler-Trade.

Esses recursos servem para apoiar o Codex, reduzir retrabalho, melhorar verificacao e organizar pesquisas.

Eles NAO substituem os 6 agentes oficiais do projeto.

## Regra central

Os 6 agentes oficiais continuam mandando o prompt. Os recursos ECC apenas auxiliam o Codex na execucao tecnica.

## Status da instalacao

Instalacao local operacional informada:

- `C:/LateGoalResearch/.agents/skills/`

Observacao: `C:/LateGoalResearch` nao foi confirmado como checkout Git valido porque nao contem `.git`.

Status:

- uso local operacional: OK, se o Codex estiver executando a partir de `C:/LateGoalResearch`;
- versionamento das pastas `.agents` no GitHub: PENDENTE;
- documentacao no GitHub: ATIVA.

## Skills ECC instaladas localmente

Confirmadas localmente:

- `deep-research`
- `eval-harness`
- `iterative-retrieval`
- `python-testing`
- `strategic-compact`
- `verification-loop`

Nao instalada nesta etapa:

- `documentation-lookup`

Motivo: fica para fase futura porque seu melhor uso depende de Context7/MCP.

## Agentes ECC auxiliares aprovados

Agentes auxiliares permitidos para instalacao local em `.agents/agents/`:

- `code-explorer`
- `python-reviewer`
- `silent-failure-hunter`

Regra: esses agentes sao auxiliares tecnicos do Codex, nao agentes oficiais do projeto.

## Regras ECC auxiliares aprovadas

Regras permitidas para instalacao local em `.agents/rules/`:

- `anti-fake-work`
- `critical-verification`
- `no-silent-failures`
- `minimal-change`

## Workflows ECC auxiliares aprovados

Workflows permitidos para instalacao local em `.agents/workflows/`:

- `verification-loop`
- `tdd-workflow`
- `research-plan`
- `debugging-loop`

## Itens proibidos nesta etapa

Nao instalar sem aprovacao explicita do PM:

- MCPs;
- hooks globais;
- plugins globais;
- sync completo do ECC;
- configuracao global do Codex;
- `documentation-lookup`;
- agentes extras;
- regras extras;
- workflows extras.

## Ordem geral de uso

### Para pesquisa nova

1. `research-plan`
2. `iterative-retrieval`
3. `deep-research`, se a pesquisa exigir fontes externas ou estudo metodologico
4. `eval-harness`
5. `verification-loop`
6. `strategic-compact`

### Para tarefa em codigo existente

1. `iterative-retrieval`
2. `code-explorer`
3. `minimal-change`
4. `python-testing`, se houver Python
5. `python-reviewer`
6. `silent-failure-hunter`
7. `verification-loop`
8. `strategic-compact`

### Para novo script Python

1. `research-plan`, se houver definicao metodologica
2. `tdd-workflow`
3. `python-testing`
4. `python-reviewer`
5. `no-silent-failures`
6. `verification-loop`
7. `strategic-compact`

### Para divergencia de resultado

Usar quando N, lucro, ROI, EV, drawdown ou taxa mudarem inesperadamente.

1. `debugging-loop`
2. `iterative-retrieval`
3. `code-explorer`
4. `no-silent-failures`
5. `critical-verification`
6. `verification-loop`
7. `strategic-compact`

### Para relatorio financeiro ou estatistico critico

1. `iterative-retrieval`
2. `eval-harness`
3. `critical-verification`
4. `no-silent-failures`
5. `silent-failure-hunter`
6. `verification-loop`
7. `strategic-compact`

## Matriz por agente oficial

### 01 - PM

Usar:

- `research-plan` para organizar nova frente;
- `iterative-retrieval` para recuperar contexto oficial;
- `strategic-compact` para resumo de milestone;
- `verification-loop` para checar entrega;
- `minimal-change` para impedir alteracao fora do escopo.

Ordem sugerida:

`research-plan -> iterative-retrieval -> verification-loop -> strategic-compact`

### 02 - CTO

Usar:

- `code-explorer` antes de mudanca estrutural;
- `minimal-change` para controlar escopo;
- `python-reviewer` para revisao tecnica Python;
- `critical-verification` antes de aprovar arquitetura;
- `no-silent-failures` em pipelines criticos.

Ordem sugerida:

`code-explorer -> minimal-change -> python-reviewer -> no-silent-failures -> critical-verification -> verification-loop`

### 03 - Data Acquisition Engineer

Usar:

- `code-explorer` para mapear coletores;
- `no-silent-failures` para JSON vazio, odds ausentes e APIs;
- `debugging-loop` em divergencia de dados;
- `python-testing` para scripts de coleta;
- `verification-loop` antes de finalizar.

Ordem sugerida:

`code-explorer -> python-testing -> no-silent-failures -> debugging-loop -> verification-loop`

### 04 - Data Engineer / Database

Usar:

- `code-explorer` para ETL/pipelines;
- `tdd-workflow` para novos transformadores;
- `python-testing` para scripts;
- `silent-failure-hunter` para falhas silenciosas;
- `verification-loop` antes de finalizar.

Ordem sugerida:

`code-explorer -> tdd-workflow -> python-testing -> silent-failure-hunter -> verification-loop`

### 05 - Data Science / Quant Research

Usar:

- `research-plan` antes de nova hipotese;
- `iterative-retrieval` para ler docs oficiais;
- `deep-research` quando houver estudo metodologico;
- `eval-harness` para falso positivo, estabilidade e robustez;
- `python-testing` em scripts de analise;
- `python-reviewer` apos alterar codigo;
- `silent-failure-hunter` antes do resultado final;
- `verification-loop` antes de entregar.

Ordem sugerida:

`research-plan -> iterative-retrieval -> eval-harness -> python-testing -> python-reviewer -> silent-failure-hunter -> verification-loop -> strategic-compact`

### 06 - Trade Operations Quant

Usar:

- `iterative-retrieval` para buscar premissas financeiras;
- `eval-harness` para criterios de ROI/EV/drawdown;
- `critical-verification` em lucro, ROI, EV, break-even e drawdown;
- `no-silent-failures` para odds ausentes e N insuficiente;
- `debugging-loop` quando lucro ou ROI divergirem;
- `verification-loop` antes do veredito.

Ordem sugerida:

`iterative-retrieval -> eval-harness -> critical-verification -> no-silent-failures -> debugging-loop se houver divergencia -> verification-loop -> strategic-compact`

## Regra para prompts enviados pelos agentes

Todo prompt enviado ao Codex por um agente oficial deve conter:

1. agente responsavel;
2. objetivo;
3. escopo;
4. arquivos permitidos;
5. arquivos proibidos;
6. recursos ECC que devem ser usados;
7. ordem de uso, quando aplicavel;
8. entregaveis esperados;
9. verificacao obrigatoria.

Modelo minimo:

```text
Use os recursos ECC locais quando aplicavel, seguindo esta ordem:
[ordem especifica da tarefa]

Antes de finalizar, use verification-loop.
Se houver calculo, odds, N, lucro, ROI, EV ou drawdown, use critical-verification e no-silent-failures.
```

## Relacao com a governanca oficial

A governanca oficial continua tendo prioridade sobre qualquer recurso ECC.

Documentos superiores:

- `docs/00_AGENTS/GOVERNANCE_V2.md`
- `docs/00_AGENTS/CHAIN_OF_COMMAND.md`
- `docs/01_CONTEXT/PROJECT_STATUS.md`
- `docs/06_SPRINTS/CURRENT_SPRINT.md`

## Status final

- documentacao do pacote ECC: ATIVA;
- instalacao local das skills: CONFIRMADA EM `C:/LateGoalResearch`;
- instalacao/versionamento no GitHub das pastas `.agents`: PENDENTE;
- `AGENTS.md` no GitHub: AUSENTE ate criacao especifica.
