#!/usr/bin/env python3
"""
Runner simplificado para auditoria de drawdown.

Objetivo:
- Rodar o drawdown a partir dos CSVs de entries gerados pelo discovery V2.
- Receber apenas league_id e season_id da SportMonks.
- Usar league_label e season_id como marcadores nas saidas.
- Nao alterar a logica financeira do calc_strategy_drawdown.py.

Exemplo:
python run_strategy_drawdown.py --league-id 564 --season-id 25659

Use --dry-run para conferir caminhos:
python run_strategy_drawdown.py --league-id 564 --season-id 25659 --dry-run
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
REPORTS_DIR = PROJECT_ROOT / "data/processed/reports"
DEFAULT_DRAWDOWN_SCRIPT = PROJECT_ROOT / "scripts/research/calc_strategy_drawdown.py"
DEFAULT_CONFIG = PROJECT_ROOT / "configs/strategy_drawdown_config_v1.json"


def slug(value: str) -> str:
    """Normaliza texto para nome seguro de arquivo."""
    return (
        value.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
        .replace(".", "")
    )


def season_short(season_label: str) -> str:
    """Converte 2025_2026 para 2025_26, mantendo temporadas anuais como 2025."""
    parts = season_label.split("_")
    if len(parts) == 2 and all(len(part) == 4 for part in parts):
        return f"{parts[0]}_{parts[1][-2:]}"
    return season_label


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_season(league_id: int, season_id: int) -> dict[str, Any]:
    for row in load_json(LEAGUE_SEASON_MAP):
        if int(row["league_id"]) == league_id and int(row["season_id"]) == season_id:
            return row
    raise FileNotFoundError(
        f"Nao encontrei league_id={league_id} season_id={season_id} em {LEAGUE_SEASON_MAP}"
    )


def find_entries_csv(league_label: str, season_label: str, tag: str, explicit: str | None) -> Path:
    """Localiza o entries CSV do discovery para liga/temporada."""
    if explicit:
        path = Path(explicit)
        if not path.exists():
            raise FileNotFoundError(f"Entries informado nao existe: {path}")
        return path

    short = season_short(season_label)
    patterns = [
        f"sportmonks_team_side_strategy_discovery_entries_v2_{league_label}_{short}_{tag}.csv",
        f"sportmonks_team_side_strategy_discovery_entries_v2_{league_label}_{short}*.csv",
        f"*entries*v2*{league_label}*{short}*.csv",
    ]
    for pattern in patterns:
        matches = sorted(REPORTS_DIR.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        if matches:
            return matches[0]
    raise FileNotFoundError(
        "Nao encontrei entries CSV do discovery. Rode primeiro o discovery V2 simplificado. "
        f"Procurei por liga={league_label}, season={short}, tag={tag} em {REPORTS_DIR}"
    )


def read_csv_any(path: Path) -> tuple[list[dict[str, Any]], str]:
    """Le CSV detectando separador entre virgula e ponto e virgula."""
    text = path.read_text(encoding="utf-8-sig")
    first_line = text.splitlines()[0] if text.splitlines() else ""
    delimiter = ";" if first_line.count(";") > first_line.count(",") else ","
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file, delimiter=delimiter)), delimiter



def to_float(value: Any) -> float | None:
    """Converte valor numerico sem quebrar quando vier vazio."""
    try:
        if value in (None, ""):
            return None
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None


def fmt_decimal(value: Any, digits: int = 2) -> str:
    """Numero com virgula decimal para leitura no Excel PT-BR."""
    number = to_float(value)
    if number is None:
        return ""
    return f"{number:.{digits}f}".replace(".", ",")


def fmt_pct(value: Any, digits: int = 1) -> str:
    """Percentual legivel: 0.135 => 13,5%."""
    number = to_float(value)
    if number is None:
        return ""
    return f"{number * 100:.{digits}f}%".replace(".", ",")


def enrich_readable_metrics(row: dict[str, Any]) -> None:
    """Adiciona colunas formatadas sem remover os valores brutos."""
    if "strike_rate" in row:
        row["strike_rate_pct"] = fmt_pct(row.get("strike_rate"))
    if "ROI" in row:
        row["ROI_pct"] = fmt_pct(row.get("ROI"))
    if "max_drawdown_pct" in row:
        row["max_drawdown_pct_fmt"] = fmt_pct(row.get("max_drawdown_pct"))
    for source, target in [
        ("profit_final", "profit_final_fmt"),
        ("EV_per_trade", "EV_per_trade_fmt"),
        ("max_drawdown_abs", "max_drawdown_abs_fmt"),
        ("entry_odd", "entry_odd_fmt"),
        ("exit_odd", "exit_odd_fmt"),
        ("profit", "profit_fmt"),
        ("equity", "equity_fmt"),
        ("peak", "peak_fmt"),
        ("drawdown", "drawdown_fmt"),
    ]:
        if source in row:
            row[target] = fmt_decimal(row.get(source), 2)

def write_csv_excel(path: Path, rows: list[dict[str, Any]]) -> None:
    """Escreve CSV em formato amigavel ao Excel PT-BR."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    preferred = [
        "league_id",
        "league_label",
        "season_id",
        "season_label",
        "season",
        "strategy_name",
        "cutoff_minute",
        "target",
        "window",
        "market_type",
        "settlement",
        "N",
        "wins",
        "losses",
        "strike_rate_pct",
        "profit_final_fmt",
        "ROI_pct",
        "EV_per_trade_fmt",
        "max_drawdown_abs_fmt",
        "max_drawdown_pct_fmt",
        "max_losing_streak",
        "max_winning_streak",
        "profit_fmt",
        "equity_fmt",
        "drawdown_fmt",
    ]
    for field in preferred:
        if any(field in row for row in rows):
            fields.append(field)
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def add_markers(path: Path, marker: dict[str, Any]) -> int:
    """Adiciona marcadores league/season e colunas legiveis nas saidas do drawdown."""
    rows, _ = read_csv_any(path)
    for row in rows:
        # Mantem a coluna season original, mas adiciona marcadores explicitos e confiaveis.
        row["league_id"] = marker["league_id"]
        row["league_label"] = marker["league_label"]
        row["season_id"] = marker["season_id"]
        row["season_label"] = marker["season_label"]
        if not row.get("season") or row.get("season") == "UNKNOWN" or row.get("season", "").startswith("EPL"):
            row["season"] = marker["season_marker"]
        enrich_readable_metrics(row)
    write_csv_excel(path, rows)
    return len(rows)

