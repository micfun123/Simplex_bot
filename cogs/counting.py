import discord
import discord
from discord.ext import commands
import json
from simpcalc import simpcalc
import asyncio
calculator = simpcalc.Calculate()

async def get_counting_channel(guild):
    with open("./databases/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == guild.id:
            return int(i["counting_channel"])
    return None

# Counting


async def counting(msg, guild, channel, m):
    try:
      calc = simpcalc.Calculate()
      ans = await calc.calculate(msg)
      msg = int(ans)
    except:
     return    

    cc = await get_counting_channel(guild)

    if cc is None:
        return
    if channel.id == cc:
        with open("./databases/counting.json") as f:
            data = json.load(f)
        with open('./databases/db.json') as f:
            dataa = json.load(f)
        for i in dataa:
            if i['guild_id'] == guild.id:
                if i['lastcounter'] == None:
                    i['lastcounter'] = m.author.id
                    break
                elif i['lastcounter'] == m.author.id:
                    data[f"{guild.id}"] = 0
                    i['lastcounter'] = None
                    await m.add_reaction("❌")
                    em = discord.Embed(title=f"{m.author.name}, You ruined it!", description="Only one person at a time\nCount reset to zero")
                    with open("./databases/counting.json", 'w') as f:
                        json.dump(data, f, indent=4)
                    with open("./databases/db.json", 'w') as f:
                        json.dump(dataa, f, indent=4)
                    return await channel.send(embed=em)
                else:
                    i['lastcounter'] = m.author.id
                    break
                    
        if (data[f"{guild.id}"] + 1) == msg:
            data[f"{guild.id}"] += 1
            await m.add_reaction("✅")
            if msg == 69:
                await channel.send("Nice")
            if msg == 42:
                await channel.send("You have found the meaning of life.")
        else:
            await m.add_reaction("❌")
            em = discord.Embed(title=f"{m.author.name}, You ruined it!", description=f"You were supposed to type `{(data[f'{guild.id}']+1)}`\nCount reset to zero")
            i['lastcounter'] = None
            data[f"{guild.id}"] = 0
            await channel.send(embed=em)
        with open("./databases/counting.json", 'w') as f:
            json.dump(data, f, indent=4)
        with open("./databases/db.json", 'w') as f:
            json.dump(dataa, f, indent=4)


class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['num'])
    async def numrn(self, ctx):
        guild = ctx.guild
        with open('./databases/counting.json') as f:
            data = json.load(f)
        guildid = f'{guild.id}'
        numrn = data[guildid]
        await ctx.send(f"Current number is {numrn}")

    @commands.Cog.listener()
    async def on_message(self, message):

        channel = message.channel
        msg = message.content
        guild = message.guild

        await counting(msg, guild, channel, message)

    def mic(ctx):
        return ctx.author.id == 481377376475938826

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_num(self,ctx,nums):
        with open("./databases/counting.json") as f:
            data = json.load(f)
            nums = int(nums)
        data[f"{ctx.guild.id}"] = nums
        with open("./databases/counting.json", 'w') as f:
                        json.dump(data, f, indent=4)
        await ctx.send(f"Numb set to {nums}")



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
            with open("./databases/db.json") as f:
                data = json.load(f)
            data.append(insert)
            with open("./databases/db.json", 'w') as f:
                json.dump(data, f, indent=4)
            
            with open("./databases/counting.json") as f:
                data2 = json.load(f)
            data2[f"{i.id}"] = 0
            with open("./databases/counting.json", 'w') as f:
                json.dump(data2, f, indent=4)
            
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcountchannel(self, ctx, channel:discord.TextChannel):
        with open("./databases/db.json") as f:
            data = json.load(f)
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                i['counting_channel'] = channel.id
        with open('./databases/db.json', 'w') as f:
            json.dump(data, f, indent =4)
            await ctx.send("Done")

            
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def countingoff(self, ctx):
            with open("./databases/db.json") as f:
                data = json.load(f)
            for i in data:
                if i['guild_id'] == ctx.guild.id:
                    i['counting_channel'] = None
            with open('./databases/db.json', 'w') as f:
                json.dump(data, f, indent =4)
    
            
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        insert = {
            "guild_id": guild.id,
            "counting_channel": None,
            "lastcounter":None,
        }
        with open("./databases/db.json") as f:
            data = json.load(f)
        data.append(insert)
        with open("./databases/db.json", 'w') as f:
            json.dump(data, f, indent=4)

        with open("./databases/counting.json") as f:
            data2 = json.load(f)
        data2[f"{guild.id}"] = 0
        with open("./databases/counting.json", 'w') as f:
            json.dump(data2, f, indent=4)



def setup(client):
    client.add_cog(Counting(client))
