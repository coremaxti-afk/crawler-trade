# GOVERNANCE_V2

Status: EXPERIMENTAL

Estado: ATIVA

Versão: V2

---

## Objetivo

Reduzir sobrecarga de contexto.

Separar claramente:

- Chat → Comunicação Executiva
- GitHub → Fonte Oficial da Verdade

A governança V2 define como agentes devem comunicar decisões, registrar progresso, atualizar documentação e manter rastreabilidade do projeto LateGoalResearch.

---

## Princípio Fundamental

Chat deve conter:

- decisões;
- aprovações;
- direcionamentos;
- coordenação;
- dúvidas objetivas;
- pedidos de execução.

GitHub deve conter:

- documentação;
- relatórios;
- metodologia;
- resultados;
- especificações;
- estado atual do projeto;
- status de sprint;
- artefatos versionáveis;
- histórico técnico rastreável.

Regra central:

```text
O chat coordena. O GitHub registra.
```

---

## Fonte Oficial da Verdade

A fonte oficial da verdade documental do projeto é o repositório GitHub:

```text
coremaxti-afk/crawler-trade
```

Documentos de estado que devem permanecer atualizados:

- `docs/01_CONTEXT/PROJECT_STATUS.md`
- `docs/06_SPRINTS/CURRENT_SPRINT.md`

Documentos técnicos/metodológicos devem ser atualizados conforme a frente impactada:

- `docs/03_SOURCES/`
- `docs/04_RESEARCH/`
- `docs/08_DATABASE/`
- `docs/00_AGENTS/`

---

## Nova Regra de Autonomia Documental

Todo agente possui autonomia para atualizar a documentação necessária ao concluir uma entrega.

Não é mais necessário solicitar autorização prévia para atualizar documentos quando a atualização apenas registra, corrige ou sincroniza o estado real do projeto.

É obrigatório atualizar documentação quando o estado do projeto mudar.

É obrigatório manter atualizado:

- `docs/01_CONTEXT/PROJECT_STATUS.md`
- `docs/06_SPRINTS/CURRENT_SPRINT.md`

É obrigatório registrar commits relevantes quando houver alteração documental, técnica ou metodológica significativa.

---

## Responsabilidade Documental dos Agentes

Cada agente deve atualizar a documentação impactada pela própria entrega.

Exemplos:

- Data Acquisition Engineer deve documentar fontes, endpoints, coleta, logs, cobertura e limitações.
- Data Engineer / Database deve documentar schema, importers, validações de banco, integridade e status de importação.
- Quant Research / Data Science deve documentar hipóteses, validações estatísticas, features, datasets, métricas e riscos de leakage.
- CTO deve documentar decisões arquiteturais, restrições técnicas, aprovações e pareceres.
- PM deve manter visão de sprint, roadmap, prioridades e estado executivo.
- Codex Developer deve atualizar documentação quando uma implementação altera o estado do projeto ou entrega artefatos relevantes.

A autonomia documental não altera papéis técnicos nem cadeia de decisão.

---

## Documentação Obrigatória ao Concluir Entregas

Ao concluir uma entrega, o agente responsável deve avaliar se precisa atualizar:

1. `PROJECT_STATUS.md`
2. `CURRENT_SPRINT.md`
3. documento técnico da área impactada;
4. relatório de resultado, se aplicável;
5. especificação, se a entrega consolidar decisão ou contrato técnico;
6. lista de commits relevantes.

A atualização deve ser objetiva e rastreável.

Não é necessário duplicar conteúdo extenso entre documentos, mas os documentos de status devem apontar para os artefatos principais.

---

## Commits Relevantes

Devem ser registrados em documentação quando representarem:

- implementação de script relevante;
- criação ou alteração de schema/importer;
- criação de dataset ou artefato analítico;
- relatório estatístico ou validação importante;
- decisão metodológica;
- mudança de status de uma frente;
- correção documental importante;
- restauração de governança.

O registro pode ser feito no documento específico da frente ou em documentos de status, conforme relevância.

---

## Exceções que Exigem Aprovação PM/CTO

Continuam exigindo aprovação explícita do PM, CTO ou ambos, conforme o caso:

- mudanças de estratégia;
- mudanças de target;
- mudanças de arquitetura;
- mudanças de governança;
- mudanças de roadmap;
- mudanças de schema não autorizadas previamente;
- criação de nova frente técnica;
- avanço para baseline, modelagem, backtesting ou produção fora do escopo aprovado.

Atualizar documentação para refletir uma decisão aprovada é permitido.

Tomar a decisão sem aprovação não é permitido.

---

## Regras de Escopo

Agentes podem atualizar documentação necessária para refletir sua entrega.

Agentes não podem usar atualização documental para:

- mudar estratégia por conta própria;
- redefinir target;
- alterar arquitetura aprovada;
- alterar roadmap;
- reescrever governança sem autorização;
- promover fonte, modelo ou baseline a status oficial sem aprovação;
- mascarar incertezas ou pendências.

Quando houver dúvida se uma mudança documental altera decisão de projeto, o agente deve pedir validação ao PM/CTO.

---

## Padrão de Escrita Documental

Documentos devem ser:

- claros;
- auditáveis;
- datados quando necessário;
- objetivos;
- consistentes com o estado real do projeto;
- explícitos sobre restrições;
- explícitos sobre pendências;
- explícitos sobre próximos passos.

Evitar:

- documentação genérica;
- duplicação excessiva;
- conclusões sem evidência;
- promoção de hipótese a fato;
- misturar coleta, banco, features e modelagem no mesmo documento sem necessidade.

---

## Relação Chat x GitHub

O chat pode conter resumo executivo, decisão ou pedido.

O GitHub deve conter o registro persistente.

Quando uma decisão relevante ocorrer no chat, o agente responsável deve registrar a decisão no documento adequado.

Quando uma entrega relevante for concluída, o agente responsável deve registrar:

- o que mudou;
- arquivos ou tabelas impactados;
- resultado da validação;
- restrições ainda ativas;
- commits relevantes.

---

## Documentos de Status

### PROJECT_STATUS.md

Deve refletir o estado global do projeto.

Atualizar quando houver mudança em:

- fontes de dados;
- cobertura de coleta;
- banco/importação;
- datasets;
- features;
- validações estatísticas;
- baselines;
- hipóteses;
- bloqueios;
- próximos passos oficiais.

### CURRENT_SPRINT.md

Deve refletir a frente ativa.

Atualizar quando houver mudança em:

- tarefas concluídas;
- tarefa atual;
- próximos passos;
- bloqueios;
- status da sprint;
- frente oficial do momento.

---

## Critério de Boa Governança

A governança está funcionando quando:

- o chat fica leve e orientado a decisão;
- o GitHub contém o histórico confiável;
- qualquer agente consegue entender o estado atual lendo os documentos;
- `PROJECT_STATUS.md` e `CURRENT_SPRINT.md` não ficam defasados;
- entregas relevantes possuem commit e documentação;
- exceções e riscos continuam explícitos;
- mudanças estratégicas continuam passando por PM/CTO.

---

## Status Final

Governança V2 restaurada e atualizada com autonomia documental aprovada pelo PM.

Status: ATIVA.
