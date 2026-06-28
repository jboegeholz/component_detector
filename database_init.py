from component import Component
from database import Database


def main():
    db = Database()
    db.create()

    db.add(Component(
        "IRFZ44V",
        manufacturer="International Rectifier",
        channel_type="n-channel",
        vds=60,
        rdson=0.0165,
        continous_drain_current=55
    ))
    db.add(Component(
        "IRFZ44N",
        manufacturer="International Rectifier",
        channel_type="n-channel",
        vds=55,
        rdson=0.0175,
        continous_drain_current=49
    ))
    db.add(Component(
        "IRLZ44Z",
        manufacturer="International Rectifier",
        channel_type="n-channel",
        vds=55,
        rdson=0.0135,
        continous_drain_current=51
    ))
    db.add(Component(
        "IRF830",
        manufacturer="International Rectifier",
        channel_type="n-channel",
        vds=500,
        rdson=1.5,
        continous_drain_current=4.5
    ))
    db.add(Component(
        "IRF9540",
        manufacturer="International Rectifier",
        channel_type="p-channel",
        vds=-100,
        rdson=0.2,
        continous_drain_current=-19
    ))
    print("Datenbank initialisiert.")


if __name__ == "__main__":
    main()
