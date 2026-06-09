# PROJECT_OBJECTIVE_TRADE_INSIGHTS

## Status

Objetivo estrategico definido pelo usuario.

Data: 2026-06-09

---

## Objetivo Atual do Projeto

O projeto LateGoalResearch / Crawler-Trade deve evoluir para gerar insights de entradas em trade esportivo, com foco em decisoes dinamicas baseadas no estado do jogo, odds, H8 e protocolos de saida.

O objetivo nao e apenas prever gol tardio.

O objetivo atual e responder:

```text
Quando entrar?
Quando sair?
Quando realizar cashout?
Quando manter ate o fim e assumir o risco total?
Qual o lucro/prejuizo esperado dado o preco/odd?
```

---

## Capacidades Esperadas

O projeto deve ser capaz de:

1. Gerar insights de entrada em trade esportivo.
2. Calcular lucro/prejuizo sobre a odd de entrada.
3. Calcular cenarios de cashout.
4. Comparar hold ate o fim versus saida dinamica.
5. Indicar melhores criterios para entrada.
6. Indicar melhores criterios para cashout positivo ou negativo.
7. Indicar quando manter a operacao ate o fim da janela ou fim do jogo.
8. Detectar quando o jogo esfria apos a entrada e sugerir saida.
9. Detectar quando o jogo continua quente/frio e sugerir manter.
10. Separar taxa estatistica, EV teorico, EV com cashout e operacionalidade real.

---

## Tipos de Decisao Que o Projeto Deve Suportar

### Entrada

Exemplos:

- Lay Over em jogo frio.
- Back Over em jogo quente.
- Entrada com favorito vencendo por 1.
- Entrada com mandante/visitante vencendo por 1.
- Entrada com favorito perdendo por 1.
- Entrada com H8 frio/quente.
- Entrada combinando Match State + Odds + H8.

### Gestao da Operacao

Depois da entrada, o projeto deve avaliar:

- se o jogo continuou coerente com a tese;
- se o jogo esfriou;
- se o jogo aqueceu;
- se a pressao mudou de direcao;
- se vale cashout;
- se vale segurar ate o fim;
- se o risco de perda integral e compensado pelo EV.

### Saida / Cashout

O projeto deve comparar:

- cashout fixo em minuto predefinido;
- cashout condicional por mudanca de H8;
- cashout positivo;
- cashout negativo;
- hold ate o fim da janela;
- hold ate o final do jogo.

---

## Mercado Inicial

Mercados exploratorios atuais:

- Back Over.
- Lay Over.

Mercados futuros podem incluir outros tipos de trade, mas somente apos aprovacao PM/Quant.

---

## Requisitos Analiticos

Cada estrategia deve reportar, quando aplicavel:

- criterio de entrada;
- minuto de entrada;
- odd de entrada;
- criterio de saida;
- minuto de saida;
- odd de saida/cashout;
- wins;
- losses;
- cashouts;
- lucro total;
- prejuizo total;
- ROI;
- EV hold;
- EV com cashout;
- break-even hold;
- break-even com cashout;
- drawdown simples;
- maior sequencia negativa;
- lucro medio por trade;
- comparacao contra hold simples;
- comparacao contra cashout fixo;
- classificacao de robustez;
- necessidade de replicacao multi-liga.

---

## Regras Metodologicas

Obrigatorio:

- preservar anti-leakage por cutoff;
- usar somente dados disponiveis ate o momento da decisao;
- separar pesquisa exploratoria de producao;
- separar odds medias fixas de odds historicas reais;
- registrar N pequeno como micro-amostra;
- validar robustez antes de qualquer conclusao operacional;
- preferir replicacao multi-liga antes de qualquer uso real.

Proibido sem autorizacao explicita:

- trade real;
- robo;
- producao;
- automacao operacional;
- modelo preditivo novo;
- baseline preditivo novo;
- backtesting financeiro real com odds live nao timestampadas;
- uso de eventos pos-cutoff como feature;
- uso de placar final como feature;
- uso de colunas target-derived como feature.

---

## Direcao Tecnica Prioritaria

Prioridades atuais:

1. `DYNAMIC_TRADE_PROTOCOL_EXPANSION_PLAN_V1`.
2. `DYNAMIC_TRADE_PROTOCOL_VALIDATION_V2`.
3. `MARKET_PRICE_CASHOUT_SENSITIVITY_V1`.
4. `H8_TEAM_SIDE_FEATURES_V1`.
5. Replicacao multi-liga dos padroes mais promissores.
6. Futuro: odds live historicas por timestamp, se disponiveis.

---

## Interpretacao PM

A pesquisa deve deixar de ser apenas:

```text
Vai sair gol?
```

E passar a ser:

```text
Existe uma operacao com entrada, gestao e saida que possui vantagem estatistica e financeira?
```

Esse e o novo eixo central do projeto.
