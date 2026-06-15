# SPORTMONKS_OPERATIONAL_PLAYBOOKS_V3_SCOPE_V1

## Objetivo

Registrar o escopo oficial da futura frente:

```text
SPORTMONKS_OPERATIONAL_PLAYBOOKS_V3
```

A V3 deve transformar os playbooks V2 em especificações operacionais avançadas, mantendo as estratégias exatamente como estão.

---

## Decisão

O projeto seguirá para V3 com todos os playbooks aprovados atualmente, antes da validação multi-liga e multi-temporada.

Playbooks base:

```text
BO_75_HOME_WINNING_BY_1_VISITOR_PRESSING
LO_65_TEAM_WINNING_BY_1_OPP_COLD_2OF3
LO_65_FAVORITE_WINNING_BY_1_OPP_COLD_2OF3
```

---

## O que a V3 deve entregar

### 1. Ficha operacional completa

Para cada playbook:

- código;
- nome curto;
- família;
- mercado;
- direção;
- minuto de entrada;
- janela/target;
- tipo de operação;
- objetivo operacional.

### 2. Checklist de entrada

Cada playbook deve ter checklist objetivo:

```text
[ ] minuto correto
[ ] placar correto
[ ] lado correto pressionando/frio
[ ] janela estatística válida
[ ] mercado disponível
[ ] odd mínima atingida
```

### 3. Regras de não entrada

Incluir bloqueios objetivos, por exemplo:

- vantagem de 2+ gols;
- cartão vermelho;
- odds abaixo da mínima;
- mercado suspenso;
- baixa liquidez;
- estatística contraditória;
- favorito indefinido quando a estratégia exige favorito.

### 4. Regras de saída

Separar:

- saída por gol;
- saída por fim do jogo;
- cashout estimado;
- invalidação operacional.

### 5. Odd mínima sugerida

Usar odds médias do projeto como base:

```text
60 = 1.50
65 = 1.60
70 = 1.80
75 = 2.00
80 = 2.45
85 = 3.35
```

Toda conclusão financeira deve ser marcada como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MÉDIAS
```

### 6. Gestão de stake

Regra inicial conservadora:

```text
Stake padrão: 1 unidade
Stake máxima por operação: 1 unidade
Máximo de operações simultâneas: 1
Não usar martingale
Não aumentar stake após red
```

### 7. Risco operacional

Incluir:

- risco principal;
- sequência de perdas esperada;
- drawdown simples;
- sensibilidade à odd;
- risco de liquidez;
- risco de cashout estimado.

### 8. Interpretação estatística e financeira

Registrar por playbook:

- confirmação 2024/25;
- confirmação 2025/26;
- ROI estimado;
- EV estimado;
- lucro estimado;
- break-even;
- ressalvas.

### 9. Classificação V3

Classificar cada playbook como:

```text
V3 EXPERIMENTAL
V3 VALIDADO COM RESSALVAS
V3 CANDIDATO OPERACIONAL
```

---

## Restrições

A V3 não deve:

- criar novas estratégias;
- alterar filtros estatísticos;
- alterar features-base;
- otimizar parâmetros;
- criar modelos;
- criar robôs;
- executar trade real;
- afirmar produção;
- afirmar backtesting financeiro real.

---

## Próxima etapa após V3

Após V3, a próxima etapa será validação dos mesmos playbooks em novas ligas e novas temporadas.

```text
VALIDAÇÃO MULTI-LIGA / MULTI-TEMPORADA
```

---

## Decisão geral

```text
APROVADO COM RESSALVAS PARA DOCUMENTAÇÃO OPERACIONAL V3
```
