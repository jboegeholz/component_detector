from database import Database


def main():
    db = Database()
    part = db.find("44")

    if part is None:
        raise SystemExit("Test fehlgeschlagen: Bauteil mit MPN-Teilstring '44' nicht gefunden.")

    print(part.mpn)
    print(part.rdson)


if __name__ == "__main__":
    main()
