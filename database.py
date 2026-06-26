import sqlite3

from component import Component


class Database:

    def __init__(self):
        self.db = sqlite3.connect("data/bauteile.sqlite")
        self.db.row_factory = sqlite3.Row

    def create(self):
        c = self.db.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS components(
        mpn TEXT PRIMARY KEY,
        vds REAL,
        rdson REAL
        );
        """)

        self.db.commit()

    def add(self, comp):
        c = self.db.cursor()

        c.execute("""
        INSERT OR REPLACE INTO components
        VALUES(?,?,?)
        """, (

            comp.mpn,
            comp.vds,
            comp.rdson,

        ))

        self.db.commit()

    def find(self, mpn):
        db = sqlite3.connect("data/bauteile.sqlite")
        db.row_factory = sqlite3.Row
        c = db.cursor()

        c.execute("""
        SELECT *
        FROM components
        WHERE mpn like ?
        """, ('%'+mpn+'%',))

        row = c.fetchone()

        if row is None:
            return None

        return Component(
            row["mpn"],
            row["vds"],
            row["rdson"]
        )
