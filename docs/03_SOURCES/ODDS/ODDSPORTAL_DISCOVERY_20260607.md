# OddsPortal Discovery - 20260607

## Escopo

Investigacao controlada da disponibilidade de odds historicas no OddsPortal/OddsAgora para a frente **ODDS HISTORICAS** do LateGoalResearch.

Esta tarefa nao implementou coletor, nao fez coleta em massa, nao alterou banco, schema, importer, dataset, features ou modelagem.

## Partida e Competicao

Competicao investigada:

- Premier League
- Temporada alvo: 2024/2025

Partida alvo do discovery:

- Arsenal x Fulham
- URL indexada: `https://www.oddsportal.com/football/england/premier-league-2024-2025/arsenal-fulham-vRiDNL8C/`

Observacao operacional:

- A URL da partida estava indexada em busca publica, mas a tentativa direta via HTTP redirecionou para a home localizada `https://www.oddsagora.com.br/`.
- A pagina de resultados da competicao foi acessivel em `https://www.oddsagora.com.br/football/england/campeonato-ingles/results/`.
- Uma tentativa anterior com outra URL indexada (`Wolves x Bournemouth`) foi descartada como partida analisada porque a rota foi convertida para pagina H2H/futura. Ela foi usada apenas como evidencia auxiliar de nomes de rotas internas observadas na aplicacao.

## Evidencias Salvas Localmente

Diretorios locais de evidencia:

- `docs/03_SOURCES/ODDS/evidence/oddsportal_20260607_arsenal_fulham/`
- `docs/03_SOURCES/ODDS/evidence/oddsportal_20260607_results_probe/`
- `docs/03_SOURCES/ODDS/evidence/oddsportal_20260607_assets/`
- `docs/03_SOURCES/ODDS/evidence/oddsportal_20260607_wolves_bournemouth/` somente como tentativa descartada/auxiliar

Arquivos principais:

- `match_page.html`
- `match_page_pl.html`
- `curl_status.txt`
- `curl_status_pl.txt`
- `results_page.html`
- `archive_payload_current.json`
- `curl_status_archive_current.txt`
- `app-DScagpaP.js`

Screenshots:

- Nao capturados nesta execucao porque o navegador interno falhou ao inicializar e o Node local estava bloqueado por permissao do ambiente. A evidencia preservada nesta rodada e HTML/status/payload observado.

## Cobertura Encontrada

| Item | Status | Evidencia |
|---|---|---|
| Pagina individual da partida | parcialmente encontrado | URL indexada para Arsenal x Fulham, mas acesso direto redirecionou para home localizada |
| Historico de odds | parcialmente encontrado | pagina de resultados da Premier League declara resultados e odds historicas |
| Opening odd | parcialmente encontrado | texto da pagina de arquivo menciona probabilidades de abertura, mas valor da partida nao foi recuperado |
| Closing odd | parcialmente encontrado | texto da pagina de arquivo menciona probabilidades de fechamento, mas valor da partida nao foi recuperado |
| Historico de movimento | parcialmente encontrado | ferramenta/tema de dropping odds existe, mas historico timestamped por partida nao foi recuperado |
| Match Odds | parcialmente encontrado | mercado 1x2 documentado no site, mas nao confirmado com payload da partida encerrada |
| Over 2.5 | parcialmente encontrado | mercado Over/Under documentado no site, mas nao confirmado com payload da partida encerrada |
| BTTS | parcialmente encontrado | mercado Ambas Marcam documentado no site, mas nao confirmado com payload da partida encerrada |
| Multiplas casas | parcialmente encontrado | site declara comparacao de mais de 80 casas, mas lista por partida nao foi recuperada |
| Timestamp das alteracoes | nao encontrado | nenhum timestamp de movimento historico foi recuperado |
| Historico live | nao encontrado | existe pagina de odds ao vivo atual, mas nao foi identificado historico live de partida encerrada |
| Exportacao acessivel | nao encontrado | nenhum CSV/PDF/API export acessivel foi identificado |
| API publica | nao encontrado | nenhuma API publica documentada foi encontrada |
| Chamada JSON usada pela pagina | parcialmente encontrado | HTML/bundle expuseram rotas internas, mas chamada direta retornou 404 |

## Mercados Encontrados

Mercados identificados como suportados conceitualmente pela plataforma:

- 1x2 / Match Odds.
- Over/Under, incluindo uso esperado para Over 2.5.
- Both Teams To Score / Ambas Marcam.

Limite desta rodada:

- Os mercados foram confirmados por conteudo da plataforma e pagina da competicao, mas nao foram recuperados como payload historico especifico da partida Arsenal x Fulham.

## Casas Encontradas

A plataforma declara comparacao de odds em mais de 80 casas de apostas.

Nesta rodada nao foi possivel recuperar uma lista estruturada de casas para a partida alvo.

Status: parcialmente encontrado.

## Opening Odds

A pagina de resultados da competicao contem texto de ajuda indicando que o arquivo de odds historicas evidencia probabilidades de abertura e fechamento.

Nao foi recuperado valor numerico de opening odd para Arsenal x Fulham.

Status: parcialmente encontrado.

## Closing Odds

A pagina de resultados da competicao contem texto de ajuda indicando probabilidades de fechamento.

Nao foi recuperado valor numerico de closing odd para Arsenal x Fulham.

Status: parcialmente encontrado.

## Movimento de Odds

