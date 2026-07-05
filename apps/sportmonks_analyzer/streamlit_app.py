from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from sportmonks_analyzer.analyses import (  # noqa: E402
    coverage_summary,
    data_quality_summary,
    late_goal_summary,
    odds_favorite_summary,
    pressure_window_summary,
)
from sportmonks_analyzer.loaders import load_local_path, load_uploaded_file, merge_tables  # noqa: E402


st.set_page_config(page_title="SportMonks Analyzer", layout="wide")


def _store_tables(tables: dict[str, pd.DataFrame]) -> None:
    st.session_state["tables"] = tables


def _get_tables() -> dict[str, pd.DataFrame]:
    return st.session_state.get("tables", {})


def render_sidebar() -> None:
    st.sidebar.title("Entrada de dados")
    st.sidebar.caption("Carregue JSON/CSV ou aponte para uma pasta local da coleta SportMonks.")

    uploaded_files = st.sidebar.file_uploader(
        "Arquivos JSON/CSV",
        type=["json", "csv"],
        accept_multiple_files=True,
    )

    local_path = st.sidebar.text_input(
        "Caminho local opcional",
        placeholder=r"C:\LateGoalResearch\data\raw\sportmonks\full_collection\...\02_fixtures",
    )

    if st.sidebar.button("Carregar dados", type="primary"):
        loaded = []
        for uploaded_file in uploaded_files or []:
            loaded.extend(load_uploaded_file(uploaded_file))

        if local_path.strip():
            loaded.extend(load_local_path(local_path.strip()))

        if not loaded:
            st.sidebar.warning("Nenhum dado carregado. Envie arquivos ou informe um caminho valido.")
            return

        tables = merge_tables(loaded)
        _store_tables(tables)
        st.sidebar.success(f"{len(tables)} tabela(s) carregada(s).")

    if st.sidebar.button("Limpar sessao"):
        st.session_state.pop("tables", None)
        st.sidebar.info("Tabelas removidas da sessao.")


def render_overview(tables: dict[str, pd.DataFrame]) -> None:
    st.subheader("Visao geral")
    quality = data_quality_summary(tables)
    st.dataframe(quality, use_container_width=True, hide_index=True)

    selected_table = st.selectbox("Ver amostra da tabela", options=list(tables.keys()))
    df = tables[selected_table]
    st.caption(f"Tabela `{selected_table}`: {len(df):,} linhas x {len(df.columns):,} colunas")
    st.dataframe(df.head(200), use_container_width=True)


def render_coverage(tables: dict[str, pd.DataFrame]) -> None:
    st.subheader("Cobertura SportMonks")
    coverage = coverage_summary(tables)
    if coverage.empty:
        st.info("Nao encontrei tabela `fixtures` com colunas de cobertura. Carregue uma pasta `02_fixtures` da coleta SportMonks para ativar esta visao.")
        return

    left, right = st.columns([1, 2])
    with left:
        st.dataframe(coverage, use_container_width=True, hide_index=True)
    with right:
        chart_df = coverage.set_index("category")[["coverage_pct"]]
        st.bar_chart(chart_df)


def render_late_goals(tables: dict[str, pd.DataFrame]) -> None:
    st.subheader("Gols tardios")
    threshold = st.slider("Minuto minimo", min_value=45, max_value=90, value=75, step=5)
    summary = late_goal_summary(tables.get("events"), tables.get("timeline"), minute_threshold=threshold)

    if summary.empty:
        st.info("Nao encontrei eventos de gol com as colunas esperadas de minuto/tipo.")
        return

    st.metric("Fixtures com gol tardio", f"{summary['fixture_id'].nunique() if 'fixture_id' in summary.columns else len(summary):,}")
    st.dataframe(summary, use_container_width=True, hide_index=True)


def render_pressure(tables: dict[str, pd.DataFrame]) -> None:
    st.subheader("Pressao / Trends H8")
    trends = tables.get("trends")
    if trends is None or trends.empty:
        st.info("Nao encontrei tabela `trends`. Carregue JSONs de `07_h8_pressure/trends.json` ou uma pasta `02_fixtures`.")
        return

    col1, col2 = st.columns(2)
    cutoff = col1.slider("Cutoff", min_value=45, max_value=90, value=75, step=5)
    window = col2.slider("Janela anterior ao cutoff", min_value=5, max_value=30, value=10, step=5)

    summary = pressure_window_summary(trends, cutoff=cutoff, window=window)
    if summary.empty:
        st.info("Nao consegui calcular deltas. Verifique se `trends` possui colunas de minuto, tipo e valor.")
        st.dataframe(trends.head(100), use_container_width=True)
        return

    st.dataframe(summary.head(300), use_container_width=True, hide_index=True)

    numeric = summary.select_dtypes(include="number")
    if "delta" in numeric.columns:
        st.caption("Top deltas de pressao/indicadores na janela selecionada")
        chart = summary.head(30).copy()
        label_columns = [column for column in chart.columns if column not in {"delta", "start_value", "end_value", "cutoff", "window", "start_minute"}]
        chart["label"] = chart[label_columns].astype(str).agg(" | ".join, axis=1) if label_columns else chart.index.astype(str)
        st.bar_chart(chart.set_index("label")[["delta"]])


def render_odds(tables: dict[str, pd.DataFrame]) -> None:
    st.subheader("Odds 1X2 / Favoritismo")
    odds = odds_favorite_summary(tables)
    if odds.empty:
        st.info("Nao encontrei CSV com colunas `AvgH`, `AvgD`, `AvgA`. Esta aba funciona bem com arquivos Football-Data.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Jogos com odds", f"{len(odds):,}")
    col2.metric("Odd media do favorito", f"{odds['favorite_odd'].mean():.2f}")
    col3.metric("Prob. media normalizada", f"{odds['favorite_prob_norm'].mean() * 100:.1f}%")

    band_counts = odds["favorite_band"].value_counts(dropna=False).rename_axis("faixa").reset_index(name="jogos")
    st.dataframe(band_counts, use_container_width=True, hide_index=True)
    st.bar_chart(band_counts.set_index("faixa")[["jogos"]])
    st.dataframe(odds.head(300), use_container_width=True, hide_index=True)


def main() -> None:
    st.title("SportMonks Analyzer")
    st.caption("Exploracao visual para JSON/CSV de futebol: cobertura, pressao, gols tardios, odds e base para novos padroes.")

    render_sidebar()
    tables = _get_tables()

    if not tables:
        st.info("Carregue arquivos na sidebar para iniciar. A primeira versao aceita uploads `.json`/`.csv` e leitura de pasta local SportMonks.")
        st.markdown(
            """
            **Sugestao de primeiro teste:** aponte para a pasta `02_fixtures` de uma temporada SportMonks ja coletada.

            Depois disso, use as abas para inspecionar cobertura, gols tardios, trends/pressao e odds 1X2.
            """
        )
        return

    tabs = st.tabs(["Visao geral", "Cobertura", "Gols tardios", "Pressao H8", "Odds 1X2"])
    with tabs[0]:
        render_overview(tables)
    with tabs[1]:
        render_coverage(tables)
    with tabs[2]:
        render_late_goals(tables)
    with tabs[3]:
        render_pressure(tables)
    with tabs[4]:
        render_odds(tables)


if __name__ == "__main__":
    main()
