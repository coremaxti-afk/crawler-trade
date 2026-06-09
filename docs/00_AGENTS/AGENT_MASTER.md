# AGENT MASTER

## Objetivo

LateGoalResearch e um projeto de pesquisa quantitativa para identificar padroes associados a gols tardios e protocolos exploratorios de trade esportivo no futebol atraves da integracao de multiplas fontes de dados.

O projeto pertence ao repositorio:

```text
coremaxti-afk/crawler-trade
```

---

## Governanca

Documento oficial:

- `docs/00_AGENTS/GOVERNANCE_V2.md`

Principios:

- Chat = Comunicacao Executiva.
- GitHub = Fonte Oficial da Verdade.
- Em caso de conflito, GitHub prevalece.
- `PROJECT_STATUS.md` e `CURRENT_SPRINT.md` devem permanecer atualizados.

Todos os agentes devem seguir a `GOVERNANCE_V2` enquanto ela estiver ativa.

---

## Fontes Principais

1. SofaScore
   - `event`, `statistics`, `incidents`, `graph`, `shotmap`.
2. Football-Data
   - odds historicas pre-jogo/closing para 1X2 e Over/Under 2.5.
3. Understat
   - fonte historica complementar para metricas pre-jogo/rolling quando validado sem leakage.

## Fontes Secundarias / Futuras

1. FotMob.
2. OddsPortal.
3. Odds live/in-play com timestamp historico confiavel, se disponivel futuramente.

---

## Ordem de Leitura para Novos Agentes

1. `docs/00_AGENTS/AGENT_MASTER.md`
2. `docs/00_AGENTS/GOVERNANCE_V2.md`
3. `docs/00_AGENTS/AGENT_COORDINATION.md`
4. `docs/01_CONTEXT/PROJECT_STATUS.md`
5. `docs/06_SPRINTS/CURRENT_SPRINT.md`
6. Documentacao especifica da area de atuacao.

---

## Estado Atual do Projeto

Concluido:

- PostgreSQL operacional.
- Understat operacional como fonte historica complementar.
- SofaScore EPL 2024/25 coletado/importado para 380 partidas importaveis.
- `graph` e `shotmap` coletados/importados para H8.
- Dataset Analitico V1 criado.
- H3/H4, H6/H9 e H8 testados em baselines controlados; nenhum baseline foi aprovado quantitativamente.
- Football-Data EPL 2024/25 importado localmente com 380 partidas e 34280 odds.
- Odds Feature Builder V1 e Dataset Odds V1 concluidos.
- Odds isoladas e Odds+H8 avaliadas; odds nao seguem como frente principal isolada.
- Match State + Odds + H8 Variation V1 executada como exploratoria.
- H8 Composite Pressure Score V1 executado como exploratorio.
- Dynamic Trade Protocol Validation V1 executado como simulacao teorica com odds medias fixas.
- Issues abertas para `MARKET_PRICE_CASHOUT_SENSITIVITY_V1` e `DYNAMIC_TRADE_PROTOCOL_VALIDATION_V2`.

Em andamento:

- Expansao controlada de protocolos dinamicos de trade teorico.
- Correcao/verificacao de JSONs vazios da entrega `MATCH_STATE_ODDS_H8_VARIATION_V1`.
- Planejamento de `MARKET_PRICE_CASHOUT_SENSITIVITY_V1`.
- Planejamento de `H8_TEAM_SIDE_FEATURES_V1` para separar pressao por equipe.
- Selecao de padroes para replicacao multi-liga.

Bloqueado / proibido sem nova aprovacao:

- Trade real.
- Robo.
- Producao.
- Backtesting financeiro real.
- Modelo ou baseline preditivo novo.
- Uso de odds live sem timestamp historico confiavel.
- Uso de eventos pos-cutoff como feature.
- Uso de placar final ou target-derived columns como preditores.

---

## Proximos Marcos

1. Corrigir/verificar JSONs vazios de `MATCH_STATE_ODDS_H8_VARIATION_V1`.
2. Criar/revisar `DYNAMIC_TRADE_PROTOCOL_EXPANSION_PLAN_V1.md`.
3. Executar `DYNAMIC_TRADE_PROTOCOL_VALIDATION_V2` apenas apos plano aprovado.
4. Especificar `MARKET_PRICE_CASHOUT_SENSITIVITY_V1`.
5. Especificar `H8_TEAM_SIDE_FEATURES_V1`.
6. Selecionar padroes para replicacao multi-liga.

---

## Regra PM

A fase atual e pesquisa exploratoria, nao operacao real.

Todo agente deve separar explicitamente:

- taxa estatistica;
- EV teorico;
- EV com cashout;
- operacionalidade real;
- necessidade de replicacao.
