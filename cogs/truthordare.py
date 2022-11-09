import discord
from discord.ext import commands
import sqlite3

def enabled_check(ctx):
    con = sqlite3.connect('databases/truthordare.db')
    cur = con.cursor()
    cur.execute(f"SELECT enabled FROM guilds WHERE guild_id = {ctx.guild.id}")
    enabled = cur.fetchone()
    if enabled[0][0] == 1:
        return True

class TruthOrDare(commands.Cog):
    def __init__(self, client):
        self.client = client

    #@commands.command()
    #async def maketable(self, ctx):
    #    con = sqlite3.connect('databases/truthordare.db')
    #    cur = con.cursor()
    #    cur.execute("CREATE table truthordare (server_id int, toggel int)")
    #    con.commit()
    #    con.close()
    #    await ctx.send("Table created")
    #    for i in self.client.guilds:
    #        con = sqlite3.connect('databases/truthordare.db')
    #        cur = con.cursor()
    #        cur.execute("INSERT INTO truthordare VALUES (?, ?)", (i.id, 0))
    #        con.commit()
    #        con.close()
    #    await ctx.send("Table filled")
    #
    #onserverjoin
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        con = sqlite3.connect('databases/truthordare.db')
        cur = con.cursor()
        data = cur.execute("SELECT * FROM truthordare WHERE server_id = ?", (guild.id,))
        data = data.fetchall()
        if len(data) == 0:
            cur.execute("INSERT INTO truthordare VALUES (?, ?)", (guild.id, 0))
            con.commit()
            con.close()
        else:
            pass

    @commands.slash_command(name="truthordare_toggle", description="Toggle truth or dare",server_ids=[908963077125459989])
    @commands.has_permissions(administrator=True)
    async def truthordare_toggle(self, ctx):
        con = sqlite3.connect('databases/truthordare.db')
        cur = con.cursor()
        data = cur.execute("SELECT toggel FROM truthordare WHERE server_id = ?", (ctx.guild.id,))
        data = data.fetchall()
        #check if there is a row for the server
        if len(data) == 0:
            if data[0][0] == 0:
                cur.execute("UPDATE truthordare SET toggel = ? WHERE server_id = ?", (1, ctx.guild.id))
                con.commit()
                con.close()
                await ctx.respond("Truth or dare enabled!")
            else:
                cur.execute("UPDATE truthordare SET toggel = ? WHERE server_id = ?", (0, ctx.guild.id))
                con.commit()
                con.close()
                await ctx.respond("Truth or dare disabled!")
        else:
            cur.execute("INSERT INTO truthordare VALUES (?, ?)", (ctx.guild.id, 1))
            con.commit()
            con.close()
            await ctx.respond("Truth or dare enabled!")

    @commands.command()
    

            


def setup(client):
    client.add_cog(TruthOrDare(client))
