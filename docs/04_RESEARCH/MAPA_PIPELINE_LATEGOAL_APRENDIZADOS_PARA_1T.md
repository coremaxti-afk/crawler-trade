# MAPA_PIPELINE_LATEGOAL_APRENDIZADOS_PARA_1T

Status: ATIVO

## Origem

Documento baseado no arquivo enviado pelo usuario:

```text
MAPA_PIPELINE_LATEGOAL_SCRIPTS.md
```

## Aprendizados aplicados a ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1

1. Executar por `season_id`.
2. Separar pipeline sazonal de pipeline multi-temporada.
3. Gerar artefatos auditaveis por etapa.
4. Validar outputs antes de avancar.
5. Deduplicar por fixture antes de qualquer leitura de resultado.
6. Separar discovery, validacao, radar, prospectivo e playbook.
7. Nao transformar discovery em aprovacao operacional.
8. Nao somar familias ou variacoes parecidas sem overlap/deduplicacao.
9. Criar playbook somente no final.
10. Para Corner Pro, usar primeiro como alerta paper/observacao, nao como operacao.

## Consequencia para a nova frente

A frente de primeiro tempo deve seguir uma esteira propria:

```text
1. Reconstrucao do filme do 1T.
2. Features de trajetoria.
3. Classificacao de perfis.
4. Conversao de perfis em estrategias candidatas.
5. Validacao estatistica.
6. Preparacao de alertas paper Corner Pro.
7. Validacao prospectiva dos alertas.
8. Playbook somente se houver evidencia suficiente.
```

## Regra final

O mapa LateGoal vira referencia metodologica para a engenharia analitica da frente de primeiro tempo, mas a frente de 1T nao deve copiar mecanicamente o estudo de gols tardios.
