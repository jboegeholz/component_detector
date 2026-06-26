from database import Database
from component import Component

db = Database()
db.create()

db.add(Component(
    "IRL3103PBF",
    30,
    True
))

part = db.find("IRL3103PBF")

print(part.mpn)
print(part.rds_on)