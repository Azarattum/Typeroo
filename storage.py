import sqlite3

file = "bindings.db"

db = sqlite3.connect(file)
db.execute("""
CREATE TABLE IF NOT EXISTS bindings
    (input TEXT PRIMARY KEY, output TEXT)
""")


def setBinding(input, output):
    db.execute("INSERT OR REPLACE INTO bindings VALUES (?, ?)",
               [input, output])
    db.commit()


def removeBinding(input):
    db.execute("DELETE FROM bindings WHERE input=?", [input])
    db.commit()


def loadBindings():
    return db.execute("SELECT * FROM bindings").fetchall()
