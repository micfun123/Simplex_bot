import discord
import random
from discord.ext import commands
import qrcode
import numexpr as ne
import numpy
import aiohttp
import asyncio
import datetime

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["flip", "coin"])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command(aliases=['qr'])
    async def qrcode(self, ctx, *, url):
        await ctx.message.delete()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(url))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",
                            back_color="white").convert('RGB')
        img.save('qrcode.png')
        await ctx.send(file=discord.File('qrcode.png'))


    @commands.command(aliases=["calculator"])
    async def calc(self, ctx, *, text: str):
        calc = ne.evaluate(text)
        msg = int(calc)
        await ctx.send(msg)

    @commands.command(Hidden=True)
    @commands.has_guild_permissions(administrator=True)
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)



    @commands.command(aliases=['rockpaperscissors'], help="Play Rock Paper Scissors")
    async def rps(self, ctx, rps: str):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        rps = rps.lower()
        if rps == 'rock':
            if cpu_choice == 'rock':
                em.description = "It's a tie!"
            elif cpu_choice == 'scissors':
                em.description = "You win!"
            elif cpu_choice == 'paper':
                em.description = "You lose!"

        elif rps == 'paper':
            if cpu_choice == 'paper':
                em.description = "It's a tie!"
            elif cpu_choice == 'rock':
                em.description = "You win!"
            elif cpu_choice == 'scissors':
                em.description = "You lose!"

        elif rps == 'scissors':
            if cpu_choice == 'scissors':
                em.description = "It's a tie!"
            elif cpu_choice == 'paper':
                em.description = "You win!"
            elif cpu_choice == 'rock':
                em.description = "You lose!"

        else:
            em.description = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.send(embed=em)


    @commands.command()
    async def roll(ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split("d"))
        except Exception:
            await ctx.send("Format has to be in NdN!")
            return

        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)


    @commands.command(aliases=['yahornah', 'yn'], extras={"category":"Fun"}, usage="yesorno [question]", help="This command makes a small poll which users can vote either yes, or no", description="Makes a Yah or Nah poll")
    async def yesorno(self, ctx, *, message):
        msg = await ctx.send(embed=discord.Embed(title="Yah or Nah?", description=message))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

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
            catjson = await request.json()
        # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/cat')
            factjson = await request2.json()

        embed = discord.Embed(title="Cat!", color=discord.Color.purple())
        embed.set_image(url=catjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)


    @commands.command(help = "It shows you a panda photo as well as a fact") #shows cat photo and fact
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/panda')
            Pandajson = await request.json()
        # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/panda')
            factjson = await request2.json()

        embed = discord.Embed(title="Panda!", color=discord.Color.purple())
        embed.set_image(url=Pandajson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)


    @commands.command(help = "It shows you a koala photo as well as a fact") #shows cat photo and fact
    async def koala(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/koala')
            koalajson = await request.json()
        # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/koala')
            factjson = await request2.json()

        embed = discord.Embed(title="koala!", color=discord.Color.purple())
        embed.set_image(url=koalajson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)


    @commands.command(help = "It shows you a fox photo as well as a fact") #shows cat photo and fact
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/fox')
            foxjson = await request.json()
        # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/fox')
            factjson = await request2.json()

        embed = discord.Embed(title="fox!", color=discord.Color.purple())
        embed.set_image(url=foxjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)

    @commands.command(help = "It shows you a bird photo as well as a fact") #shows cat photo and fact
    async def bird(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/birb')
            birdjson = await request.json()
        # This time we'll get the fact request as well!
            request2 = await session.get('https://some-random-api.ml/facts/bird')
            factjson = await request2.json()

        embed = discord.Embed(title="bird!", color=discord.Color.purple())
        embed.set_image(url=birdjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)


    @commands.command(aliases=["8ball", "eightball", "eight_ball"]) #8ball game
    async def _8ball(self, ctx, *, question):
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
    
    
    @commands.command(aliases=['pie'])
    async def catch(self,ctx):
        """Catch the pie, by reacting. Dont't drop it!"""
        em = discord.Embed(color=discord.Color.orange())
        em.add_field(name='🥧  __Catch The Pie Game__  🥧', value='To catch the pie you must simply react with the emoji, when it appears. Click as fast as you can and see how fast you caught it... \n**Good Luck!** \n\nHere we go in 3...', inline=False)
        pie1 = await ctx.send(embed=em)

        await asyncio.sleep(1)

        em = discord.Embed(color=discord.Color.orange())
        em.add_field(name='🥧  __Catch The Pie Game__  🥧', value='To catch the pie you must simply react with the emoji, when it appears. Click as fast as you can and see how fast you caught it... \n**Good Luck!** \n\nHere we go in 2..', inline=False)
        await pie1.edit(embed=em)

        await asyncio.sleep(1)

        em = discord.Embed(color=discord.Color.orange())
        em.add_field(name='🥧  __Catch The Pie Game__  🥧', value='To catch the pie you must simply react with the emoji, when it appears. Click as fast as you can and see how fast you caught it... \n**Good Luck!** \n\nHere we go in 1.', inline=False)
        await pie1.edit(embed=em)

        await asyncio.sleep(1)
        await pie1.add_reaction('🥧')

        def check(reaction, user):
            self.reacted = reaction.emoji
            return user == ctx.author and str(reaction.emoji)

        before_wait = datetime.datetime.now()
        reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        after_wait = datetime.datetime.now()
        time_delta = after_wait - before_wait
        time_taken = time_delta.total_seconds()

        em = discord.Embed(color=discord.Color.orange())
        em.add_field(name='🥧  __Catch The Pie Game__  🥧', value=f'To catch the pie you must simply react with the emoji, when it appears. Click as fast as you can and see how fast you caught it... \n**Good Luck!** \n\nYou caught it in **{round(time_taken, 3)} seconds**', inline=False)
        await pie1.edit(embed=em)

def setup(bot):
    bot.add_cog(Fun(bot))