from database import Database
from component import Component

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

part = db.find("44")

print(part.mpn)
print(part.rds_on)