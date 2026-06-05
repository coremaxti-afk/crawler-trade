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

Acionar Data Acquisition Engineer para projetar um spike/coleta controlada do `graph.json` em partidas já existentes da EPL.

Objetivo da próxima etapa:

- medir cobertura;
- medir taxa de sucesso;
- avaliar risco de HTTP 403;
- confirmar consistência do payload;
- preparar decisão posterior sobre importer e feature engineering H8.
