# FOOTBALL-DATA STORAGE IMPORT SPEC

## Objetivo

Definir estrategia futura para ingestao de odds historicas Football-Data no projeto LateGoalResearch.

Esta especificacao orienta a etapa futura de armazenamento e importacao, sem autorizar implementacao imediata, migration, schema fisico, importer, features, dataset, modelagem ou backtesting.

---

## Escopo

Incluido:

- mapping entre Football-Data e SofaScore;
- estrategia staging-first;
- rastreabilidade de arquivos e registros;
- versionamento de CSVs;
- idempotencia futura;
- riscos e limitacoes da fonte.

Excluido:

- implementacao;
- schema fisico;
- migration;
- importer;
- features;
- dataset analitico;
- modelagem;
- SQL executavel.

---

## 1. Contrato de Mapping

A cadeia oficial futura deve preservar o vinculo completo entre a linha original do CSV Football-Data e a partida oficial do banco:

```text
football_data_row
-> football_data_match_key
-> sofascore_event_id
-> match_id
```

### 1.1 football_data_row

Representa a linha original do CSV bruto Football-Data, sem transformacao destrutiva.

Cada linha futura deve ser rastreavel por, no minimo:

- arquivo de origem;
- indice ou numero da linha no CSV;
- conteudo bruto preservado em staging;
- hash do arquivo de origem.

### 1.2 football_data_match_key

Representa uma chave logica derivada do CSV para permitir pareamento com a partida SofaScore.

Estrategias possiveis de matching:

- data + home_team + away_team;
- data + equipes normalizadas;
- data + equipes normalizadas + placar final, apenas como validacao auxiliar;
- mapeamento manual quando houver conflito, remarcacao, nomenclatura divergente ou ambiguidade.

O placar final pode ser usado para validar compatibilidade do pareamento, mas nao deve ser o unico criterio oficial de identidade da partida.

### 1.3 sofascore_event_id

Nenhum match Football-Data deve ser considerado confiavel sem vinculo explicito com `sofascore_event_id`.

O `sofascore_event_id` e o identificador externo principal para conectar a fonte Football-Data ao universo oficial de partidas ja coletado/importado via SofaScore.

### 1.4 match_id

O `match_id` representa a partida oficial no banco do projeto.

O vinculo futuro `football_data_row -> sofascore_event_id -> match_id` deve permitir:

- auditoria de qualquer odd ate a linha original do CSV;
- reprocessamento seguro;
- validacao de cobertura;
- deteccao de conflitos ou perdas de pareamento.

### 1.5 Regras Minimas de Confianca

- O mapping deve ser explicito.
- Conflitos de nomes devem ser resolvidos por dicionario auditavel.
- Partidas nao pareadas devem permanecer em staging com status claro.
- Partidas canceladas, adiadas ou remarcadas devem receber classificacao propria.
- Nenhum dado Football-Data deve ser promovido a armazenamento definitivo sem mapping confiavel para `sofascore_event_id`.

---

## 2. Estrategia Staging-First

Football-Data deve passar primeiro por staging.

Fluxo futuro:

```text
CSV bruto
-> staging
-> validacao
-> mapping
-> armazenamento definitivo
```

### 2.1 CSV Bruto

O CSV original deve ser preservado integralmente como fonte primaria.

O arquivo bruto nao deve ser tratado como dataset analitico, feature store ou tabela final.

### 2.2 Staging

A camada de staging deve receber os dados do CSV de forma fiel, preservando:

- nomes originais das colunas;
- valores originais;
- linhas nao pareadas;
- colunas ainda nao utilizadas;
- metadados da fonte.

Objetivos do staging:

- preservar a fonte original;
- permitir reprocessamento;
- evitar perda de informacao;
- separar validacao de armazenamento definitivo;
- registrar problemas de qualidade sem descartar dados prematuramente.

### 2.3 Validacao

Antes do armazenamento definitivo, a validacao deve verificar:

- total de linhas;
- total de partidas validas;
- colunas esperadas;
- mercados disponiveis;
- cobertura de odds;
- linhas duplicadas ou suspeitas;
- tipos de dados esperados;
- integridade do mapping para SofaScore.

### 2.4 Mapping

O mapping deve ocorrer apos staging e validacao estrutural.

Ele deve produzir uma relacao auditavel entre a linha Football-Data e a partida oficial SofaScore/PostgreSQL.

### 2.5 Armazenamento Definitivo

Somente registros validados e pareados de forma confiavel devem ser promovidos a armazenamento definitivo futuro.

