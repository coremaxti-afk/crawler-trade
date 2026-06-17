# MAPA_TEMPORAL_DE_GOLS_POR_LIGA_V1

## Status
PROPOSTA APROVADA PARA PESQUISA

## Objetivo
Construir o perfil temporal de gols por liga e temporada.

A pesquisa não cria estratégias novas. Seu objetivo é explicar por que estratégias existentes funcionam ou falham.

## Motivação
Uma estratégia pode parecer forte apenas porque a liga possui comportamento natural de gols naquele período.

Exemplo:
- La Liga pode apresentar menos gols entre 70-85.
- Bundesliga pode concentrar gols entre 75-90.

O estudo servirá como camada de contexto para Discovery.

## Blocos temporais
0-5
5-10
10-15
...
85-90
90+

## Métricas obrigatórias
- Jogos analisados (N)
- Total de gols
- Média de gols por jogo
- % jogos com gol
- % jogos sem gol
- Gols mandante
- Gols visitante
- Gols favorito
- Gols azarão

## Segmentações futuras
- Empatado
- Mandante vencendo por 1
- Visitante vencendo por 1
- Favorito vencendo por 1
- Favorito perdendo
- Zebra vencendo

## Uso permitido
- Validar estratégias
- Explicar padrões por liga
- Comparar temporadas

## Proibições
- Não criar modelo preditivo
- Não usar dados pós-cutoff
- Não executar trade real
- Não substituir Discovery

## Pipeline científico
Discovery -> Mapa temporal -> Break-even -> Drawdown -> Operação

## Decisão esperada
Classificar cada liga quanto à concentração temporal de gols e avaliar compatibilidade com estratégias Back Over e Lay Over.
