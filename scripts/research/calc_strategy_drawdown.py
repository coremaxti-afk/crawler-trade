"""Calcula drawdown por temporada para estrategias originais.

Este script nao cria estrategias, nao junta targets e nao usa filtros de playbook V3.
Ele le CSVs de entradas ja geradas pelo discovery e aplica uma configuracao JSON.

Toda simulacao financeira gerada aqui e ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
quando as odds reais nao existem no CSV de entrada.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

AVG_ODDS_BY_MINUTE = {
    60: 1.50,
    65: 1.60,
    70: 1.80,
    75: 2.00,
    80: 2.45,
    85: 3.35,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auditoria de drawdown por estrategia original.")
    parser.add_argument("--entries", nargs="+", required=True, help="Um ou mais CSVs de entradas.")
    parser.add_argument("--config", required=True, help="JSON com estrategias a testar.")
    parser.add_argument("--stake", type=float, default=100.0)
    parser.add_argument("--initial-bank", type=float, default=1000.0)
    parser.add_argument("--out-summary", required=True)
    parser.add_argument("--out-trades", required=True)
    return parser.parse_args()


def read_config(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    strategies = payload.get("strategies", [])
    if not isinstance(strategies, list) or not strategies:
        raise ValueError("Config deve conter lista nao vazia em 'strategies'.")
    return strategies


def infer_season(path: Path) -> str:
    text = path.name.lower()
    parent = str(path.parent).lower()
    probe = text + " " + parent
    if "2024_25" in probe or "2024-25" in probe or "2024_2025" in probe:
        return "EPL 2024/25"
    if (
        "2025_26" in probe
        or "2025-26" in probe
        or "2025_2026" in probe
        or text == "sportmonks_team_side_strategy_discovery_entries_v2.csv"
    ):
        return "EPL 2025/26"
    return "UNKNOWN"


def as_float(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value: Any) -> int | None:
    try:
        if value in (None, ""):
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def target_end_minute(target: str, fallback: int) -> int:
    # Ex.: goal_70_85 ou no_goal_65_90.
    for part in reversed(target.split("_")):
        if part.isdigit():
            return int(part)
    return fallback


def fallback_entry_odd(cutoff: int) -> float:
    return AVG_ODDS_BY_MINUTE.get(cutoff, 2.0)


def fallback_exit_odd(target: str, cutoff: int) -> float:
    end = target_end_minute(target, cutoff)
    return AVG_ODDS_BY_MINUTE.get(end, fallback_entry_odd(cutoff))


def load_entries(paths: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry_path in paths:
        path = Path(entry_path)
        season = infer_season(path)
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                row = dict(row)
                row.setdefault("season", season)
                if not row.get("season") or row.get("season") == "UNKNOWN":
                    row["season"] = season
                rows.append(row)
    return rows


def matches_strategy(row: dict[str, Any], strategy: dict[str, Any]) -> bool:
    row_strategy = row.get("strategy_name") or row.get("strategy")
    row_cutoff = as_int(row.get("cutoff") or row.get("cutoff_minute"))
    row_target = row.get("target")
    row_window = row.get("window")
    if row_strategy != strategy["strategy_name"]:
        return False
    if row_cutoff != int(strategy["cutoff_minute"]):
        return False
    if row_target != strategy["target"]:
        return False
    expected_window = strategy.get("window")
    if expected_window and row_window != expected_window:
        return False
    return True


def normalize_trade(row: dict[str, Any], strategy: dict[str, Any], stake: float) -> dict[str, Any]:
    cutoff = int(strategy["cutoff_minute"])
    target = strategy["target"]
    entry_odd = as_float(row.get("entry_odd")) or as_float(strategy.get("entry_odd")) or fallback_entry_odd(cutoff)
    exit_odd = as_float(row.get("exit_odd")) or as_float(strategy.get("exit_odd")) or fallback_exit_odd(target, cutoff)
    hit = as_int(row.get("hit") if row.get("hit") not in (None, "") else row.get("result")) or 0
    market_type = strategy["market_type"].lower()
    settlement = strategy["settlement"].upper()

    if market_type == "back_over" and settlement == "HOLD_FINAL":
        profit = stake * (entry_odd - 1) if hit else -stake
    elif market_type == "back_over" and settlement == "CASHOUT_ESTIMADO":
        profit = stake * (entry_odd - 1) if hit else stake * ((entry_odd / exit_odd) - 1)
    elif market_type == "lay_over" and settlement == "HOLD_FINAL":
        profit = stake if hit else -stake * (entry_odd - 1)
    elif market_type == "lay_over" and settlement == "CASHOUT_ESTIMADO":
        profit = stake * (1 - (entry_odd / exit_odd)) if hit else -stake * (entry_odd - 1)
    else:
        raise ValueError(f"market_type/settlement nao suportado: {market_type}/{settlement}")

    match_id = row.get("match_id") or row.get("fixture_id") or row.get("game_id") or ""
    date = row.get("date") or row.get("match_date") or row.get("starting_at") or ""
    window = strategy.get("window") or row.get("window") or ""
    return {
        "season": row.get("season") or "UNKNOWN",
        "match_id": match_id,
        "date": date,
        "strategy_name": strategy["strategy_name"],
        "cutoff_minute": cutoff,
        "target": target,
        "window": window,
        "market_type": market_type,
        "settlement": settlement,
        "hit": hit,
        "entry_odd": entry_odd,
        "exit_odd": exit_odd,
        "profit": profit,
        "sort_key": (row.get("season") or "UNKNOWN", date, str(match_id), cutoff, window),
        "dedupe_key": "|".join([
            row.get("season") or "UNKNOWN",
            str(match_id),
            strategy["strategy_name"],
            str(cutoff),
            target,
            window,
        ]),
    }


def streaks(outcomes: list[int]) -> tuple[int, int]:
    max_loss = max_win = cur_loss = cur_win = 0
    for outcome in outcomes:
        if outcome:
            cur_win += 1
            cur_loss = 0
        else:
            cur_loss += 1
            cur_win = 0
        max_win = max(max_win, cur_win)
        max_loss = max(max_loss, cur_loss)
    return max_loss, max_win


def verdict_for(n: int, profit: float, roi: float, ev: float, max_dd_abs: float) -> str:
    if profit <= 0 or ev <= 0:
        return "DESCARTAR"
    if n < 20 or abs(max_dd_abs) >= max(300.0, abs(profit) * 0.75):
        return "OBSERVAR"
    return "APROVADO COM RESSALVAS"


def audit(rows: list[dict[str, Any]], strategies: list[dict[str, Any]], stake: float, initial_bank: float) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    all_trades: list[dict[str, Any]] = []
    duplicate_counter: dict[tuple[str, str, str, int, str], int] = {}

    for strategy in strategies:
        selected = [row for row in rows if matches_strategy(row, strategy)]
        trades = [normalize_trade(row, strategy, stake) for row in selected]
        seen: set[str] = set()
        unique_trades: list[dict[str, Any]] = []
        dup_by_season: dict[str, int] = {}
        for trade in trades:
            if trade["dedupe_key"] in seen:
                season_key = trade["season"]
                dup_by_season[season_key] = dup_by_season.get(season_key, 0) + 1
                continue
            seen.add(trade["dedupe_key"])
            unique_trades.append(trade)
        for season_key, dup_count in dup_by_season.items():
            duplicate_counter[(season_key, strategy["strategy_name"], strategy["target"], int(strategy["cutoff_minute"]), strategy.get("window", ""))] = dup_count
        all_trades.extend(unique_trades)

    all_trades.sort(key=lambda trade: trade["sort_key"])

    summary: list[dict[str, Any]] = []
    detailed: list[dict[str, Any]] = []
    groups: dict[tuple[str, str, int, str, str], list[dict[str, Any]]] = {}
    for trade in all_trades:
        key = (trade["season"], trade["strategy_name"], trade["cutoff_minute"], trade["target"], trade["window"])
        groups.setdefault(key, []).append(trade)

    for key, trades in sorted(groups.items()):
        season, strategy_name, cutoff, target, window = key
        equity = 0.0
        peak = 0.0
        max_dd = 0.0
        outcomes: list[int] = []
        for trade in sorted(trades, key=lambda item: item["sort_key"]):
            equity += trade["profit"]
            peak = max(peak, equity)
            drawdown = equity - peak
            max_dd = min(max_dd, drawdown)
            outcomes.append(int(trade["profit"] > 0))
            trade_out = {k: v for k, v in trade.items() if k not in {"sort_key", "dedupe_key"}}
            trade_out.update({"equity": equity, "peak": peak, "drawdown": drawdown})
            detailed.append(trade_out)
        n = len(trades)
        wins = sum(outcomes)
        losses = n - wins
        profit_final = equity
        roi = profit_final / (n * stake) if n else 0.0
        ev = profit_final / n if n else 0.0
        max_loss_streak, max_win_streak = streaks(outcomes)
        sample_trade = trades[0]
        dup_count = duplicate_counter.get((season, strategy_name, target, cutoff, window), 0)
        summary.append({
            "season": season,
            "strategy_name": strategy_name,
            "cutoff_minute": cutoff,
            "target": target,
            "window": window,
            "market_type": sample_trade["market_type"],
            "settlement": sample_trade["settlement"],
            "N": n,
            "wins": wins,
            "losses": losses,
            "strike_rate": wins / n if n else 0.0,
            "profit_final": profit_final,
            "ROI": roi,
            "EV_per_trade": ev,
            "max_drawdown_abs": max_dd,
            "max_drawdown_pct": abs(max_dd) / max(initial_bank, peak, 1.0),
            "max_losing_streak": max_loss_streak,
            "max_winning_streak": max_win_streak,
            "duplicate_count": dup_count,
            "verdict": verdict_for(n, profit_final, roi, ev, max_dd),
            "note": "ESTIMATIVA OPERACIONAL COM ODDS MEDIAS",
        })
    return summary, detailed


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    strategies = read_config(Path(args.config))
    rows = load_entries(args.entries)
    summary, trades = audit(rows, strategies, args.stake, args.initial_bank)
    write_csv(Path(args.out_summary), summary)
    write_csv(Path(args.out_trades), trades)
    duplicates = sum(int(row.get("duplicate_count", 0)) for row in summary)
    print(json.dumps({
        "summary": args.out_summary,
        "trades": args.out_trades,
        "summary_rows": len(summary),
        "trades_rows": len(trades),
        "duplicate_count": duplicates,
        "note": "ESTIMATIVA OPERACIONAL COM ODDS MEDIAS",
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
