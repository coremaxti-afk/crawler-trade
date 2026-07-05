# SportMonks Analyzer App

Aplicacao Streamlit para explorar dados coletados da SportMonks em JSON e CSV.

A ideia desta primeira versao e ser simples, mas evolutiva: ela carrega arquivos brutos, normaliza estruturas comuns da SportMonks, mostra qualidade/cobertura dos dados e executa primeiras analises de pressao, gols tardios e odds 1X2 quando o CSV possuir odds de mercado.

## Por que existe

O projeto LateGoalResearch ja tem coletores e scripts de discovery. Este app cria uma camada visual para investigar rapidamente:

- quais arquivos foram carregados;
- quais colunas e tabelas existem;
- cobertura por fixture;
- eventos de gol tardio;
- tendencias/pressao H8 por minuto;
- favoritos pre-jogo quando houver colunas `AvgH`, `AvgD`, `AvgA`.

## Como rodar

A partir da raiz do repositorio:

```bash
cd apps/sportmonks_analyzer
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

No Linux/Mac:

```bash
cd apps/sportmonks_analyzer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Formas de entrada

O app aceita duas formas:

1. Upload manual de arquivos `.json` e `.csv` na sidebar.
2. Caminho local para uma pasta ja existente, por exemplo:

```text
C:\LateGoalResearch\data\raw\sportmonks\full_collection\england_premier_league_league_8_season_25583_2025_2026\02_fixtures
```

Tambem funciona apontando para a pasta da temporada acima de `02_fixtures`; o loader tenta detectar automaticamente a subpasta correta.

## Estrutura

```text
apps/sportmonks_analyzer/
  streamlit_app.py
  requirements.txt
  sportmonks_analyzer/
    __init__.py
    loaders.py
    analyses.py
```

## Como evoluir

Para adicionar uma nova analise:

1. Crie uma funcao em `sportmonks_analyzer/analyses.py`.
2. Retorne um `pandas.DataFrame` ou um dicionario simples.
3. Adicione uma nova aba em `streamlit_app.py`.

Exemplos de proximas analises:

- padroes por cutoff 60/65/70/75;
- pressao acumulada antes do gol;
- under hold apos minuto X;
- comparacao favorita vs zebra;
- score state no cutoff;
- validacao de leakage entre `statistics`, `xgfixture` e snapshots temporais.

## Observacao importante

Este app nao substitui os scripts de coleta e discovery existentes. Ele fica como camada de exploracao e pode chamar ou reaproveitar esses scripts depois.