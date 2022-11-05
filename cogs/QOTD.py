import discord
from discord.ext import commands,tasks
import random
import requests
import sqlite3
from datetime import datetime,time



url = "https://the-trivia-api.com/api/questions?categories=general_knowledge,food_and_drink&limit=1&difficulty=medium"

class QOTD(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.qotd.start()

    @commands.is_owner()
    @commands.command()
    async def make_file_table(self, ctx):
        con = sqlite3.connect('databases/qotd.db')
        cur = con.cursor()
        cur.execute("CREATE table qotd (server_id int, channel_id int)")
        con.commit()
        con.close()
        await ctx.send("Table created")
        



    @commands.slash_command(name="setqotd", description="Set the QOTD channel")
    @commands.has_permissions(administrator=True)
    async def setqotd(self, ctx, channel: discord.TextChannel):
            con = sqlite3.connect('databases/qotd.db')
            cur = con.cursor()
            data = cur.execute("SELECT * FROM qotd WHERE server_id = ?", (ctx.guild.id,))
            data = data.fetchall()
            if len(data) == 0:
                cur.execute("INSERT INTO qotd VALUES (?, ?)", (ctx.guild.id, channel.id))
                con.commit()
                con.close()
                await ctx.respond("QOTD channel set!", ephemeral=True)
            else:
                cur.execute("UPDATE qotd SET channel_id = ? WHERE server_id = ?", (channel.id, ctx.guild.id))
                con.commit()
                con.close()
                await ctx.respond("QOTD channel updated!", ephemeral=True)

    @tasks.loop(time=time(00,00))
    async def qotd(self):
        con = sqlite3.connect('databases/qotd.db')
        cur = con.cursor()
        response = requests.get(url)
        data = response.json()
        question = data[0]["question"]
        answer = data[0]["correctAnswer"]
        for server in cur.execute("SELECT server_id, channel_id FROM qotd").fetchall():
            channel = self.client.get_channel(server[1])
            embed = discord.Embed(title="QOTD", description=question, color=0x00ff00)
            embed.add_field(name="Answers", value=f"||{answer}||", inline=False)
            await channel.send(embed=embed)
        con.close()

def setup(client):
    client.add_cog(QOTD(client))
