#generate all the databases
import sqlite3

#rade stuff for the anti cog
con = sqlite3.connect("databases/raids.db")
cur = con.cursor()
cur.execute("CREATE TABLE raids(ServerID int, Servertoggle, raiderneed int, currentrade int)")
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
cur.execute("CREATE TABLE server(ServerID int, Servertoggle, birthdaychannel int,birthdaymessage text)")
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
cur.execute("CREATE TABLE verification(ServerID int, ServerToggle, verifyChannel int, verifycode int, verifyedRole int)")
con.commit()
con.close()
print("verification.db created")


        