Registros sem mapping confiavel devem permanecer em staging ou em tabela/estrutura de status, sem contaminarem a camada final.

---

## 3. Estrutura Futura de Armazenamento

Esta secao define conceitos de armazenamento futuro, sem definir schema fisico.

### 3.1 Mercado 1X2

O armazenamento futuro deve representar odds historicas para o mercado 1X2:

- `home_win`;
- `draw`;
- `away_win`.

Esses campos representam os tres resultados possiveis do tempo regulamentar conforme a convencao da fonte Football-Data.

### 3.2 Over/Under 2.5

O armazenamento futuro deve representar odds do mercado de total de gols 2.5:

- `over_2_5`;
- `under_2_5`.

Esses campos devem preservar a origem e o tipo da odd, sem conversao prematura para probabilidade implicita na etapa de importacao.

### 3.3 Asian Handicap

O armazenamento futuro deve representar odds de Asian Handicap quando presentes:

- `handicap_line`;
- `home_handicap`;
- `away_handicap`.

A linha de handicap deve ser preservada exatamente conforme a fonte, com validacao posterior para formatos decimais, quartos de linha ou convencoes especificas da casa/bookmaker.

### 3.4 Odds

As odds devem ser separadas conceitualmente por tipo:

- `opening_like_odds`;
- `closing_odds`;
- `average_odds`;
- `maximum_odds`.

#### opening_like_odds

Representa odds que parecem refletir abertura, pre-close ou snapshot anterior ao fechamento, conforme nomenclatura e disponibilidade da fonte.

Como Football-Data pode nao fornecer opening odds explicitamente para todos os bookmakers/mercados, qualquer classificacao como opening-like deve ser documentada e validada antes de uso analitico.

#### closing_odds

Representa odds de fechamento ou odds finais disponiveis no CSV.

Closing odds devem ser tratadas com cuidado metodologico, pois podem refletir informacao acumulada ate proximo do kickoff. Para uso pre-jogo, o momento de disponibilidade deve ser documentado.

#### average_odds

Representa medias agregadas por mercado quando fornecidas pela fonte.

Essas odds podem resumir multiplas casas, mas devem preservar o tipo de agregacao original.

#### maximum_odds

Representa melhores odds/maximas por mercado quando fornecidas pela fonte.

Devem ser usadas com cautela em estudos futuros, pois podem representar disponibilidade teorica e nao necessariamente odds executaveis por um operador especifico.

### 3.5 Separacao Conceitual Obrigatoria

O armazenamento futuro deve distinguir:

- mercado;
- selecao;
- bookmaker ou agregador;
- tipo da odd;
- arquivo de origem;
- versao do arquivo;
- partida oficial vinculada.

Nenhuma odd deve ser misturada a tabelas de eventos in-game, match statistics, features ou datasets analiticos nesta etapa.

---

## 4. Rastreabilidade

Todo registro futuro deve preservar:

- `source_file`;
- `source_url`;
- `source_hash`;
- `imported_at`.

### 4.1 source_file

Identifica o arquivo bruto usado como origem.

Deve permitir localizar a versao exata do CSV processado.

### 4.2 source_url

Identifica a URL publica ou origem declarada do arquivo.

Quando a fonte mudar a URL ou substituir conteudo no mesmo endereco, `source_hash` deve ser usado para diferenciar versoes.

### 4.3 source_hash

Identifica o conteudo do arquivo bruto.

O hash deve ser calculado sobre o conteudo real do CSV, permitindo detectar:

- arquivo novo;
- arquivo alterado;
- reprocessamento de versao ja conhecida;
- divergencia entre arquivos com mesmo nome.

### 4.4 imported_at

Registra o momento em que a versao foi processada pelo pipeline futuro.

Esse campo deve apoiar auditoria operacional, sem substituir `source_hash` como identificador de conteudo.

### 4.5 Objetivo da Rastreabilidade

A rastreabilidade deve permitir reconstruir a origem de qualquer valor armazenado:

```text
valor armazenado
-> mercado/selecao/bookmaker/tipo
-> partida oficial
-> linha Football-Data
-> CSV bruto
-> source_url/source_hash
```

---

## 5. Estrategia de Versionamento dos CSVs

### 5.1 Regra Principal

CSV bruto nunca deve ser sobrescrito.

Cada versao deve ser preservada.

### 5.2 Versionamento Logico

A estrategia recomendada e versionar logicamente cada CSV por:

- competicao;
- temporada;
- data de aquisicao;
- nome original do arquivo;
- `source_hash`.

Exemplo conceitual:

