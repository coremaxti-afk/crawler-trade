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

---

## Princípio Fundamental

Chat deve conter:

- decisões;
- aprovações;
- direcionamentos;
- coordenação.

GitHub deve conter:

- documentação;
- relatórios;
- metodologia;
- resultados;
- especificações.

Em caso de conflito:

**GitHub prevalece.**

Nenhuma decisão arquitetural, metodológica ou de pesquisa é considerada oficial até estar registrada no GitHub.

---

## Estrutura Obrigatória para Todos os Agentes

### 1. Resumo Executivo

Máximo de 5 a 10 linhas.

Responder:

- o que foi feito;
- resultado;
- recomendação.

---

### 2. Impacto no Projeto

Responder:

"O que mudou no estado do projeto?"

Exemplos:

- H3 validada inicialmente.
- H4 validada inicialmente.
- Dataset V1 concluído.

---

### 3. Decisão Necessária

Formato obrigatório:

Decisão necessária:

[ ] Aprovar

[ ] Revisar

[ ] Bloquear

O agente deve indicar sua recomendação.

---

### 4. GitHub

Formato obrigatório:

Arquivos criados:

- ...

Arquivos alterados:

- ...

Commit:

- ...

---

### 5. Verificação Documental

Formato obrigatório:

Documentação precisa ser atualizada?

SIM

ou

NÃO

Se SIM:

Arquivos:

- ...

---

### 6. Próximo Agente

Formato obrigatório:

Próximo agente:

...

---

### 7. Prompt para o Próximo Agente

Sempre fornecer prompt pronto para copiar.

Não reproduzir:

- documentação completa;
- relatório completo;
- metodologia completa.

---

## Proibições

Não colocar no chat:

- documentação completa;
- relatórios completos;
- metodologia completa;
- conteúdo já registrado no GitHub.

---

## Exceções

Permitido quando necessário:

- código;
- SQL;
- diffs;
- patches;
- revisão técnica.

---

## Reversão

A Governança V2 pode ser revertida para V1 por decisão do Sponsor / Product Owner.

---

## Escopo

Aplica-se a:

- PM
- CTO
- Data Acquisition Engineer
- Data Engineer / Database
- Quant Research
- Codex Developer

---

## Precedência

Enquanto ativa:

GOVERNANCE_V2.md possui precedência operacional sobre formatos anteriores de comunicação.
