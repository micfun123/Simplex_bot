from typing import Text
import discord
import random
import aiohttp

from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("we have powered on, I an alive.")

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms ping time')
    

@client.command(aliases=["Hello", "hi", "Hi"])
async def hello(ctx):
    await ctx.send('Hi')


@client.command(aliases=["8ball", "eightball", "eight_ball", "Eight_ball"])
async def _8ball(ctx, *, question):
    responses = ['magic eight ball maintains Signs point to yes.',
                 'magicball affirms My reply is no.',
                 'magic ball answers Signs point to yes.',
                 'magicball affirms Yes definitely.',
                 'magicball affirms Yes.',
                 '8 ball magic said Most likely.',
                 'magic ball answers Very doubtful.',
                 'magic 8 ball answers Without a doubt.',
                 'mystic eight ball said Most likely.',
                 "magic ball answers Don't count on it.",
                 'Magic ball says 100% No',
                 'Magic ball does not know have you tryed google?',
                 "Its not looking so good"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command(aliases=["purge"])
@commands.has_permissions(administrator=True) # Making sure the person executing the command has the permissions
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)

@commands.has_permissions(kick_members=True)
@client.command(help = "kicks a person from server")
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)

@client.command(aliases=["doggo"], help = "It shows you a Dog photo as well as a fact")
async def dog(ctx):
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

@client.command(help = "It shows you a cat photo as well as a fact")
async def cat(ctx):
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


@client.command(aliases=["Joke", "jokes", "Jokes"], help = "It tells a joke")
async def joke(ctx):
   async with aiohttp.ClientSession() as session:
      # This time we'll get the joke request as well!
      request = await session.get('https://some-random-api.ml/joke')
      jokejson = await request.json()

   
   embed = discord.Embed(title="I know its funny", color=discord.Color.purple())
   embed.set_footer(text=jokejson['joke'])
   await ctx.send(embed=embed) 




client.run('')