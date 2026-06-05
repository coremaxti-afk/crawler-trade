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

Coletor utilizado:

```text
LateGoalResearch/Crawler/Sofascore/h8_graph_momentum_collector.py
```

Log auditável local:

```text
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\collection_log_graph.jsonl
```

Partidas planejadas para o spike controlado:

| Ordem | event_id | Partida | target_late_goal_75 | Status |
|---:|---:|---|---:|---|
| 1 | 12436870 | Manchester United x Fulham | 1 | Testada; HTTP 403 |
| 2 | 12436873 | Everton x Brighton & Hove Albion | 1 | Não testada; execução encerrada por HTTP 403 |
| 3 | 12436875 | Nottingham Forest x Bournemouth | 1 | Não testada; execução encerrada por HTTP 403 |
| 4 | 12436871 | Ipswich Town x Liverpool FC | 0 | Não testada; execução encerrada por HTTP 403 |
| 5 | 12436872 | Arsenal x Wolverhampton | 0 | Não testada; execução encerrada por HTTP 403 |

Resumo operacional:

- Partidas planejadas: 5.
- Partidas únicas efetivamente testadas: 1.
- Tentativas registradas no log: 3, todas para `event_id=12436870`.
- JSONs válidos retornados: 0.
- JSONs falhos/bloqueados: 1 partida única.
- HTTP 403: sim.
- `graphPoints` observado no spike: não, pois não houve resposta 200 válida.
- `graph_points_count`: 0.
- Critério de 80% de validade: não atingido.

Interpretação:

O coletor respeitou a regra operacional de parada imediata em HTTP 403. Uma nova tentativa manual em 2026-06-05 também retornou HTTP 403 no primeiro evento. Nenhuma ampliação de coleta deve ser feita enquanto o bloqueio persistir.

Recomendação:

- Status H8 Graph/Momentum: BLOQUEADO para ampliação imediata.
- Não ampliar para 20 partidas neste momento.
- Revisar estratégia operacional de Data Acquisition antes de nova tentativa.
- Não implementar importer, features, dataset ou baseline H8 até existir amostra raw válida suficiente.

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

Acionar Data Acquisition Engineer para revisar o bloqueio HTTP 403 observado no spike inicial antes de qualquer nova ampliação.

Objetivo da próxima etapa:

- reduzir risco de bloqueio;
- confirmar se o endpoint permanece acessível em ambiente autorizado;
- obter amostra raw válida mínima antes de qualquer decisão sobre importer e feature engineering H8.
