# SofaScore Graph / Momentum Endpoint

Status: ENDPOINT CONFIRMADO

Frente relacionada: H8 — Graph / Momentum

---

## Objetivo

Registrar oficialmente o endpoint SofaScore de graph/momentum para uso futuro na frente H8.

Este documento registra apenas a descoberta e a orientação arquitetural inicial.

Não autoriza implementação de importer, features, baseline ou modelagem.

---

## Endpoint

```text
https://www.sofascore.com/api/v1/event/{event_id}/graph
```

Exemplo validado:

```text
https://www.sofascore.com/api/v1/event/12436874/graph
```

---

## Payload Observado

```json
{
  "graphPoints": [
    {"minute": 1, "value": 3},
    {"minute": 2, "value": 20},
    {"minute": 3, "value": 5},
    {"minute": 4, "value": 6},
    {"minute": 5, "value": 18},
    {"minute": 6, "value": -13},
    {"minute": 7, "value": -26}
  ]
}
```

---

## Interpretação Inicial

Cada item em `graphPoints` contém:

- `minute`: minuto da partida;
- `value`: valor de momentum observado para aquele minuto.

Valores positivos e negativos parecem representar variação relativa de domínio/momentum entre as equipes.

A semântica exata do sinal deve ser validada antes de qualquer feature engineering oficial.

---

## Estrutura Raw Recomendada

Caso a coleta seja aprovada, salvar o JSON bruto em:

```text
data/raw/sofascore/premier_league_61627/matches/{event_id}/graph.json
```

---

## Regras de Coleta Recomendadas

A coleta deve seguir as mesmas regras operacionais dos coletores SofaScore seguros:

- checkpoint por arquivo;
- não sobrescrever JSON válido existente;
- `--limit` obrigatório;
- delay entre partidas;
- jitter;
- retry/backoff para falhas temporárias;
- HTTP 403 deve encerrar o lote;
- log auditável separado;
- sem paralelismo;
- sem bypass agressivo;
- sem rotação de IP.

---

## Validação Mínima do Payload

Um `graph.json` deve ser considerado válido se:

- for JSON parseável;
- contiver a chave `graphPoints`;
- `graphPoints` for uma lista;
- cada item tiver `minute` e `value`;
- `minute` for numérico ou conversível para número;
- `value` for numérico ou conversível para número.

Payload vazio ou ausente deve ser registrado, não inferido.

---

## Resultado do Spike Inicial

Data de registro: 2026-06-05

Coletores utilizados:

```text
LateGoalResearch/Crawler/Sofascore/h8_graph_momentum_collector.py
LateGoalResearch/Crawler/Sofascore/h8_graph_momentum_collector_playwright.py
```

Logs auditáveis locais:

```text
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\collection_log_graph.jsonl
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\collection_log_graph_playwright.jsonl
```

Partidas testadas no spike controlado:

| Ordem | event_id | Partida | target_late_goal_75 | Status Playwright | graphPoints |
|---:|---:|---|---:|---|---:|
| 1 | 12436870 | Manchester United x Fulham | 1 | JSON válido | 92 |
| 2 | 12436873 | Everton x Brighton & Hove Albion | 1 | JSON válido | 92 |
| 3 | 12436875 | Nottingham Forest x Bournemouth | 1 | JSON válido | 92 |
| 4 | 12436871 | Ipswich Town x Liverpool FC | 0 | JSON válido | 92 |
| 5 | 12436872 | Arsenal x Wolverhampton | 0 | JSON válido | 92 |

Resumo operacional:

- Partidas planejadas: 5.
- Partidas efetivamente coletadas via Playwright com sessão aquecida: 5.
- JSONs válidos retornados: 5.
- JSONs falhos/bloqueados na execução Playwright: 0.
- `graphPoints` observado: sim, em 5/5 partidas.
- `graph_points_count`: 92 em todas as 5 partidas.
- HTTP 403 na execução Playwright: não.
- Critério de 80% de validade: atingido, com 100% de validade no spike.

Observação operacional:

O coletor inicial baseado em `urllib` retornou HTTP 403 para `event_id=12436870` em tentativas anteriores. A variante Playwright com browser/sessão aquecida coletou as 5 partidas com sucesso. Portanto, o endpoint está acessível, mas depende de contexto de navegador/sessão para a coleta controlada.

Interpretação:

O payload observado é consistente com o contrato esperado para H8 Graph/Momentum. A presença de 92 pontos em todas as partidas sugere cobertura minuto-a-minuto suficiente para avaliação posterior, mas ainda é uma amostra pequena.

Recomendação:

- Status H8 Graph/Momentum: APTO PARA AMPLIAÇÃO CONTROLADA.
- Ampliar para 20 partidas com o coletor Playwright e warmup manual/sessão persistida.
- Manter limite, checkpoint, delay, jitter, log auditável e parada imediata em HTTP 403.
- Não implementar importer, features, dataset ou baseline H8 até a amostra de 20 partidas ser validada.

---

## Restrições

- Não alterar schema.
- Não implementar importer.
- Não criar features H8 ainda.
- Não criar dataset novo.
- Não executar baseline.
- Não fazer modelagem.
- Não misturar coleta graph com features.
- Não alterar estrutura dos JSONs existentes.

---

## Próximo Passo Recomendado

Acionar Data Acquisition Engineer para ampliar o spike controlado para 20 partidas usando a variante Playwright com sessão aquecida.

Objetivo da próxima etapa:

- medir cobertura em amostra maior;
- confirmar estabilidade sem HTTP 403;
- medir variação de `graphPoints` por partida;
- confirmar consistência do payload antes de qualquer decisão sobre importer e feature engineering H8.
