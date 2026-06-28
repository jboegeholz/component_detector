from component import Component
from database import Database


def main():
    db = Database()
    db.create()

    db.add(Component(
        "IRL3103PBF",
        30,
        0.0035
    ))

    db.add(Component(
        "IRLZ44N",
        55,
        0.022
    ))

    print("Datenbank initialisiert.")


if __name__ == "__main__":
    main()
