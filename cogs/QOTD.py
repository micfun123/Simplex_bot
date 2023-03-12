import discord
from discord.ext import commands,tasks
import random
import requests
import sqlite3
from datetime import datetime,time



url = "https://the-trivia-api.com/api/questions?categories=society_and_culture,arts_and_literature,film_and_tv,food_and_drink,general_knowledge,geography,history,music,science&limit=1&difficulty=medium"

class QOTD(commands.Cog):
    ''' All the commands needed to set up question of the day
    '''
    def __init__(self, client):
        self.client = client
        self.qotd.start()

    #@commands.is_owner()
    #@commands.command()
    #async def make_file_table(self, ctx):
    #    con = sqlite3.connect('databases/qotd.db')
    #    cur = con.cursor()
    #    cur.execute("CREATE table qotd (server_id int, channel_id int)")
    #    con.commit()
    #    con.close()
    #    await ctx.send("Table created")
        



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
                await ctx.respond("QOTD channel set!")
            else:
                cur.execute("UPDATE qotd SET channel_id = ? WHERE server_id = ?", (channel.id, ctx.guild.id))
                con.commit()
                con.close()
                await ctx.respond("QOTD channel updated!")
                await ctx.followup.send("If you like the bot, please consider voting for it at https://top.gg/bot/902240397273743361 \n It helps a lot! :D", ephemeral=True)


    @commands.slash_command(name="disableqotd", description="Disable the QOTD channel")
    @commands.has_permissions(administrator=True)
    async def disableqotd(self, ctx):
        con = sqlite3.connect('databases/qotd.db')
        cur = con.cursor()
        if len(cur.execute("SELECT * FROM qotd WHERE server_id = ?", (ctx.guild.id,)).fetchall()) == 0:
            await ctx.respond("QOTD is not enabled on this server!")
        else:
            cur.execute("DELETE FROM qotd WHERE server_id = ?", (ctx.guild.id,))
            con.commit()
            con.close()
            await ctx.respond("QOTD disabled!")
        await ctx.followup.send("If you like the bot, please consider voting for it at https://top.gg/bot/902240397273743361 \n It helps a lot! :D", ephemeral=True)

    @tasks.loop(time=time(00,00))
    async def qotd(self):
        con = sqlite3.connect('databases/qotd.db')
        cur = con.cursor()
        response = requests.get(url)
        data = response.json()
        question = data[0]["question"]
        answer = data[0]["correctAnswer"]
        #get the yesterday answer from the text file
        with open("databases/qotd.txt", "r") as f:
            yesterday_answer = f.read()
            #clear the file
            f.close()
        with open("databases/qotd.txt", "w") as f:
            f.write(answer)
            f.close()
        
        
        
            
        options = data[0]["incorrectAnswers"]
        options.append(answer)
        random.shuffle(options)

        for server in cur.execute("SELECT server_id, channel_id FROM qotd").fetchall():
            try:
                channel = await self.client.fetch_channel(server[1])
                embed = discord.Embed(title="QOTD", description=question, color=0x00ff00)
                embed.add_field(name="options", value=f"{options[0]} \n {options[1]} \n {options[2]} \n {options[3]}", inline=False)
                embed.add_field(name="Answer for yesterdays QOTD is", value=f"||{yesterday_answer}||", inline=False)
                embed.set_footer(text=f"QOTD for {datetime.now().strftime('%d/%m/%Y')} \n If you like the bot, please consider voting for it at https://top.gg/bot/902240397273743361 \n It helps a lot! :D")
                await channel.send(embed=embed)
            except:
                pass
        con.close()

    @commands.command()
    @commands.is_owner()
    async def qotdtest(self, ctx):
        con = sqlite3.connect('databases/qotd.db')
        cur = con.cursor()
        response = requests.get(url)
        data = response.json()
        question = data[0]["question"]
        answer = data[0]["correctAnswer"]
        #get the yesterday answer from the text file
        with open("databases/qotd.txt", "r") as f:
            yesterday_answer = f.read()
            #clear the file
            f.close()
        with open("databases/qotd.txt", "w") as f:
            f.write(answer)
            f.close()
        
        
        
            
        options = data[0]["incorrectAnswers"]
        options.append(answer)
        random.shuffle(options)

        for server in cur.execute("SELECT server_id, channel_id FROM qotd").fetchall():
            try:
                channel = await self.client.fetch_channel(server[1])
                embed = discord.Embed(title="QOTD", description=question, color=0x00ff00)
                embed.add_field(name="options", value=f"{options[0]} \n {options[1]} \n {options[2]} \n {options[3]}", inline=False)
                embed.add_field(name="Answer for yesterdays QOTF is", value=f"||{yesterday_answer}||", inline=False)
                embed.set_footer(text=f"QOTD for {datetime.now().strftime('%d/%m/%Y')} \n If you like the bot, please consider voting for it at https://top.gg/bot/902240397273743361 \n It helps a lot! :D")
                await channel.send(embed=embed)
            except:
                pass
        con.close()
        await ctx.send("QOTD sent!")

def setup(client):
    client.add_cog(QOTD(client))
