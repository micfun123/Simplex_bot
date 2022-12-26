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

    @commands.command(help="Dms all server owners")
    @commands.check(micsid)
    async def dm_owners(self,ctx,*, msg):
        owners = []
        for server in self.client.guilds:
            tosend = server.owner
            owners.append(tosend)
        owners = list(set(owners))
        for i in owners:
            try:
                await i.send(msg)
            except:
                await ctx.send(f"Counld not send to {i}")
            

    @commands.command()
    @commands.check(micsid)
    async def ghoastping(self,ctx,*,member:discord.Member):
        for i in ctx.guild.channels:
            try:
                x = await i.send(f"{member.mention}")
                await x.delete()
            except:
                print(f"Can't send message in {i}")

    @commands.command(hidden = True)
    @commands.is_owner()
    async def clearlog(self,ctx):
        file = discord.File("./other/log.txt")
        await ctx.author.send(file=file)
        dirs = 'other/'
        for f in os.listdir(dirs):  
            os.remove(os.path.join(dirs, f))
        dirs = 'tempstorage/'
        for f in os.listdir(dirs):  
            os.remove(os.path.join(dirs, f))
        await ctx.send("Cleared")
        await log("Cleared at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))	

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

    @commands.command()
    @commands.is_owner()
    async def change_status(self, ctx, *, status):
        status = status.replace("[[servers]]", str(len(self.client.guilds)))
        await self.client.change_presence(activity=discord.Game(name=status))
        await ctx.send(f"Status changed to {status}")




    



def setup(client):
    client.add_cog(BotMakerCommands(client))
