import json
import os
from pathlib import Path

import requests


BASE_URL = "https://www.sofascore.com/api/v1"

# Partida usada nos testes
DEFAULT_EVENT_ID = 14023951


class SofaScoreCollector:

    def __init__(self, output_dir="data/raw/sofascore"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36"
            ),
            "Accept": "application/json"
        })

    def _get(self, endpoint):
        url = f"{BASE_URL}{endpoint}"

        response = self.session.get(url, timeout=30)

        response.raise_for_status()

        return response.json()

    def save_json(self, event_id, filename, data):
        event_folder = self.output_dir / str(event_id)
        event_folder.mkdir(parents=True, exist_ok=True)

        filepath = event_folder / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )

        print(f"[OK] {filepath}")

    def get_event(self, event_id):
        return self._get(f"/event/{event_id}")

    def get_statistics(self, event_id):
        return self._get(f"/event/{event_id}/statistics")

    def get_incidents(self, event_id):
        return self._get(f"/event/{event_id}/incidents")

    def get_lineups(self, event_id):
        return self._get(f"/event/{event_id}/lineups")

    def get_h2h(self, event_id):
        return self._get(f"/event/{event_id}/h2h")

    def collect_match(self, event_id):

        endpoints = {
            "event.json": self.get_event,
            "statistics.json": self.get_statistics,
            "incidents.json": self.get_incidents,
            "lineups.json": self.get_lineups,
            "h2h.json": self.get_h2h,
        }

        results = {}

        print(f"\nColetando partida {event_id}\n")

        for filename, func in endpoints.items():

            try:
                data = func(event_id)

                self.save_json(
                    event_id,
                    filename,
                    data
                )

                results[filename] = "OK"

            except Exception as e:
                print(f"[ERRO] {filename}: {e}")
                results[filename] = str(e)

        return results


if __name__ == "__main__":

    EVENT_ID = DEFAULT_EVENT_ID

    collector = SofaScoreCollector()

    result = collector.collect_match(EVENT_ID)

    print("\nResumo:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
