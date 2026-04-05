# generate all the databases
import sqlite3
import json
import os

os.makedirs("./databases", exist_ok=True)


# rade stuff for the anti cog
con = sqlite3.connect("databases/raids.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS raids(ServerID int, Servertoggle, raiderneed int, currentrade int)"
)
con.commit()
con.close()
print("raids.db created")


con = sqlite3.connect("databases/reactionroles.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS reactionroles(guild_id int, role_id int, emoji text)")
con.commit()
con.close()
print("reactionroles.db created")

con = sqlite3.connect("databases/autoroles.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS autoroles(guild_id int, role_id int)")
con.commit()
con.close()
print("autoroles.db created")

con = sqlite3.connect("databases/birthdays.db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS guild_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        channel_id INTEGER,
        message TEXT
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS user_birthdays (
        user_id INTEGER PRIMARY KEY,
        birthday TEXT
    )
""")
con.commit()
con.close()
print("birthdays.db created")

#    async with aiosqlite.connect("databases/verification.db") as db:
#        await db.execute("CREATE TABLE verification(ServerID int, ServerToggle, verifyChannel int, verifycode int, verifyedRole int)")
#        await db.commit()
#        await db.close()

con = sqlite3.connect("databases/verification.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS verification(ServerID int, ServerToggle, verifyChannel int, verifycode int, verifyedRole int)"
)
con.commit()
con.close()
print("verification.db created")

# Ensure counting.db exists with a clean schema
con = sqlite3.connect("databases/counting.db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS counting (
        guild_id INTEGER PRIMARY KEY,
        channel_id INTEGER,
        current_number INTEGER DEFAULT 0,
        last_user_id INTEGER,
        highest_number INTEGER DEFAULT 0
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS user_counts (
        guild_id INTEGER,
        user_id INTEGER,
        count INTEGER DEFAULT 0,
        failures INTEGER DEFAULT 0,
        PRIMARY KEY (guild_id, user_id)
    )
""")
con.commit()
con.close()
print("counting.db created")



con = sqlite3.connect("databases/blacklist.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS blacklist(id int)")
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
cur.execute("CREATE TABLE IF NOT EXISTS server(ServerID int, channel int)")
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
cur.execute("CREATE TABLE IF NOT EXISTS ticket_channel_id (userid it, channel_id int)")
con.commit()
con.close()
print("ticket_channel_id.db created")


con = sqlite3.connect("databases/qotd.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS qotd (server_id INTEGER PRIMARY KEY, channel_id INTEGER, role_id INTEGER)")
con.commit()
con.close()
print("qotd.db created")

con = sqlite3.connect("databases/truthordare.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS truthordare (server_id int, toggel int)")
con.commit()
con.close()
print("truthordare.db created")

con = sqlite3.connect("databases/Welcome.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS welcome (guild_id INTEGER PRIMARY KEY, channel integer, text text, card_enabled integer,textorembed integer, enabled integer)"
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

con = sqlite3.connect("databases/leveling.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS guild_config (guild_id INTEGER PRIMARY KEY, enabled INTEGER DEFAULT 1, wipe_on_leave INTEGER DEFAULT 0)")
cur.execute("CREATE TABLE IF NOT EXISTS ignored_channels (guild_id INTEGER, channel_id INTEGER, PRIMARY KEY (guild_id, channel_id))")
cur.execute("CREATE TABLE IF NOT EXISTS user_levels (guild_id INTEGER, user_id INTEGER, xp INTEGER DEFAULT 0, level INTEGER DEFAULT 0, total_xp INTEGER DEFAULT 0, PRIMARY KEY (guild_id, user_id))")
con.commit()
con.close()
print("leveling.db created")

con = sqlite3.connect("databases/mastodon.db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS mastodon (
        channel_id INTEGER,
        guild_id INTEGER,
        username TEXT,
        instance TEXT DEFAULT 'mastodon.social',
        mastodon_user_id TEXT,
        last_posted TEXT,
        PRIMARY KEY (channel_id, username, instance)
    )
""")
con.commit()
con.close()
print("mastodon.db created")

print("all databases created")
