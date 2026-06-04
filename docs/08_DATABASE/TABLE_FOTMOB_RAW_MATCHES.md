# TABLE FOTMOB_RAW_MATCHES

## Tipo

Staging / Raw Layer

## Objetivo

Armazenar payloads brutos do FotMob para reprocessamento futuro.

## Campos

- fotmob_match_id
- json_data
- created_at

## Papel Arquitetural

FotMob API
→ JSON Bruto
→ Transformações
→ Banco Analítico
