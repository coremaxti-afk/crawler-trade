#!/usr/bin/env python3
"""
Coletor simples de CSVs de odds do Football-Data.co.uk.

Objetivo:
- Baixar arquivos CSV brutos do Football-Data para uso nos estudos do LateGoalResearch.
- Preservar o CSV original, sem transformar odds, nomes ou resultados.
- Facilitar a troca de liga e temporada via argumentos de linha de comando.

Exemplo LaLiga 2025/26:
python football_data_odds_collector.py --league-code SP1 --country spain --league-label la_liga --season 2025_2026

Observacao importante:
- Ligas principais europeias usam URL por temporada: /mmz4281/2526/SP1.csv
- Algumas ligas extras usam URL consolidada: /new/BRA.csv, /new/ARG.csv etc.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(r"C:\LateGoalResearch")
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "data" / "raw" / "football_data"

# Codigos que o Football-Data publica no padrao historico por temporada.
SEASONAL_CODES = {
    "E0", "E1", "D1", "D2", "F1", "I1", "I2", "SP1", "SP2", "N1", "B1", "P1", "T1"
}

# Codigos que o Football-Data publica no padrao extra consolidado.
# Esses arquivos normalmente contem varias temporadas no mesmo CSV.
EXTRA_CODES = {
    "ARG", "AUT", "BRA", "CHN", "DNK", "FIN", "IRL", "JPN", "MEX", "NOR",
    "POL", "ROU", "RUS", "SWE", "SWZ", "USA"
}


def season_to_football_data_code(season: str) -> str:
    """Converte 2025_2026 ou 2025-2026 para 2526."""
    normalized = season.replace("-", "_").replace("/", "_")
    parts = normalized.split("_")
    if len(parts) != 2 or not all(part.isdigit() and len(part) == 4 for part in parts):
        raise ValueError("Use temporada no formato 2025_2026, 2025-2026 ou 2025/2026.")
    return parts[0][-2:] + parts[1][-2:]


def build_url(league_code: str, season: str, source_type: str) -> str:
    """Monta a URL oficial do CSV conforme o tipo da liga."""
    code = league_code.upper()
    if source_type == "auto":
        if code in SEASONAL_CODES:
            source_type = "seasonal"
        elif code in EXTRA_CODES:
            source_type = "extra"
        else:
            raise ValueError(f"Codigo {code} nao esta no mapa interno. Use --source-type seasonal ou extra manualmente.")

    if source_type == "seasonal":
        season_code = season_to_football_data_code(season)
        return f"https://www.football-data.co.uk/mmz4281/{season_code}/{code}.csv"
    if source_type == "extra":
        return f"https://www.football-data.co.uk/new/{code}.csv"
    raise ValueError("--source-type deve ser auto, seasonal ou extra.")


def safe_slug(value: str) -> str:
    """Normaliza texto para nome de pasta simples."""
    return value.strip().lower().replace(" ", "_").replace("-", "_").replace("/", "_")


def download_csv(url: str, output_path: Path) -> int:
    """Baixa o CSV bruto e retorna o tamanho em bytes."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 LateGoalResearch/football-data-collector"})
    with urlopen(request, timeout=30) as response:
        content = response.read()
    output_path.write_bytes(content)
    return len(content)


def inspect_csv(path: Path) -> dict[str, object]:
    """Faz uma auditoria leve, sem transformar o arquivo bruto."""
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames or []
    return {
        "rows": len(rows),
        "columns_count": len(columns),
        "has_1x2_avg_odds": all(col in columns for col in ["AvgH", "AvgD", "AvgA"]),
        "has_bet365_1x2_odds": all(col in columns for col in ["B365H", "B365D", "B365A"]),
        "sample_columns": columns[:30],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Coleta CSV bruto de odds do Football-Data.co.uk")
    parser.add_argument("--league-code", required=True, help="Codigo Football-Data, ex: SP1, E0, D1, I1")
    parser.add_argument("--country", required=True, help="Pais em slug, ex: spain, england, germany")
    parser.add_argument("--league-label", required=True, help="Liga em slug, ex: la_liga, premier_league")
    parser.add_argument("--season", required=True, help="Temporada, ex: 2025_2026")
    parser.add_argument("--source-type", default="auto", choices=["auto", "seasonal", "extra"], help="Padrao de URL do Football-Data")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Raiz onde salvar o CSV bruto")
    parser.add_argument("--force", action="store_true", help="Sobrescreve arquivo existente")
    args = parser.parse_args()

    league_code = args.league_code.upper()
    season_label = args.season.replace("-", "_").replace("/", "_")
    country = safe_slug(args.country)
    league_label = safe_slug(args.league_label)

    url = build_url(league_code, season_label, args.source_type)
    output_dir = Path(args.output_root) / country / f"{league_label}_{season_label}"
    output_path = output_dir / f"{league_code}_{season_label}.csv"
    metadata_path = output_dir / "download_metadata.json"

    if output_path.exists() and not args.force:
        print(f"[skip] Arquivo ja existe: {output_path}")
        print("Use --force para baixar novamente.")
    else:
        print(f"[download] {url}")
        size = download_csv(url, output_path)
        print(f"[ok] Salvo em {output_path} ({size} bytes)")

    audit = inspect_csv(output_path)
    metadata = {
        "collected_at_local": datetime.now().isoformat(timespec="seconds"),
        "source": "Football-Data.co.uk",
        "url": url,
        "league_code": league_code,
        "country": country,
        "league_label": league_label,
        "season_label": season_label,
        "source_type": args.source_type,
        "output_path": str(output_path),
        **audit,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[audit] rows={audit['rows']} has_avg_1x2={audit['has_1x2_avg_odds']} has_b365_1x2={audit['has_bet365_1x2_odds']}")
    print(f"[metadata] {metadata_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        print(f"[erro] {exc}", file=sys.stderr)
        raise SystemExit(1)
