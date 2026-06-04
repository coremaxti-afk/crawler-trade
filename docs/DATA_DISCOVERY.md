# DATA DISCOVERY

Este documento registra todas as descobertas realizadas durante o projeto.

Objetivos:

1. Nenhuma descoberta deve ser perdida.
2. Separar descobertas técnicas de descobertas estatísticas.
3. Registrar hipóteses, evidências e limitações.
4. Permitir que novos membros entendam rapidamente o estado do projeto.

---

# FotMob Technical Discoveries

## Working League Endpoint

Endpoint validado:

https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025

Status:

CONFIRMADO

---

### Dados Disponíveis

Estrutura observada:

```json
fixtures
allMatches
table
overview
stats
seasons
```

Dentro de:

```json
fixtures.allMatches
```

foram identificados:

```json
id
home
away
status
utcTime
pageUrl
round
```

---

### FotMob Match ID

Campo:

```json
id
```

corresponde ao:

```text
fotmob_match_id
```

Utilizado para relacionar partidas com dados detalhados do FotMob.

---

## Premier League Validation

Liga:

Premier League

League ID:

47

Temporada:

2024/2025

Resultado:

```text
Partidas descobertas: 380
Partidas mapeadas: 369
Não mapeadas: 11
```

Status:

CONCLUÍDO

---

## Understat → FotMob Match Mapping

Problema:

Relacionar partidas do Understat com partidas do FotMob.

Resultado:

```text
369 partidas associadas com sucesso.
```

Exemplos:

```text
Manchester United x Fulham
→ 4506263

Ipswich x Liverpool
→ 4506264

Arsenal x Wolverhampton Wanderers
→ 4506265
```

Status:

CONCLUÍDO

---

# MatchDetails Investigation

## Endpoint

Endpoint identificado:

https://www.fotmob.com/api/data/matchDetails?matchId=XXXX

---

## Objetivo

Coletar:

```text
momentum
events
playerStats
attackingZones
shotmap
matchFacts
expectedGoals
```

---

## Resultado Atual

Requests:

```python
requests.get(...)
```

Retorno:

```json
{
  "error": "Verification required",
  "code": "TURNSTILE_REQUIRED"
}
```

Status HTTP:

```text
403
```

---

## Playwright Investigation

Método:

```text
Abrir página
↓
Interceptar respostas
↓
Capturar matchDetails
```

Resultado:

```text
URL detectada
Payload bloqueado
```

Status:

PARCIAL

---

## Header x-mas

Obtido via:

```text
Copy as cURL
```

Resultado:

```text
403
```

Conclusão:

Header isolado não resolve o bloqueio.

---

## DevTools Investigation

Resultado observado:

```text
200 OK (from disk cache)
```

Hipótese:

O navegador estava exibindo uma resposta armazenada localmente.

Status:

PROVÁVEL

---

# Historical Evidence

## matchdetails.json

Arquivo encontrado:

```text
matchdetails.json
```

Contém:

```text
momentum
events
expectedGoals
expectedGoalsOnTarget
playerStats
attackingZones
matchFacts
shotmap
```

Conclusão:

O payload do MatchDetails foi capturado com sucesso pelo menos uma vez.

A captura atualmente não é reproduzível.

---

# Open Challenges

## Challenge 1

Problema:

Capturar MatchDetails automaticamente.

Status:

ABERTO

Tentativas realizadas:

* requests
* custom headers
* x-mas
* Playwright
* acesso direto ao endpoint
* janela anônima
* interceptação de rede

Resultado:

Não resolvido.

---

## Challenge 2

Problema:

Identificar exatamente como o matchdetails.json foi capturado.

Status:

ABERTO

Evidências:

* Arquivo existe.
* Conteúdo válido.
* Método não reproduzível atualmente.

---

# Statistical Discoveries

## Momentum

Fonte:

FotMob

Status:

VALIDADO

Descrição:

Pressão ofensiva minuto a minuto.

Faixa observada:

```text
-100 até +100
```

Observações:

* Aproximadamente 94 registros por partida.
* Inclui acréscimos.
* Principal série temporal encontrada até o momento.

---

## Goal (Shotmap)

Fonte:

FotMob

Status:

VALIDADO

Descrição:

Gols registrados dentro de:

```text
shotmap.shots
```

Identificados por:

```text
eventType = Goal
```

Campos observados:

* min
* minAdded
* teamId
* playerName
* expectedGoals

---

## Touches In Opposition Box

Fonte:

FotMob

Status:

VALIDADO

Descrição:

Quantidade de toques na área adversária.

Observação:

Potencial substituto para métricas de ataques perigosos.

---

## Expected Goals (xG)

Fonte:

FotMob / Understat

Status:

VALIDADO

Descrição:

Métrica principal de qualidade de chances.

---

## Expected Goals On Target (xGOT)

Fonte:

FotMob

Status:

VALIDADO

Descrição:

Avalia qualidade da finalização após o chute.

---

## Total Shots

Fonte:

FotMob

Status:

VALIDADO

---

## Shots On Target

Fonte:

FotMob

Status:

VALIDADO

---

## Big Chances

Fonte:

FotMob

Status:

VALIDADO

---

## PPDA

Fonte:

Understat

Status:

EM ESTUDO

Descrição:

Pressão defensiva por ações permitidas.

---

## Deep

Fonte:

Understat

Status:

EM ESTUDO

Descrição:

Entradas em zonas ofensivas profundas.

---

## Corners

Fonte:

FotMob

Status:

EM ESTUDO

---

## Big Chances Missed

Fonte:

FotMob

Status:

EM ESTUDO

---

## Shots Inside Box

Fonte:

FotMob

Status:

EM ESTUDO

---

## Attacking Zones

Fonte:

FotMob

Status:

VALIDADO

Descrição:

Distribuição espacial dos ataques.

Observação:

Não é série temporal.

---

## PlayerStats

Fonte:

FotMob

Status:

VALIDADO

Descrição:

Estatísticas finais de jogadores.

Observação:

Não é série temporal.

---

# Future Research

## Snapshot Providers

Investigar:

* SofaScore
* Flashscore
* FBref
* StatsBomb Open Data
* SoccerNet
* AiScore

Objetivo:

Reduzir dependência do FotMob.

---

## Multi-Source Architecture

Objetivo:

Combinar múltiplas fontes de dados.

Exemplo:

```text
Understat
+
FotMob
+
Odds
+
StatsBomb
+
SofaScore
```

para construção de modelos quantitativos de gols tardios.

---

# Current Conclusion

Situação Atual:

```text
Understat .................. OK
FotMob Match IDs ........... OK
369 partidas mapeadas ...... OK

MatchDetails ............... BLOQUEADO

Projeto .................... CONTINUAR
```

A investigação do MatchDetails deve continuar em paralelo, mas não deve bloquear a evolução do projeto.
