# generate all the databases
import sqlite3
import json
import os

# rade stuff for the anti cog
con = sqlite3.connect("databases/raids.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE raids(ServerID int, Servertoggle, raiderneed int, currentrade int)"
)
con.commit()
con.close()
print("raids.db created")


con = sqlite3.connect("databases/autoroles.db")
cur = con.cursor()
cur.execute("CREATE TABLE autoroles(guild_id int, role_id int)")
con.commit()
con.close()
print("autoroles.db created")

con = sqlite3.connect("databases/server_brithdays.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE server(ServerID int, Servertoggle, birthdaychannel int,birthdaymessage text)"
)
con.commit()
con.close()
print("server_brithdays.db created")
con = sqlite3.connect("databases/user_brithdays.db")
cur = con.cursor()
cur.execute("CREATE TABLE birthday(UsersID int, birthday)")
con.commit()
con.close()
print("user_brithdays.db created")

#    async with aiosqlite.connect("databases/verification.db") as db:
#        await db.execute("CREATE TABLE verification(ServerID int, ServerToggle, verifyChannel int, verifycode int, verifyedRole int)")
#        await db.commit()
#        await db.close()

con = sqlite3.connect("databases/verification.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE verification(ServerID int, ServerToggle, verifyChannel int, verifycode int, verifyedRole int)"
)
con.commit()
con.close()
print("verification.db created")


con = sqlite3.connect("databases/counting.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE counting (guild_id INTEGER, counting_channel INTEGER, lastcounter INTEGER,highest INTEGER, last_user INTEGER,attemps INTEGER DEFAULT 0)"
)
con.commit()
con.close()
print("counting.db created")


con = sqlite3.connect("databases/blacklist.db")
cur = con.cursor()
cur.execute("CREATE TABLE blacklist(id int)")
con.commit()
con.close()
print("blacklist.db created")


con = sqlite3.connect("databases/Goodbye.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS goodbye (guild_id INTEGER PRIMARY KEY, channel integer, text text, card_enabled integer,textorembed integer, enabled integer)"
)
con.commit()
con.close()
print("Goodbye.db created")


con = sqlite3.connect("databases/announcement.db")
cur = con.cursor()
cur.execute("CREATE TABLE server(ServerID int, channel int)")
con.commit()
con.close()
print("announcement.db created")

# make the log.json file
if not os.path.exists("./databases/log.json"):
    with open("./databases/log.json", "w") as f:
        json.dump({}, f, indent=4)
        print("log.json created")


con = sqlite3.connect("databases/rss.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS rss (name text, url text, channel text,guild text,lastpost text)"
)
con.commit()
con.close()
print("rss.db created")


con = sqlite3.connect("databases/ticket_channel_id.db")
cur = con.cursor()
cur.execute("CREATE table ticket_channel_id (userid it, channel_id int)")
con.commit()
con.close()
print("ticket_channel_id.db created")


con = sqlite3.connect("databases/qotd.db")
cur = con.cursor()
cur.execute("CREATE table qotd (server_id int, channel_id int)")
con.commit()
con.close()
print("qotd.db created")

con = sqlite3.connect("databases/truthordare.db")
cur = con.cursor()
cur.execute("CREATE table truthordare (server_id int, toggel int)")
con.commit()
con.close()
print("truthordare.db created")

con = sqlite3.connect("databases/Welcome.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS welcome (guild_id integer, channel integer, text text, card_enabled integer,textorembed integer, enabled integer)"
)
con.commit()
con.close()
print("Welcome.db created")


con = sqlite3.connect("databases/log.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS log (GuildID INTEGER, ChannelID INTEGER)")
con.commit()
con.close()
print("log.db created")

con = sqlite3.connect("databases/mastodon.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS mastodon (channel_id int, guild_id int, username text,last_posted text)"
)
con.commit()
con.close()
print("mastodon.db created")

print("all databases created")
