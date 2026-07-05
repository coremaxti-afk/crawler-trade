from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO

import pandas as pd


@dataclass
class LoadedTable:
    name: str
    source: str
    dataframe: pd.DataFrame


def _flatten_dict(value: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Flatten leve para campos aninhados sem explodir listas grandes."""
    row: dict[str, Any] = {}
    for key, item in value.items():
        clean_key = f"{prefix}{key}" if not prefix else f"{prefix}.{key}"
        if isinstance(item, dict):
            row.update(_flatten_dict(item, clean_key))
        elif isinstance(item, list):
            row[clean_key] = json.dumps(item, ensure_ascii=False)
        else:
            row[clean_key] = item
    return row


def _as_dataframe(records: Any) -> pd.DataFrame:
    if records is None:
        return pd.DataFrame()
    if isinstance(records, list):
        if not records:
            return pd.DataFrame()
        if all(isinstance(item, dict) for item in records):
            return pd.DataFrame([_flatten_dict(item) for item in records])
        return pd.DataFrame({"value": records})
    if isinstance(records, dict):
        return pd.DataFrame([_flatten_dict(records)])
    return pd.DataFrame({"value": [records]})


def _payload_data(payload: Any) -> Any:
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    return payload


def json_payload_to_tables(payload: Any, base_name: str) -> list[LoadedTable]:
    """Converte JSON generico em uma ou mais tabelas.

    A funcao tenta preservar tabelas comuns da SportMonks, mas tambem aceita JSONs
    desconhecidos para permitir exploracao inicial sem schema fixo.
    """
    data = _payload_data(payload)
    tables: list[LoadedTable] = []

    if isinstance(data, dict):
        extracted = False
        for key in ("trends", "timeline", "events", "statistics", "participants", "scores", "periods"):
            value = data.get(key)
            if isinstance(value, list):
                df = _as_dataframe(value)
                if not df.empty:
                    tables.append(LoadedTable(name=f"{base_name}_{key}", source=base_name, dataframe=df))
                    extracted = True
        if not extracted:
            df = _as_dataframe(data)
            if not df.empty:
                tables.append(LoadedTable(name=base_name, source=base_name, dataframe=df))
        return tables

    df = _as_dataframe(data)
    if not df.empty:
        tables.append(LoadedTable(name=base_name, source=base_name, dataframe=df))
    return tables


def load_uploaded_file(uploaded_file: BinaryIO) -> list[LoadedTable]:
    name = getattr(uploaded_file, "name", "uploaded_file")
    suffix = Path(name).suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(uploaded_file)
        return [LoadedTable(name=Path(name).stem, source=name, dataframe=df)]

    if suffix == ".json":
        payload = json.load(uploaded_file)
        return json_payload_to_tables(payload, Path(name).stem)

    return []


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _safe_get(payload: Any, *keys: str, default: Any = None) -> Any:
    value = payload
    for key in keys:
        if not isinstance(value, dict):
            return default
        value = value.get(key)
    return default if value is None else value


def _find_file(folder: Path, *relative_candidates: str) -> Path | None:
    for relative in relative_candidates:
        candidate = folder / relative
        if candidate.exists():
            return candidate
    return None


def _participant_map(identity_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    participants: dict[str, dict[str, Any]] = {}
    for participant in identity_data.get("participants") or []:
        location = _safe_get(participant, "meta", "location")
        if location in {"home", "away"}:
            participants[location] = {
                "participant_id": participant.get("id"),
                "team_name": participant.get("name"),
            }
    return participants


def load_sportmonks_fixture_folder(fixtures_root: Path) -> list[LoadedTable]:
    """Carrega pasta 02_fixtures da coleta SportMonks.

    Estrutura esperada por fixture:
    - 02_identity/identity.json
    - 03_match_state/match_state.json
    - 05_minute_by_minute/timeline.json
    - 07_h8_pressure/trends.json
    """
    fixture_rows: list[dict[str, Any]] = []
    event_rows: list[dict[str, Any]] = []
    timeline_rows: list[dict[str, Any]] = []
    trend_rows: list[dict[str, Any]] = []

    for fixture_dir in sorted(path for path in fixtures_root.iterdir() if path.is_dir()):
        fixture_id = fixture_dir.name

        identity_file = _find_file(fixture_dir, "02_identity/identity.json", "identity.json")
        match_state_file = _find_file(fixture_dir, "03_match_state/match_state.json", "match_state.json")
        timeline_file = _find_file(fixture_dir, "05_minute_by_minute/timeline.json", "timeline.json")
        trends_file = _find_file(fixture_dir, "07_h8_pressure/trends.json", "trends.json")

        identity_data: dict[str, Any] = {}
        if identity_file:
            identity_payload = _read_json(identity_file)
            identity_data = _payload_data(identity_payload) or {}
            fixture_id = str(identity_data.get("id") or fixture_id)

        participants = _participant_map(identity_data)
        fixture_rows.append(
            {
                "fixture_id": fixture_id,
                "folder": str(fixture_dir),
                "home_team": participants.get("home", {}).get("team_name"),
                "away_team": participants.get("away", {}).get("team_name"),
                "home_participant_id": participants.get("home", {}).get("participant_id"),
                "away_participant_id": participants.get("away", {}).get("participant_id"),
                "starting_at": identity_data.get("starting_at") or identity_data.get("starting_at_timestamp"),
                "league_id": _safe_get(identity_data, "league", "id"),
                "season_id": _safe_get(identity_data, "season", "id"),
                "has_identity": identity_file is not None,
                "has_match_state": match_state_file is not None,
                "has_timeline": timeline_file is not None,
                "has_trends": trends_file is not None,
            }
        )

        if match_state_file:
            payload = _payload_data(_read_json(match_state_file)) or {}
            for event in payload.get("events") or []:
                row = _flatten_dict(event)
                row["fixture_id"] = fixture_id
                event_rows.append(row)

        if timeline_file:
            payload = _payload_data(_read_json(timeline_file)) or {}
            timeline = payload.get("timeline") if isinstance(payload, dict) else payload
            for item in timeline or []:
                row = _flatten_dict(item)
                row["fixture_id"] = fixture_id
                timeline_rows.append(row)

        if trends_file:
            payload = _payload_data(_read_json(trends_file)) or {}
            trends = payload.get("trends") if isinstance(payload, dict) else payload
            for item in trends or []:
                row = _flatten_dict(item)
                row["fixture_id"] = fixture_id
                trend_rows.append(row)

    tables = [LoadedTable("fixtures", str(fixtures_root), pd.DataFrame(fixture_rows))]
    if event_rows:
        tables.append(LoadedTable("events", str(fixtures_root), pd.DataFrame(event_rows)))
    if timeline_rows:
        tables.append(LoadedTable("timeline", str(fixtures_root), pd.DataFrame(timeline_rows)))
    if trend_rows:
        tables.append(LoadedTable("trends", str(fixtures_root), pd.DataFrame(trend_rows)))
    return tables


def load_local_path(path_text: str) -> list[LoadedTable]:
    root = Path(path_text).expanduser()
    if not root.exists():
        raise FileNotFoundError(f"Caminho nao encontrado: {root}")

    if root.is_file():
        with root.open("rb") as file:
            return load_uploaded_file(file)

    fixtures_root = root / "02_fixtures" if (root / "02_fixtures").exists() else root
    if any(child.is_dir() for child in fixtures_root.iterdir()):
        try:
            tables = load_sportmonks_fixture_folder(fixtures_root)
            if len(tables) > 1 or not tables[0].dataframe.empty:
                return tables
        except Exception:
            pass

    tables: list[LoadedTable] = []
    for file_path in sorted(root.rglob("*")):
        if file_path.suffix.lower() not in {".csv", ".json"}:
            continue
        try:
            if file_path.suffix.lower() == ".csv":
                tables.append(LoadedTable(file_path.stem, str(file_path), pd.read_csv(file_path)))
            else:
                tables.extend(json_payload_to_tables(_read_json(file_path), file_path.stem))
        except Exception:
            continue
    return tables


def merge_tables(tables: list[LoadedTable]) -> dict[str, pd.DataFrame]:
    merged: dict[str, list[pd.DataFrame]] = {}
    for table in tables:
        if table.dataframe.empty:
            continue
        merged.setdefault(table.name, []).append(table.dataframe.assign(_source=table.source))
    return {name: pd.concat(frames, ignore_index=True, sort=False) for name, frames in merged.items()}
