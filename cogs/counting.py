import discord
import discord
from discord.ext import commands
import json
from simpcalc import simpcalc
import asyncio
import threading

calculator = simpcalc.Calculate()

# Counting
async def counting(msg, guild, channel, m, counting):
    try:
      calc = simpcalc.Calculate()
      ans = await calc.calculate(msg)
      msg = int(ans)
    except:
     return


    db_data = counting.load_db_data()
    guild_db_data = counting.get_guild_db_data(db_data, guild)
    try:    
        counting_channel_id = int(guild_db_data["counting_channel"])
        if counting_channel_id is None:
            return
    except:
        return

    if channel.id == counting_channel_id:
        counting_data = counting.load_counting_data()
        if guild_db_data['lastcounter'] == m.author.id:
            counting_data[f"{guild.id}"] = 0
            guild_db_data['lastcounter'] = None
            counting.save_counting_data(counting_data)
            counting.save_db_data(db_data)
            await m.add_reaction("❌")
            em = discord.Embed(title=f"{m.author.name}, You ruined it!", description="Only one person at a time\nCount reset to zero")
            await channel.send(embed=em)
        else:
            guild_db_data['lastcounter'] = m.author.id
            next_number = counting_data[f"{guild.id}"] + 1
                    
            if msg == next_number:
                counting_data[f"{guild.id}"] = next_number
                counting.save_counting_data(counting_data)
                counting.save_db_data(db_data)
                await m.add_reaction("✅")
            else:
                guild_db_data['lastcounter'] = None
                counting_data[f"{guild.id}"] = 0
                counting.save_counting_data(counting_data)
                counting.save_db_data(db_data)
                em = discord.Embed(title=f"{m.author.name}, You ruined it!", description=f"You were supposed to type `{(counting_data[f'{guild.id}']+1)}`\nCount reset to zero")
                await channel.send(embed=em)
                await m.add_reaction("❌")


class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.counting_data_lock = threading.Lock()
        self.db_data_lock = threading.Lock()

    # Loads and returns counting data json object.
    # If lock is NOT set to False, save_counting_data needs to be called after this method.
    def load_counting_data(self, lock = True):
        if lock:
            self.counting_data_lock.acquire()
        with open("./databases/counting.json") as f:
            return json.load(f)

    # Loads and returns db data json object.
    # If lock is NOT set to False, save_db_data needs to be called after this method.
    def load_db_data(self, lock = True):
        if lock:
            self.db_data_lock.acquire()
        with open("./databases/db.json") as f:
            return json.load(f)

    def save_counting_data(self, counting_data):
        with open("./databases/counting.json", 'w') as f:
            json.dump(counting_data, f, indent=4)
        if self.counting_data_lock.locked():
            self.counting_data_lock.release()

    def save_db_data(self, db_data):
        with open("./databases/db.json", 'w') as f:
            json.dump(db_data, f, indent=4)
        if self.db_data_lock.locked():
            self.db_data_lock.release()

    def get_guild_db_data(self, db_data, guild):
        for datum in db_data:
            if datum["guild_id"] == guild.id:
                return datum
        return None
        
    @commands.command(aliases=['num'])
    async def numrn(self, ctx):
        guild = ctx.guild
        counting_data = self.load_counting_data(False)
        guild_id = f'{guild.id}'
        numrn = data[guild_id]
        await ctx.send(f"Current number is {numrn}")

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        msg = message.content
        guild = message.guild

        await counting(msg, guild, channel, message, self)

    def mic(ctx):
        return ctx.author.id == 481377376475938826

    # delete after usage 
    @commands.command()
    @commands.check(mic) # cmd can only be run by mic
    async def sacc(self, ctx):
        for i in self.client.guilds:
            insert = {
                "guild_id": i.id,
                "counting_channel": None,
                "lastcounter":None,
            }
            db_data = self.load_db_data()
            db_data.append(insert)
            self.save_db_data(db_data)
            
            counting_data = self.load_counting_data()
            counting_data[f"{i.id}"] = 0
            self.save_counting_data(counting_data)
            
    
    @commands.command()
    async def setcountchannel(self, ctx, channel:discord.TextChannel):
        db_data = self.load_db_data()

        guild_db_data = get_guild_db_data(db_data, ctx.guild)
        guild_db_data['counting_channel'] = channel.id

        self.save_db_data(db_data)
        await ctx.send("Done")

            
    @commands.command()
    async def countingoff(self, ctx):
        data = self.load_db_data()

        guild_db_data = get_guild_db_data(db_data, ctx.guild)
        guild_db_data['counting_channel'] = None

        self.save_db_data(db_data)
    
            
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        insert = {
            "guild_id": guild.id,
            "counting_channel": None,
            "lastcounter":None,
        }
        db_data = self.load_db_data()
        db_data.append(insert)
        self.save_db_data(db_data)

        counting_data = load_counting_data()
        counting_data[f"{guild.id}"] = 0
        self.save_counting_data(counting_data)



def setup(client):
    client.add_cog(Counting(client))
