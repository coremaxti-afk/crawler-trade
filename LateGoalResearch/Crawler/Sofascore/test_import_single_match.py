from sofascore_client import SofaScoreCollector

EVENT_ID = 14023951


def main():

    print("\n===================================")
    print("SOFASCORE SINGLE MATCH TEST")
    print("===================================\n")

    collector = SofaScoreCollector()

    try:

        print(f"Testando partida {EVENT_ID}\n")

        event = collector.get_event(EVENT_ID)

        event_data = event.get("event", {})

        print("=== EVENT ===")

        print(
            f"Mandante: "
            f"{event_data.get('homeTeam', {}).get('name')}"
        )

        print(
            f"Visitante: "
            f"{event_data.get('awayTeam', {}).get('name')}"
        )

        print(
            f"Placar: "
            f"{event_data.get('homeScore', {}).get('current')} x "
            f"{event_data.get('awayScore', {}).get('current')}"
        )

        statistics = collector.get_statistics(EVENT_ID)

        stats_count = 0

        for period in statistics.get("statistics", []):
            for group in period.get("groups", []):
                stats_count += len(
                    group.get("statisticsItems", [])
                )

        print("\n=== STATISTICS ===")
        print(f"Itens encontrados: {stats_count}")

        incidents = collector.get_incidents(EVENT_ID)

        incidents_count = len(
            incidents.get("incidents", [])
        )

        print("\n=== INCIDENTS ===")
        print(f"Eventos encontrados: {incidents_count}")

        print("\n[OK] Teste concluído")

    except Exception as e:

        print("\n[ERRO]")
        print(type(e).__name__)
        print(str(e))


if __name__ == "__main__":
    main()
