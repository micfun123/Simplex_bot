import imp
import discord
from discord.ext import commands
import json
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
import subprocess
from discordLevelingSystem import DiscordLevelingSystem

def micsid(ctx):
    return ctx.author.id == 481377376475938826 or ctx.author.id == 624076054969188363


def log(log):
    now = datetime.now()
    timern = now.strftime("%d/%m/%Y %H:%M:%S")

    with open('./other/log.txt', 'a') as f:
        f.write('\n')
        f.write(f"{timern} | {log}")

  

cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])

class BotMakerCommands(commands.Cog):
    def __init__(self, client): 
        self.client = client 



    @commands.command(aliases=['dmr'])
    @commands.check(micsid)
    async def dmreply(self, ctx, *, msg):
        if ctx.message.reference is None:
          return
        else:
            await ctx.message.delete()
            id = ctx.message.reference.message_id
            id = await ctx.channel.fetch_message(id)
            await id.reply(msg)
            id = int(id.content)
        person = await self.client.fetch_user(id)
        await person.send(msg)

    @commands.command()
    @commands.check(micsid)
    async def logs(self, ctx):
      file = discord.File("./other/log.txt")
      await ctx.author.send(file=file)

    @commands.command()
    @commands.check(micsid)
    async def msgserver(self, ctx, id:int, *, message):
        for guild in self.client.guilds:
            if guild.id == id:
                return await guild.text_channels[0].send(message)
        await ctx.send("guild not found")

    @commands.command()
    @commands.check(micsid)
    async def reloadall(self, ctx):
        lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
        no_py = [s.replace('.py', '') for s in lst]
        startup_extensions = ["cogs." + no_py for no_py in no_py]
        startup_extensions.remove("cogs.Leveling")

        try:
            for cogs in startup_extensions:
                self.client.reload_extension(cogs)

            await ctx.send("All Reloaded")

        except Exception as e:
            print(e)
            log(e)

    @commands.command(hidden = True)
    @commands.check(micsid)
    async def pull(self, ctx):
        gitstuff = subprocess.run(["git", "pull"], capture_output=True).stdout
        await ctx.send(gitstuff.decode())
        log(gitstuff.decode())


    @commands.command(hidden = True)
    @commands.check(micsid)
    async def status(self, ctx):
        gitstuff = subprocess.run(["git", "status"], capture_output=True).stdout
        await ctx.send(gitstuff.decode())
        log(gitstuff.decode())

    @commands.command()
    @commands.check(micsid)
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Load', description=f'{extension} successfully loaded', color=0xff00c8)
        await ctx.send(embed=embed)

    


    @commands.command()
    @commands.check(micsid)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        await ctx.send(f"The module '{extension}' has been unloaded successfully!")

    @commands.command(hidden = True)
    @commands.check(micsid)
    async def newrankdb(self, ctx, extension):
        DiscordLevelingSystem.create_database_file(r'databases/')



    



def setup(client):
    client.add_cog(BotMakerCommands(client))
