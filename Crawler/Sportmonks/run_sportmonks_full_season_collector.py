#!/usr/bin/env python3
"""
Runner simplificado para coleta full season SportMonks.

Objetivo:
- Rodar o sportmonks_full_season_collector.py sem precisar lembrar labels e paths.
- Receber season_id e, quando necessario, league_id.
- Buscar country_label, league_label e season_label no mapa local.
- Preservar o coletor base sem alterar a logica de coleta.

Exemplos:
python run_sportmonks_full_season_collector.py --season-id 25659
python run_sportmonks_full_season_collector.py --league-id 564 --season-id 25659 --categories h8
python run_sportmonks_full_season_collector.py --league-id 564 --season-id 25659 --dry-run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(r"C:\LateGoalResearch")
LEAGUE_SEASON_MAP = PROJECT_ROOT / "data/raw/sportmonks/league_season_map/league_last_3_seasons.json"
DEFAULT_COLLECTOR = PROJECT_ROOT / "Crawler/Sportmonks/sportmonks_full_season_collector.py"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "data/raw/sportmonks/full_collection"


def slug(value: str) -> str:
    """Slug simples compativel com as pastas do coletor."""
    return "_".join(
        "".join(ch.lower() if ch.isalnum() else "_" for ch in value.strip()).split()
    ).strip("_")


def load_map() -> list[dict[str, Any]]:
    with LEAGUE_SEASON_MAP.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_season(season_id: int, league_id: int | None = None) -> dict[str, Any]:
    """Resolve season_id. Se houver ambiguidade, exige league_id."""
    matches = [row for row in load_map() if int(row["season_id"]) == season_id]
    if league_id is not None:
        matches = [row for row in matches if int(row["league_id"]) == league_id]
    if not matches:
        if league_id is None:
            raise FileNotFoundError(f"Nao encontrei season_id={season_id} em {LEAGUE_SEASON_MAP}")
        raise FileNotFoundError(f"Nao encontrei league_id={league_id} season_id={season_id} em {LEAGUE_SEASON_MAP}")
    if len(matches) > 1:
        options = ", ".join(
            f"league_id={row['league_id']} {row['country']} {row['api_name']}" for row in matches
        )
        raise SystemExit(
            "season_id ambiguo. Informe tambem --league-id. Opcoes encontradas: " + options
        )
    return matches[0]


def build_command(args: argparse.Namespace, season: dict[str, Any]) -> list[str]:
    command = [
        sys.executable,
        str(Path(args.collector)),
        "--league-id",
        str(season["league_id"]),
        "--season-id",
        str(season["season_id"]),
        "--country-label",
        slug(season["country"]),
        "--league-label",
        slug(season["league_label"]),
        "--season-label",
        season["season_label"],
        "--output-root",
        str(Path(args.output_root)),
        "--categories",
        args.categories,
        "--delay-min",
        str(args.delay_min),
        "--delay-max",
        str(args.delay_max),
        "--retries",
        str(args.retries),
    ]
    if args.fixture_limit is not None:
        command.extend(["--fixture-limit", str(args.fixture_limit)])
    if args.max_requests is not None:
        command.extend(["--max-requests", str(args.max_requests)])
    if args.force:
        command.append("--force")
    return command


def expected_output_folder(season: dict[str, Any], output_root: Path) -> Path:
    country = slug(season["country"])
    league = slug(season["league_label"])
    return output_root / f"{country}_{league}_league_{season['league_id']}_season_{season['season_id']}_{season['season_label']}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner simplificado da coleta full season SportMonks")
    parser.add_argument("--season-id", type=int, required=True, help="ID da temporada SportMonks")
    parser.add_argument("--league-id", type=int, help="Opcional; use quando quiser mais seguranca ou season_id for ambiguo")
    parser.add_argument("--categories", default="h8", help="h8, all, ou lista separada por virgula. Padrao: h8")
    parser.add_argument("--fixture-limit", type=int, help="Limita quantidade de jogos para teste")
    parser.add_argument("--max-requests", type=int, help="Limite maximo de requests")
    parser.add_argument("--delay-min", type=float, default=0.7)
    parser.add_argument("--delay-max", type=float, default=1.5)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--force", action="store_true", help="Sobrescreve JSONs ja coletados")
    parser.add_argument("--dry-run", action="store_true", help="Mostra comando sem executar")
    parser.add_argument("--collector", default=str(DEFAULT_COLLECTOR))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    args = parser.parse_args()

    season = find_season(args.season_id, args.league_id)
    output_folder = expected_output_folder(season, Path(args.output_root))
    command = build_command(args, season)

    print("[sportmonks-collector] Configuracao resolvida")
    print(f"  Liga: {season['country']} - {season['api_name']} ({season['league_label']})")
    print(f"  league_id: {season['league_id']}")
    print(f"  season_id: {season['season_id']}")
    print(f"  season_label: {season['season_label']}")
    print(f"  categories: {args.categories}")
    print(f"  output: {output_folder}")

    if args.dry_run:
        print("[dry-run] Nenhuma coleta realizada.")
        print("[command]")
        print(" ".join(f'\"{part}\"' if " " in part else part for part in command))
        return 0

    print("[run] Executando coleta SportMonks...")
    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
