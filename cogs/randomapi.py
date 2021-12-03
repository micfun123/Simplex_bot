import discord
from discord.ext import commands
import aiohttp

class Randomapi(commands.Cog):
    def __init__(self, client): 
        self.client = client 
        
    @commands.command(aliases=["doggo"], help = "It shows you a Dog photo as well as a fact") #shows a dog photo and a fact
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dogjson = await request.json()
            # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/dog')
            factjson = await request2.json()

        embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)

    @commands.command(help = "It shows you a cat photo as well as a fact") #shows cat photo and fact
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/cat')
            dogjson = await request.json()
            # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/cat')
            factjson = await request2.json()

        embed = discord.Embed(title="Cat!", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)


    @commands.command(aliases=["Joke", "jokes", "Jokes"], help = "It tells a joke")  #tells a joke
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            # This time we'll get the joke request as well!
            request = await session.get('https://some-random-api.ml/joke')
            jokejson = await request.json()

        
        embed = discord.Embed(title="I know its funny", color=discord.Color.purple())
        embed.set_footer(text=jokejson['joke'])
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Randomapi(client))