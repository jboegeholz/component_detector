import sqlite3

from component import Component


class Database:

    def __init__(self):
        self.path = "data/bauteile.sqlite"

    def connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def create(self):
        db = self.connect()
        c = db.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS components(
        mpn TEXT PRIMARY KEY,
        vds REAL,
        rdson REAL
        );
        """)

        db.commit()
        db.close()

    def add(self, comp):
        db = self.connect()
        c = db.cursor()

        c.execute("""
        INSERT OR REPLACE INTO components
        VALUES(?,?,?)
        """, (

            comp.mpn,
            comp.vds,
            comp.rdson,

        ))

        db.commit()
        db.close()

    def find(self, mpn):
        db = self.connect()
        c = db.cursor()

        c.execute("""
        SELECT *
        FROM components
        WHERE mpn like ?
        """, ('%'+mpn+'%',))

        row = c.fetchone()

        if row is None:
            db.close()
            return None

        comp = Component(
            row["mpn"],
            row["vds"],
            row["rdson"]
        )

        db.close()
        return comp
