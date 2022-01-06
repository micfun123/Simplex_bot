import discord
import discord
from discord.ext import commands
import json

async def get_counting_channel(guild):
    with open("./databases/counting.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild"] == guild.id:
            return int(i["counting_channel"])
    return None

async def counting(msg, guild, channel, m):
    try:
        msg = int(msg)
    except:
        return

    cc = await get_counting_channel(guild)
    
    if cc is None:
        return
    if channel.id == cc:
        with open("./database/counting.json") as f:
            data = json.load(f)
        for i in data:
            if i['guild'] == guild.id:
                if (i['count'] +1) == msg:
                    i['count'] +=1 
                    await m.add_reaction("✅")
                else:
                    i['count'] = 0
                    await m.add_reaction("❌")
                    em = discord.Embed(title="You ruined it!", description="Count reset to zero")
                    await channel.send(embed=em)
        with open("database/counting.json", 'w') as f:
            json.dump(data, f, indent=4)


class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command()
    async def setcountchannel(self, ctx, channel:discord.TextChannel):
        with open("./database/counting.json") as f:
            data = json.load(f)
        for i in data:
            if i['guild'] == ctx.guild.id:
                i['counting_channel'] = channel.id
        with open("./database/counting.json", 'w') as f:
            json.load(data, f, indent=4)


    # run this once then delete this after
    @commands.command()
    async def setallcountingchannels(self, ctx):
        for i in self.client.guilds:
            insert = {
                "guild":ctx.guild.id,
                "counting_channel":None,
                "count":0
            }
            with open("./database/counting.json") as f:
                data = json.load(f)
            data.append(insert)
            with open("./database/counting.json", 'w') as f:
                json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):

        channel = message.channel
        msg = message.content
        guild = message.guild

        await counting(msg, guild, channel, message)

def setup(client):
    client.add_cog(Counting(client))