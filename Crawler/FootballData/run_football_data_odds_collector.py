#!/usr/bin/env python3
"""
Runner simplificado para baixar odds Football-Data.

Objetivo:
- Receber apenas league_id e season_id da SportMonks.
- Descobrir automaticamente o codigo Football-Data da liga.
- Descobrir automaticamente country, league_label e season_label.
- Chamar o coletor oficial football_data_odds_collector.py.

Exemplo:
python run_football_data_odds_collector.py --league-id 564 --season-id 25659

Use --dry-run para conferir sem baixar:
python run_football_data_odds_collector.py --league-id 564 --season-id 25659 --dry-run
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
LEAGUE_SEASON_MAP = PROJECT_ROOT / "data/raw/sportmonks/league_season_map/league_last_3_seasons.json"
FOOTBALL_DATA_MAP = PROJECT_ROOT / "data/raw/football_data/football_data_league_odds_map.csv"
DEFAULT_COLLECTOR = PROJECT_ROOT / "Crawler/FootballData/football_data_odds_collector.py"


def slug(value: str) -> str:
    """Normaliza texto para nome de pasta simples."""
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
    """Busca liga/temporada no mapa SportMonks."""
    for row in load_json(LEAGUE_SEASON_MAP):
        if int(row["league_id"]) == league_id and int(row["season_id"]) == season_id:
            return row
    raise FileNotFoundError(
        f"Nao encontrei league_id={league_id} season_id={season_id} em {LEAGUE_SEASON_MAP}"
    )


def find_football_data_mapping(league_id: int) -> dict[str, str]:
    """Busca codigo Football-Data pelo league_id SportMonks."""
    with FOOTBALL_DATA_MAP.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            if str(row.get("sportmonks_league_id")) == str(league_id):
                return row
    raise FileNotFoundError(f"league_id={league_id} nao existe em {FOOTBALL_DATA_MAP}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner simplificado do coletor Football-Data")
    parser.add_argument("--league-id", type=int, required=True, help="ID da liga SportMonks. Ex: 564 para LaLiga")
    parser.add_argument("--season-id", type=int, required=True, help="ID da temporada SportMonks. Ex: 25659 para 2025/26")
    parser.add_argument("--collector", default=str(DEFAULT_COLLECTOR), help="Coletor Football-Data a chamar")
    parser.add_argument("--dry-run", action="store_true", help="Mostra comando sem baixar")
    parser.add_argument("--force", action="store_true", help="Forca novo download se arquivo ja existir")
    args = parser.parse_args()

    season = find_season(args.league_id, args.season_id)
    mapping = find_football_data_mapping(args.league_id)

    if mapping.get("football_data_available") != "YES":
        raise SystemExit(
            f"Football-Data nao disponivel para league_id={args.league_id} "
            f"({mapping.get('sportmonks_country')} - {mapping.get('sportmonks_api_name')})."
        )

    league_code = mapping["football_data_code"]
    country = slug(mapping["sportmonks_country"])
    league_label = slug(mapping["sportmonks_league_label"])
    season_label = season["season_label"]
    source_type = mapping.get("football_data_source_type") or "auto"
    collector = Path(args.collector)

    command = [
        sys.executable,
        str(collector),
        "--league-code",
        league_code,
        "--country",
        country,
        "--league-label",
        league_label,
        "--season",
        season_label,
        "--source-type",
        source_type,
    ]
    if args.force:
        command.append("--force")

    print("[football-data] Configuracao resolvida")
    print(f"  Liga: {season['country']} - {season['api_name']} ({league_label})")
    print(f"  league_id: {args.league_id}")
    print(f"  season_id: {args.season_id}")
    print(f"  season_label: {season_label}")
    print(f"  football_data_code: {league_code}")
    print(f"  source_type: {source_type}")

    if args.dry_run:
        print("[dry-run] Nenhum download realizado.")
        print("[command]")
        print(" ".join(f'\"{part}\"' if " " in part else part for part in command))
        return 0

    print("[run] Baixando Football-Data...")
    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