```text
football_data
-> england
-> premier_league_2024_2025
-> versions
-> acquisition_date + source_hash
```

Esta estrutura e apenas conceitual; nao define schema fisico nem obriga layout definitivo.

### 5.3 Identificacao de Conteudo

`source_hash` deve identificar o conteudo, nao apenas o caminho.

Dois arquivos com o mesmo nome e conteudos diferentes devem ser tratados como versoes distintas.

Dois arquivos com nomes diferentes e mesmo conteudo podem ser reconhecidos como duplicatas logicas.

### 5.4 Reprocessamento

O reprocessamento deve ser possivel para qualquer versao preservada.

Um importer futuro deve conseguir:

- processar uma versao especifica;
- comparar versoes;
- detectar mudancas;
- atualizar staging com seguranca;
- preservar historico de processamento.

---

## 6. Estrategia de Idempotencia

### 6.1 Regras Gerais

O importer futuro deve ser idempotente.

Reexecutar o importer com a mesma versao do CSV nao pode duplicar registros.

Alteracoes de CSV devem ser detectadas via `source_hash`.

Staging deve permitir reprocessamento seguro.

### 6.2 Idempotencia em Staging

A camada de staging deve identificar registros pela combinacao conceitual de:

- fonte;
- competicao;
- temporada;
- versao do arquivo;
- linha original;
- `source_hash`.

Essa combinacao deve impedir duplicidade logica sem exigir descarte de versoes historicas.

### 6.3 Idempotencia no Armazenamento Definitivo

A camada definitiva futura deve impedir duplicidade por partida, mercado, selecao, bookmaker/agregador, tipo de odd e versao de origem, conforme contrato tecnico aprovado pelo CTO.

Esta especificacao nao define constraint fisica.

### 6.4 Mudancas de CSV

Quando o mesmo CSV publico mudar de conteudo:

- o novo conteudo deve receber novo `source_hash`;
- a versao anterior deve ser preservada;
- o impacto da mudanca deve ser auditavel;
- registros derivados devem apontar para a versao correta.

---

## 7. Riscos e Limitacoes da Fonte

### 7.1 Diferencas de Nomenclatura de Equipes

Football-Data e SofaScore usam nomes diferentes para algumas equipes.

Exemplos ja observados:

- `Man United` vs `Manchester United`;
- `Man City` vs `Manchester City`;
- `Nott'm Forest` vs `Nottingham Forest`;
- `Wolves` vs `Wolverhampton`;
- `Brighton` vs `Brighton & Hove Albion`;
- `Tottenham` vs `Tottenham Hotspur`;
- `West Ham` vs `West Ham United`.

O uso de dicionario explicito e obrigatorio para mapping confiavel.

### 7.2 Partidas Remarcadas

Partidas remarcadas podem gerar divergencia de data/hora entre fontes.

O mapping futuro deve considerar:

- data original;
- data realizada;
- horario local;
- timezone;
- tolerancia documentada para diferencas de horario.

### 7.3 Partidas Canceladas

Partidas canceladas ou nao realizadas nao devem ser promovidas automaticamente a armazenamento definitivo.

Elas devem receber status proprio em staging/mapping.

### 7.4 Mudancas Historicas de Mercado

Bookmakers, mercados e nomes de colunas podem mudar entre temporadas.

O contrato futuro nao deve assumir que todas as temporadas terao exatamente as mesmas colunas.

### 7.5 Ausencia Eventual de Odds

Algumas partidas, mercados ou bookmakers podem ter odds ausentes.

Ausencia deve ser registrada como dado faltante, nao inferida.

### 7.6 Diferencas entre Football-Data e SofaScore

As fontes podem divergir em:

- nomes de equipes;
- horario;
- competicao;
- status da partida;
- placar;
- partidas adiadas/remarcadas;
- cobertura historica.

Essas diferencas devem ser tratadas no mapping e na validacao, antes de qualquer uso analitico.

### 7.7 Necessidade de Match Mapping Confiavel

Football-Data so deve avancar para ingestao definitiva quando o mapping com SofaScore for confiavel.

O criterio exploratorio atual indica alto potencial quando:

- pareamento >= 95%;
- conflitos resolviveis por dicionario explicito;
- placar compativel;
- sem ambiguidade relevante.

---

## Status da Especificacao

Status:

**PRONTA PARA REVISAO CTO**

Criterios de aceite:

- documento completo;
- sem schema;
- sem migration;
- sem importer;
- sem features;
- sem modelagem;
- sem SQL;
- sem codigo.