O site possui conceitos/ferramentas de movimentacao de odds, como dropping odds e odds bloqueadas.

Nao foi identificado, nesta rodada, um payload historico por partida com serie temporal de alteracoes, timestamps e valores anteriores/posteriores.

Status: parcialmente encontrado.

## Odds Live

O site possui pagina de odds ao vivo para eventos em andamento.

Nao foi identificado historico live acessivel para partida encerrada.

Status: nao encontrado.

## Chamadas JSON Observadas

Foram observadas as seguintes rotas/chaves em HTML/bundle da aplicacao:

- `oddsRequest`
- `/ajax-sport-country-tournament-archive_/1/{encodedTournamentId}/`
- `requestBasePreMatch`
- `/match-event/`
- `requestBaseOddsHistory`
- `/match-event-history/`
- `requestEventData`
- `/ajax-event-data/{encodedEventId}/0`
- `requestMatchFacts`
- `/ajax-event-match-facts/{encodedEventId}/{encodedTournamentId}/`
- `requestBettingExchanges`
- `/ajax-betting-exchanges/.../`

Teste direto realizado:

- URL: `https://www.oddsagora.com.br/ajax-sport-country-tournament-archive_/1/KKay4EE8/?_=1780845000000`
- HTTP externo: 200
- Corpo retornado: `URL:/ajax-sport-country-tournament-archive_/1/KKay4EE8/ Status: 404`

Interpretação:

- A aplicacao usa rotas internas para odds/resultados.
- As rotas nao parecem reutilizaveis diretamente por chamada HTTP simples fora do contexto normal da pagina.
- Pode haver dependencia de sessao, cookies, headers, token, referer correto, bundle carregado, parametro temporal ou codificacao adicional.

## Possivel API Interna

Existe indicio de API interna, mas nao de API publica documentada.

A API interna parece expor:

- arquivo de resultados/odds por torneio;
- dados pre-match por evento;
- historico de odds por evento;
- dados do evento;
- match facts;
- betting exchanges.

Status: parcialmente encontrado.

## Riscos Operacionais

- Acesso direto a paginas antigas pode redirecionar para dominio localizado/home.
- Algumas rotas podem depender de contexto de navegador, cookies ou parametros nao triviais.
- Endpoint interno retornou 404 no corpo apesar de HTTP 200 externo.
- Browser automatizado nao ficou disponivel nesta sessao, limitando validacao visual e captura de screenshot.
- A estrutura do frontend e bundles pode mudar sem aviso.
- Uso de rotas internas exige cautela para nao virar scraping agressivo.
- Nao ha confirmacao de permissao/API publica para uso sistematico.

## Potencial para LateGoalResearch

O OddsPortal/OddsAgora tem potencial como fonte de odds historicas pre-match, especialmente para:

- closing odds;
- opening odds;
- comparacao multi-bookmaker;
- odds medias/maximas por mercado;
- possivel validacao de mercados 1x2, Over/Under e BTTS.

Pontos ainda nao comprovados:

- historico minuto a minuto ou timestamped de movimentos;
- odds live historicas para partidas encerradas;
- exportacao estruturada;
- API publica reutilizavel;
- cobertura por partida EPL 2024/25 em payload acessivel.

## Resposta a Pergunta Principal

Conseguimos recuperar diretamente nesta rodada:

- opening odds: nao diretamente; apenas evidencia textual de que a plataforma declara esse dado no arquivo historico.
- closing odds: nao diretamente; apenas evidencia textual de que a plataforma declara esse dado no arquivo historico.
- movimento de odds: nao diretamente; apenas evidencia de ferramenta/conceito de dropping odds.
- odds live historicas: nao encontrado.

Conseguimos recuperar indiretamente:

- sinais fortes de que opening/closing odds existem na camada de arquivo historico da plataforma;
- sinais de rotas internas que podem alimentar odds pre-match e odds history;
- evidencias insuficientes para afirmar disponibilidade operacional automatizavel.

## Recomendacao Final

Classificacao: **MEDIO POTENCIAL**.

Justificativa:

- Ha evidencias claras de que a plataforma possui arquivo historico de odds e menciona opening/closing odds.
- Ha sinais de rotas internas relevantes (`match-event`, `match-event-history`, `ajax-sport-country-tournament-archive_`).
- Porem, a rodada nao recuperou payload estruturado de uma partida encerrada com opening/closing/movimento/timestamps.
- Odds live historicas nao foram encontradas.

## Proxima Etapa Recomendada

Acionar Data Acquisition Engineer para um segundo discovery manual assistido por navegador real, com DevTools/Network aberto, em apenas uma partida encerrada EPL, sem coleta em massa.

Objetivo da proxima etapa:

1. Abrir a pagina individual da partida em navegador real.
2. Confirmar visualmente mercados 1x2, Over/Under 2.5 e BTTS.
3. Clicar/inspecionar odds history se houver.
4. Registrar chamadas de rede reais.
5. Confirmar se `match-event-history` retorna opening, closing, movimento e timestamps.
6. Confirmar se existe ou nao historico live.

Apenas apos essa confirmacao deve-se avaliar especificacao de coletor.

## Restricoes Respeitadas

- Apenas discovery controlado.
- Nenhum coletor implementado.
- Nenhuma coleta massiva executada.
- Nenhum banco alterado.
- Nenhum schema alterado.
- Nenhum importer criado.
- Nenhuma feature criada.
- Nenhum dataset criado.
- Nenhuma modelagem executada.
