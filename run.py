# generate all the databases
import sqlite3
import json
import os


con = sqlite3.connect("databases/Welcome.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS welcome (guild_id INTEGER PRIMARY KEY, channel INTEGER, text TEXT, card_enabled INTEGER, textorembed INTEGER, enabled INTEGER)"
)

con.commit()
con.close()
print("Welcome.db created")