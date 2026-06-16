#!/usr/bin/env python3
"""
Runner simplificado para o discovery de estrategias V2.

Objetivo:
- Evitar comandos PowerShell enormes.
- Receber apenas league_id e season_id da SportMonks.
- Encontrar automaticamente a pasta bruta SportMonks.
- Encontrar automaticamente o CSV Football-Data correspondente, quando existir.
- Gerar nomes de saida padronizados por liga/temporada.

Exemplo:
python run_strategy_discovery_v2.py --league-id 564 --season-id 25659

Use --dry-run para apenas conferir caminhos sem executar:
python run_strategy_discovery_v2.py --league-id 564 --season-id 25659 --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(r"C:\LateGoalResearch")
SPORTMONKS_COLLECTION_ROOT = PROJECT_ROOT / "data/raw/sportmonks/full_collection"
LEAGUE_SEASON_MAP = PROJECT_ROOT / "data/raw/sportmonks/league_season_map/league_last_3_seasons.json"
FOOTBALL_DATA_MAP = PROJECT_ROOT / "data/raw/football_data/football_data_league_odds_map.csv"
FOOTBALL_DATA_ROOT = PROJECT_ROOT / "data/raw/football_data"
REPORTS_DIR = PROJECT_ROOT / "data/processed/reports"
DOCS_DIR = PROJECT_ROOT / "docs/04_RESEARCH"
DEFAULT_DISCOVERY_SCRIPT = PROJECT_ROOT / "Crawler/Sportmonks/sportmonks_team_side_strategy_discovery_v2 editado.py"


def slug(value: str) -> str:
    """Normaliza texto para nome de arquivo/pasta simples."""
    return (
        value.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
        .replace(".", "")
    )


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_season(league_id: int, season_id: int) -> dict[str, Any]:
    """Busca metadata da liga/temporada no mapa SportMonks."""
    rows = load_json(LEAGUE_SEASON_MAP)
    for row in rows:
        if int(row["league_id"]) == league_id and int(row["season_id"]) == season_id:
            return row
    raise FileNotFoundError(
        f"Nao encontrei league_id={league_id} season_id={season_id} em {LEAGUE_SEASON_MAP}"
    )


def find_sportmonks_fixtures_root(league_id: int, season_id: int) -> Path:
    """Localiza a pasta 02_fixtures da coleta SportMonks."""
    pattern = f"*_league_{league_id}_season_{season_id}_*"
    candidates = sorted(SPORTMONKS_COLLECTION_ROOT.glob(pattern))
    if not candidates:
        raise FileNotFoundError(
            f"Nao encontrei coleta SportMonks com padrao {pattern} em {SPORTMONKS_COLLECTION_ROOT}"
        )
    fixtures_root = candidates[0] / "02_fixtures"
    if not fixtures_root.exists():
        raise FileNotFoundError(f"Coleta encontrada, mas falta 02_fixtures: {fixtures_root}")
    return fixtures_root


def load_football_data_mapping(league_id: int) -> dict[str, str]:
    """Carrega o codigo Football-Data correspondente ao league_id SportMonks."""
    with FOOTBALL_DATA_MAP.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            if str(row.get("sportmonks_league_id")) == str(league_id):
                return row
    raise FileNotFoundError(f"league_id={league_id} nao existe em {FOOTBALL_DATA_MAP}")


def find_football_data_csv(mapping: dict[str, str], season_label: str) -> Path:
    """Localiza o CSV Football-Data local para a liga/temporada."""
    if mapping.get("football_data_available") != "YES":
        raise FileNotFoundError(
            f"Football-Data indisponivel para {mapping.get('sportmonks_api_name')} "
            f"({mapping.get('sportmonks_country')}) no mapa local."
        )

    code = mapping["football_data_code"]
    country = slug(mapping["sportmonks_country"])
    league = slug(mapping["sportmonks_league_label"])
    direct = FOOTBALL_DATA_ROOT / country / f"{league}_{season_label}" / f"{code}_{season_label}.csv"
    if direct.exists():
        return direct

    # Fallback: busca por codigo e temporada em qualquer subpasta.
    matches = sorted(FOOTBALL_DATA_ROOT.glob(f"**/{code}_{season_label}.csv"))
    if matches:
        return matches[0]

    raise FileNotFoundError(
        "CSV Football-Data nao encontrado. Esperado em:\n"
        f"{direct}\n"
        "Baixe antes com Crawler/FootballData/football_data_odds_collector.py."
    )


def build_outputs(league_label: str, season_label: str, tag: str) -> dict[str, Path | str]:
    """Cria nomes de saida padronizados para nao sobrescrever estudos antigos."""
    season_short = season_label.replace("2025_2026", "2025_26").replace("2024_2025", "2024_25")
    base = f"{league_label}_{season_short}_{tag}"
    return {
        "season_label": base,
        "summary_csv": REPORTS_DIR / f"sportmonks_team_side_strategy_discovery_summary_v2_{base}.csv",
        "entries_csv": REPORTS_DIR / f"sportmonks_team_side_strategy_discovery_entries_v2_{base}.csv",
        "report_md": DOCS_DIR / f"SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2_{base.upper()}.md",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner simplificado do SportMonks strategy discovery V2")
    parser.add_argument("--league-id", type=int, required=True, help="ID da liga SportMonks. Ex: 564 para LaLiga")
    parser.add_argument("--season-id", type=int, required=True, help="ID da temporada SportMonks. Ex: 25659 para LaLiga 2025/26")
    parser.add_argument("--tag", default="tempos_expandidos", help="Sufixo dos arquivos de saida")
    parser.add_argument("--script", default=str(DEFAULT_DISCOVERY_SCRIPT), help="Script discovery V2 a executar")
    parser.add_argument("--dry-run", action="store_true", help="Mostra os caminhos sem executar")
    args = parser.parse_args()

    season = find_season(args.league_id, args.season_id)
    league_label = slug(season["league_label"])
    season_label = season["season_label"]
    sportmonks_root = find_sportmonks_fixtures_root(args.league_id, args.season_id)
    fd_mapping = load_football_data_mapping(args.league_id)
    football_data_csv = find_football_data_csv(fd_mapping, season_label)
    outputs = build_outputs(league_label, season_label, slug(args.tag))
    script = Path(args.script)

    command = [
        sys.executable,
        str(script),
        "--sportmonks-root",
        str(sportmonks_root),
        "--football-data-csv",
        str(football_data_csv),
        "--season-label",
        str(outputs["season_label"]),
        "--summary-csv",
        str(outputs["summary_csv"]),
        "--entries-csv",
        str(outputs["entries_csv"]),
        "--report-md",
        str(outputs["report_md"]),
    ]

    print("[discovery-v2] Configuracao resolvida")
    print(f"  Liga: {season['country']} - {season['api_name']} ({league_label})")
    print(f"  league_id: {args.league_id}")
    print(f"  season_id: {args.season_id}")
    print(f"  season_label: {season_label}")
    print(f"  SportMonks: {sportmonks_root}")
    print(f"  Football-Data: {football_data_csv}")
    print(f"  Summary: {outputs['summary_csv']}")
    print(f"  Entries: {outputs['entries_csv']}")
    print(f"  Report: {outputs['report_md']}")

    if args.dry_run:
        print("[dry-run] Nenhuma execucao realizada.")
        print("[command]")
        print(" ".join(f'\"{part}\"' if " " in part else part for part in command))
        return 0

    print("[run] Executando discovery V2...")
    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