def target_end_minute(target: str) -> int:
    """Extrai o minuto final de targets como goal_60_75 ou no_goal_65_90."""
    for part in reversed(str(target).split("_")):
        if part.isdigit():
            return int(part)
    return 90


def infer_market_type(family: str, target: str) -> str:
    """Define mercado operacional a partir da familia/target do discovery."""
    family_text = str(family).lower()
    target_text = str(target).lower()
    if "under" in family_text or target_text.startswith("no_goal"):
        return "lay_over"
    return "back_over"


def infer_settlement(target: str) -> str:
    """Targets que terminam antes de 90 usam cashout estimado; ate 90 usam hold final."""
    return "HOLD_FINAL" if target_end_minute(target) >= 90 else "CASHOUT_ESTIMADO"


def build_all_strategies_config(entries_path: Path, output_path: Path) -> tuple[Path, int]:
    """Cria config temporaria com todas as estrategias/targets/janelas do entries.csv."""
    rows, _ = read_csv_any(entries_path)
    strategies_by_key: dict[tuple[str, int, str, str], dict[str, Any]] = {}
    for row in rows:
        strategy_name = row.get("strategy_name") or row.get("strategy")
        cutoff = row.get("cutoff") or row.get("cutoff_minute")
        target = row.get("target")
        window = row.get("window")
        if not strategy_name or not cutoff or not target or not window:
            continue
        cutoff_int = int(float(cutoff))
        key = (strategy_name, cutoff_int, target, window)
        if key in strategies_by_key:
            continue
        market_type = infer_market_type(row.get("family", ""), target)
        strategies_by_key[key] = {
            "strategy_name": strategy_name,
            "cutoff_minute": cutoff_int,
            "target": target,
            "window": window,
            "market_type": market_type,
            "settlement": infer_settlement(target),
        }
    payload = {
        "description": "Config gerada automaticamente pelo run_strategy_drawdown.py com todas as estrategias do entries.csv.",
        "rules": {
            "market_type": "Under Hold/no_goal => lay_over; demais => back_over",
            "settlement": "target final < 90 => CASHOUT_ESTIMADO; target final >= 90 => HOLD_FINAL",
        },
        "strategies": list(strategies_by_key.values()),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_path, len(payload["strategies"])

def main() -> int:
    parser = argparse.ArgumentParser(description="Runner simplificado para drawdown de estrategias")
    parser.add_argument("--league-id", type=int, required=True, help="ID da liga SportMonks")
    parser.add_argument("--season-id", type=int, required=True, help="ID da temporada SportMonks")
    parser.add_argument("--league-label", help="Marcador opcional; se omitido usa o mapa SportMonks")
    parser.add_argument("--season-marker", help="Marcador opcional; se omitido usa league_label + season_label")
    parser.add_argument("--tag", default="tempos_expandidos", help="Tag usada nos arquivos do discovery")
    parser.add_argument("--entries", help="Entries CSV manual, se quiser sobrescrever a busca automatica")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config JSON manual das estrategias")
    parser.add_argument("--use-config", action="store_true", help="Usa --config manual. Por padrao, gera config com todas as estrategias do entries.csv")
    parser.add_argument("--stake", type=float, default=100.0)
    parser.add_argument("--initial-bank", type=float, default=1000.0)
    parser.add_argument("--script", default=str(DEFAULT_DRAWDOWN_SCRIPT), help="Script de drawdown base")
    parser.add_argument("--dry-run", action="store_true", help="Mostra caminhos sem executar")
    args = parser.parse_args()

    season = find_season(args.league_id, args.season_id)
    league_label = slug(args.league_label or season["league_label"])
    raw_season_label = season["season_label"]
    short = season_short(raw_season_label)
    season_marker = args.season_marker or f"{league_label}_{short}"
    entries = find_entries_csv(league_label, raw_season_label, slug(args.tag), args.entries)

    base = f"{league_label}_{short}_{slug(args.tag)}"
    out_summary = REPORTS_DIR / f"strategy_drawdown_summary_{base}.csv"
    out_trades = REPORTS_DIR / f"strategy_drawdown_trades_{base}.csv"
    generated_config = REPORTS_DIR / f"strategy_drawdown_config_all_{base}.json"
    config_path = Path(args.config)
    strategies_count = "manual"
    if not args.use_config:
        config_path, strategies_count = build_all_strategies_config(entries, generated_config)

    command = [
        sys.executable,
        str(Path(args.script)),
        "--entries",
        str(entries),
        "--config",
        str(config_path),
        "--stake",
        str(args.stake),
        "--initial-bank",
        str(args.initial_bank),
        "--out-summary",
        str(out_summary),
        "--out-trades",
        str(out_trades),
    ]

    marker = {
        "league_id": args.league_id,
        "league_label": league_label,
        "season_id": args.season_id,
        "season_label": raw_season_label,
        "season_marker": season_marker,
    }

    print("[drawdown] Configuracao resolvida")
    print(f"  Liga: {season['country']} - {season['api_name']} ({league_label})")
    print(f"  league_id: {args.league_id}")
    print(f"  season_id: {args.season_id}")
    print(f"  season_label: {raw_season_label}")
    print(f"  season_marker: {season_marker}")
    print(f"  entries: {entries}")
    print(f"  config: {config_path}")
    print(f"  strategies: {strategies_count}")
    print(f"  summary: {out_summary}")
    print(f"  trades: {out_trades}")

    if args.dry_run:
        print("[dry-run] Nenhuma execucao realizada.")
        print("[command]")
        print(" ".join(f'\"{part}\"' if " " in part else part for part in command))
        return 0

    print("[run] Executando drawdown...")
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        return result.returncode

    summary_rows = add_markers(out_summary, marker)
    trade_rows = add_markers(out_trades, marker)
    print(json.dumps({
        "summary": str(out_summary),
        "trades": str(out_trades),
        "summary_rows": summary_rows,
        "trade_rows": trade_rows,
        "league_id": args.league_id,
        "league_label": league_label,
        "season_id": args.season_id,
        "season_label": raw_season_label,
        "season_marker": season_marker,
        "strategies": strategies_count,
        "config": str(config_path),
        "note": "ESTIMATIVA OPERACIONAL COM ODDS MEDIAS",
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
