import os
import sys

from nexar_api import NexarApi


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Nutzung: python3 octopart_search.py <MPN>")

    client_id = os.environ.get("NEXAR_CLIENT_ID")
    client_secret = os.environ.get("NEXAR_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise SystemExit(
            "Bitte NEXAR_CLIENT_ID und NEXAR_CLIENT_SECRET als Umgebungsvariablen setzen."
        )

    result = NexarApi(client_id, client_secret).search_mpn(sys.argv[1])
    print_result(result)


def print_result(result):
    print("Treffer:", result["hits"])

    for item in result["results"]:
        part = item["part"]
        manufacturer = part.get("manufacturer") or {}

        print()
        print("MPN:", part.get("mpn", ""))
        print("Hersteller:", manufacturer.get("name", ""))
        print("Octopart:", part.get("octopartUrl", ""))

        sellers = part.get("sellers") or []
        for seller in sellers[:5]:
            company = seller.get("company") or {}
            offers = seller.get("offers") or []
            first_price = first_offer_price(offers)

            if first_price is None:
                print("  -", company.get("name", ""))
            else:
                quantity = first_price.get("quantity", "")
                price = first_price.get("price", "")
                print(f"  - {company.get('name', '')}: ab {quantity} Stueck, {price}")


def first_offer_price(offers):
    for offer in offers:
        prices = offer.get("prices") or []
        if prices:
            return prices[0]

    return None


if __name__ == "__main__":
    main()
