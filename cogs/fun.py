from unicodedata import name
import discord
import random
from discord.ext import commands
import re
import aiohttp
import asyncio
import datetime
import requests
import aiosqlite
from random import randrange
from pyfiglet import figlet_format, FontError, FontNotFound
from tools import get, log
from io import BytesIO
from discord.ui import View
import os
import aiofiles
import io
import urllib
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageSequence


def slap(imageUrl, seconduser):
    hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
    req = urllib.request.Request(imageUrl, headers=hdr)
    response = urllib.request.urlopen(req)
    f = io.BytesIO(response.read())
    req = urllib.request.Request(seconduser, headers=hdr)
    response = urllib.request.urlopen(req)
    d = io.BytesIO(response.read())
    random_number = random.randint(1, 3)
    if random_number == 1:
        im1 = Image.open("images/slap1.gif")
        im2 = Image.open(f)
        im2 = im2.resize((100, 100))
        im2 = im2.convert("RGBA")

        frames = []
        for frame in ImageSequence.Iterator(im1):
            frame = frame.copy()
            frame = frame.convert("RGBA")
            frame.paste(im2, (500, 90))
            frames.append(frame)

        bytes_img = io.BytesIO()
        frames[0].save(
            bytes_img,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=100,
            disposal=2,
        )
        bytes_img.seek(0)
        return bytes_img
    elif random_number == 2:
        im1 = Image.open("images/slap-in-the-face-angry.gif")
        im3 = Image.open(d)
        im2 = Image.open(f)
        im2 = im2.resize((100, 100))
        im2 = im2.convert("RGBA")
        im3 = im3.resize((100, 100))
        im3 = im3.convert("RGBA")

        frames = []
        for frame in ImageSequence.Iterator(im1):
            frame = frame.copy()
            frame = frame.convert("RGBA")
            frame.paste(im2, (50, 168))
            frame.paste(im3, (220, 55))
            frames.append(frame)
        bytes_img = io.BytesIO()
        frames[0].save(
            bytes_img,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=100,
            disposal=2,
        )
        bytes_img.seek(0)
        return bytes_img

    elif random_number == 3:
        im1 = Image.open("images/slap.gif")
        im3 = Image.open(d)
        im2 = Image.open(f)
        im2 = im2.resize((100, 100))
        im2 = im2.convert("RGBA")
        im3 = im3.resize((100, 100))
        im3 = im3.convert("RGBA")

        frames = []
        for frame in ImageSequence.Iterator(im1):
            frame = frame.copy()
            frame = frame.convert("RGBA")
            frame.paste(im2, (120, 45))
            frame.paste(im3, (450, 55))
            frames.append(frame)
        bytes_img = io.BytesIO()
        frames[0].save(
            bytes_img,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=100,
            disposal=2,
        )
        bytes_img.seek(0)
        return bytes_img


def snuggle(imageUrl, seconduser):
    hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
    req = urllib.request.Request(imageUrl, headers=hdr)
    response = urllib.request.urlopen(req)
    f = io.BytesIO(response.read())
    req = urllib.request.Request(seconduser, headers=hdr)
    response = urllib.request.urlopen(req)
    d = io.BytesIO(response.read())
    random_number = random.randint(1, 2)
    if random_number == 1:
        im1 = Image.open("images/love-hug.gif")
        im2 = Image.open(f)
        im2 = im2.resize((65, 65))
        im2 = im2.convert("RGBA")
        im3 = Image.open(d)
        im3 = im3.resize((65, 65))
        im3 = im3.convert("RGBA")

        frames = []
        for frame in ImageSequence.Iterator(im1):
            frame = frame.copy()
            frame = frame.convert("RGBA")
            frame.paste(im2, (40, 70))
            frames.append(frame)
            frame.paste(im3, (120, 20))
            frames.append(frame)

        bytes_img = io.BytesIO()
        frames[0].save(
            bytes_img,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=100,
            disposal=2,
        )
        bytes_img.seek(0)
        return bytes_img
    if random_number == 2:
        im1 = Image.open("images/strangehug.gif")
        im2 = Image.open(f)
        im2 = im2.resize((60, 60))
        im2 = im2.convert("RGBA")
        im3 = Image.open(d)
        im3 = im3.resize((60, 60))
        im3 = im3.convert("RGBA")

        frames = []
        for frame in ImageSequence.Iterator(im1):
            frame = frame.copy()
            frame = frame.convert("RGBA")
            frame.paste(im2, (80, 40))
            frames.append(frame)
            frame.paste(im3, (170, 20))
            frames.append(frame)

        bytes_img = io.BytesIO()
        frames[0].save(
            bytes_img,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=100,
            disposal=2,
        )
        bytes_img.seek(0)
        return bytes_img


def stab(imageUrl, seconduser):
    hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
    req = urllib.request.Request(imageUrl, headers=hdr)
    response = urllib.request.urlopen(req)
    f = io.BytesIO(response.read())
    req = urllib.request.Request(seconduser, headers=hdr)
    response = urllib.request.urlopen(req)
    d = io.BytesIO(response.read())
    im1 = Image.open("images/stab-fake.gif")
    im2 = Image.open(f)
    im2 = im2.resize((100, 100))
    im2 = im2.convert("RGBA")
    im3 = Image.open(d)
    im3 = im3.resize((100, 100))
    im3 = im3.convert("RGBA")

    frames = []
    for frame in ImageSequence.Iterator(im1):
        frame = frame.copy()
        frame = frame.convert("RGBA")
        frame.paste(im2, (120, 45))
        frame.paste(im3, (275, 40))
        frames.append(frame)

    bytes_img = io.BytesIO()
    frames[0].save(
        bytes_img,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=100,
        disposal=2,
    )
    bytes_img.seek(0)
    return bytes_img


class MyView(View):
    def __init__(self):
        super().__init__(timeout=500)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Claim", custom_id="b1")
    async def button1(self, button, interaction):
        button.style = discord.ButtonStyle.red
        button.label = "Claimed"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("https://imgur.com/NQinKJB", ephemeral=True)


class Fun(commands.Cog):
    """Games fun and silly commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", help="Flip a coin")
    async def coinflipcommands(self, ctx):
        """Coinflip!"""
        coinsides = ["Heads", "Tails"]
        await ctx.send(
            f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!"
        )

    @commands.slash_command(name="coinflip", help="Flip a coin")
    async def coinflip(self, ctx):
        """Coinflip!"""
        coinsides = ["Heads", "Tails"]
        await ctx.respond(
            f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!"
        )

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """!poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command(pass_context=True)
    async def dice(self, ctx, *, msg="1"):
        """Roll dice. Optionally input # of dice and # of sides. Ex: [p]dice 5 12"""
        await ctx.message.delete()
        invalid = "Invalid syntax. Ex: `>dice 4` - roll four normal dice. `>dice 4 12` - roll four 12 sided dice."
        dice_rolls = []
        dice_roll_ints = []
        try:
            dice, sides = re.split("[d\s]", msg)
        except ValueError:
            dice = msg
            sides = "6"
        try:
            for roll in range(int(dice)):
                result = random.randint(1, int(sides))
                dice_rolls.append(str(result))
                dice_roll_ints.append(result)
        except ValueError:
            return await ctx.send(self.bot.bot_prefix + invalid)
        embed = discord.Embed(title="Dice rolls:", description=" ".join(dice_rolls))
        embed.add_field(name="Total:", value=sum(dice_roll_ints))
        await ctx.send("", embed=embed)

    # @commands.command(aliases=["calculator"])
    # async def calc(self, ctx, *, text: str):
    #    calc = ne.evaluate(text)
    #    msg = int(calc)
    #    await ctx.send(msg)

    @commands.command(Hidden=True)
    @commands.has_guild_permissions(administrator=True)
    async def say(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command(name="pressf", help="Press F to pay respects {reson}")
    async def pressf_(self, ctx, *, object):
        """Pay respect to something/someone by pressing the reaction."""
        try:
            message = await ctx.send(f"Press F to pay respect to `{object}`")
            await message.add_reaction("<:f_key:999594098010882148>")
            while True:

                def check(r, u):
                    return (
                        str(r.emoji) == "<:f_key:999594098010882148>"
                        and r.message == message
                        and u.id != self.bot.user.id
                    )

                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=60.0
                )
                if reaction:
                    await ctx.send(f"**{user.name}** has paid their respects.")
        except asyncio.TimeoutError:
            await ctx.send("Timed out.")

    @commands.command(name="pressx", help="Press X to doubt {reson}")
    async def pressx_(self, ctx, *, object):
        """Pay respect to something/someone by pressing the reaction."""
        try:
            message = await ctx.send(f"Press X to doubts `{object}`")
            await message.add_reaction("<:X_button:978154155044646952>")
            while True:

                def check(r, u):
                    return (
                        str(r.emoji) == "<:X_button:978154155044646952>"
                        and r.message == message
                        and u.id != self.bot.user.id
                    )

                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=60.0
                )
                if reaction:
                    await ctx.send(f"**{user.name}** has doubts.")
        except asyncio.TimeoutError:
            await ctx.send("Timed out.")

    @commands.command(aliases=["jokes"], help="It tells a joke")  # tells a joke
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            # This time we'll get the joke request as well!
            jokejson = requests.get("https://some-random-api.com/joke").json()

        embed = discord.Embed(title="I know its funny", color=discord.Color.purple())
        embed.set_footer(text=jokejson["joke"])
        await ctx.send(embed=embed)

    @commands.command(aliases=["rockpaperscissors"], help="Play Rock Paper Scissors")
    async def rps(self, ctx, rps: str):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        rps = rps.lower()
        if rps == "rock":
            if cpu_choice == "rock":
                em.description = "It's a tie!"
            elif cpu_choice == "scissors":
                em.description = "You win!"
            elif cpu_choice == "paper":
                em.description = "You lose!"

        elif rps == "paper":
            if cpu_choice == "paper":
                em.description = "It's a tie!"
            elif cpu_choice == "rock":
                em.description = "You win!"
            elif cpu_choice == "scissors":
                em.description = "You lose!"

        elif rps == "scissors":
            if cpu_choice == "scissors":
                em.description = "It's a tie!"
            elif cpu_choice == "paper":
                em.description = "You win!"
            elif cpu_choice == "rock":
                em.description = "You lose!"

        else:
            em.description = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.send(embed=em)

    @commands.command(
        aliases=["yahornah", "yn"],
        extras={"category": "Fun"},
        usage="yesorno [question]",
        help="This command makes a small poll which users can vote either yes, or no",
        description="Makes a Yah or Nah poll",
    )
    async def yesorno(self, ctx, *, message):
        msg = await ctx.send(
            embed=discord.Embed(title="Yah or Nah?", description=message)
        )
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.command(
        name="dog", aliases=["doggo"], help="It shows you a Dog photo as well as a fact"
    )  # shows a dog photo and a fact
    async def dog_command(self, ctx):
        request = requests.get("https://some-random-api.com/img/dog")
        dogimg = request.json()
        # This time we'll get the fact request as well!
        request2 = requests.get("https://some-random-api.com/facts/dog")
        factjson = request2.json()

        embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
        embed.set_image(url=dogimg["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.send(embed=embed)

    @commands.slash_command(
        name="dog", help="It shows you a Dog photo as well as a fact"
    )  # shows a dog photo and a fact
    async def dog_command(self, ctx):
        request = requests.get("https://some-random-api.com/img/dog")
        dogimg = request.json()
        # This time we'll get the fact request as well!
        request2 = requests.get("https://some-random-api.com/facts/dog")
        factjson = request2.json()

        embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
        embed.set_image(url=dogimg["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.respond(embed=embed)

    @commands.command(
        name="cat", aliases=["pussy"], help="It shows you a cat photo as well as a fact"
    )  # shows cat photo and fact
    async def cat__prefix(self, ctx):
        request = requests.get("    ")
        catjson = request.json()
        # This time we'll get the fact request as well!
        request2 = requests.get("https://some-random-api.com/facts/cat")
        factjson = request2.json()

        embed = discord.Embed(title="Cat!", color=discord.Color.purple())
        embed.set_image(url=catjson["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.send(embed=embed)

    @commands.slash_command(
        name="cat", help="It shows you a cat photo as well as a fact"
    )  # shows cat photo and fact
    async def cat__slash(self, ctx):
        request = requests.get("https://some-random-api.com/img/cat")
        catjson = request.json()
        # This time we'll get the fact request as well!
        request2 = requests.get("https://some-random-api.com/facts/cat")
        factjson = request2.json()

        embed = discord.Embed(title="Cat!", color=discord.Color.purple())
        embed.set_image(url=catjson["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.respond(embed=embed)

    @commands.command(
        help="It shows you a panda photo as well as a fact"
    )  # shows cat photo and fact
    async def panda(self, ctx):
        request = requests.get("https://some-random-api.com/img/panda")
        pandajson = request.json()
        # This time we'll get the fact request as well!
        request2 = requests.get("https://some-random-api.com/facts/panda")
        factjson = request2.json()
        embed = discord.Embed(title="Panda!", color=discord.Color.purple())
        embed.set_image(url=pandajson["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.send(embed=embed)

    @commands.command(
        help="It shows you a koala photo as well as a fact"
    )  # shows cat photo and fact
    async def koala(self, ctx):
        request = requests.get("https://some-random-api.com/img/koala")
        koalajson = request.json()
        # This time we'll get the fact request as well!
        request2 = requests.get("https://some-random-api.com/facts/koala")
        factjson = request2.json()

        embed = discord.Embed(title="koala!", color=discord.Color.purple())
        embed.set_image(url=koalajson["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.send(embed=embed)

    @commands.command(
        help="It shows you a fox photo as well as a fact"
    )  # shows cat photo and fact
    async def fox(self, ctx):
        request = requests.get("https://some-random-api.com/img/fox")
        foxjson = request.json()
        # This time we'll get the fact request as well!
        request2 = requests.get("https://some-random-api.com/facts/fox")
        factjson = request2.json()

        embed = discord.Embed(title="fox!", color=discord.Color.purple())
        embed.set_image(url=foxjson["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.send(embed=embed)

    @commands.command(
        help="It shows you a bird photo as well as a fact"
    )  # shows cat photo and fact
    async def bird(self, ctx):
        urlimg = "https://some-random-api.com/img/birb"
        urlfact = "https://some-random-api.com/facts/bird"
        request = requests.get(urlimg)
        birdjson = request.json()
        # This time we'll get the fact request as well!
        request2 = requests.get(urlfact)
        factjson = request2.json()
        embed = discord.Embed(title="Bird!", color=discord.Color.purple())
        embed.set_image(url=birdjson["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.send(embed=embed)

    @commands.command(
        help="It shows you a Red Panda photo "
    )  # shows cat photo and fact
    async def red_panda(self, ctx):
        url = "https://some-random-api.com/img/red_panda"
        request = requests.get(url)
        redpandajson = request.json()
        embed = discord.Embed(title="Red Panda!", color=discord.Color.purple())
        embed.set_image(url=redpandajson["link"])
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["8ball", "eightball", "eight_ball"], help="8ball proves a answer"
    )  # 8ball game
    async def _8ball(self, ctx, *, question):
        responses = [
            "magic eight ball maintains Signs point to yes.",
            "magicball affirms My reply is no.",
            "magic ball answers Signs point to yes.",
            "magicball affirms Yes definitely.",
            "magicball affirms Yes.",
            "8 ball magic said Most likely.",
            "magic ball answers Very doubtful.",
            "magic 8 ball answers Without a doubt.",
            "mystic eight ball said Most likely.",
            "magic ball answers Don't count on it.",
            "Magic ball says 100% No",
            "Magic ball does not know have you tryed google?",
            "Its not looking so good",
        ]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @commands.command(aliases=["pie"])
    async def catch_pie(self, ctx):
        """Catch the pie, by reacting. Dont't drop it!"""
        em = discord.Embed(color=discord.Color.orange())
        em.add_field(
            name="🥧  __Catch The Pie Game__  🥧",
            value="To catch the pie you must simply react with the emoji, when it appears. Click as fast as you can and see how fast you caught it... \n**Good Luck!** \n\nHere we go in ?time...",
            inline=False,
        )
        pie1 = await ctx.send(embed=em)

        await asyncio.sleep(randrange(5))
        await pie1.add_reaction("🥧")

        def check(reaction, user):
            self.reacted = reaction.emoji
            return user == ctx.author and str(reaction.emoji)

        before_wait = datetime.datetime.now()
        reaction, user = await self.bot.wait_for(
            "reaction_add", timeout=30.0, check=check
        )
        after_wait = datetime.datetime.now()
        time_delta = after_wait - before_wait
        time_taken = time_delta.total_seconds()

        em = discord.Embed(color=discord.Color.orange())
        em.add_field(
            name="🥧  __Catch The Pie Game__  🥧",
            value=f"To catch the pie you must simply react with the emoji, when it appears. Click as fast as you can and see how fast you caught it... \n**Good Luck!** \n\nYou caught it in **{round(time_taken, 5)} seconds**",
            inline=False,
        )
        await pie1.edit(embed=em)
        async with aiosqlite.connect("./databases/pie.db") as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS pie (user_id INTEGER, time_taken REAL)"
            )
            await db.execute(
                "INSERT INTO pie (user_id, time_taken) VALUES (?, ?)",
                (ctx.author.id, time_taken),
            )
            await db.commit()
            await db.close()

    @commands.slash_command(
        name="catch_pie", description="Catch the pie, by reacting. Dont't drop it!"
    )
    async def catch_the_pie(self, ctx):
        """Catch the pie, by reacting. Dont't drop it!"""
        await ctx.respond("getting pie...")
        em = discord.Embed(color=discord.Color.orange())
        em.add_field(
            name="🥧  __Catch The Pie Game__  🥧",
            value="To catch the pie you must simply react with the emoji, when it appears. Click as fast as you can and see how fast you caught it... \n**Good Luck!** \n\nHere we go in ?time...",
            inline=False,
        )
        pie1 = await ctx.send(embed=em)

        await asyncio.sleep(randrange(5))
        await pie1.add_reaction("🥧")

        def check(reaction, user):
            self.reacted = reaction.emoji
            return user == ctx.author and str(reaction.emoji)

        before_wait = datetime.datetime.now()
        reaction, user = await self.bot.wait_for(
            "reaction_add", timeout=30.0, check=check
        )
        after_wait = datetime.datetime.now()
        time_delta = after_wait - before_wait
        time_taken = time_delta.total_seconds()

        em = discord.Embed(color=discord.Color.orange())
        em.add_field(
            name="🥧  __Catch The Pie Game__  🥧",
            value=f"To catch the pie you must simply react with the emoji, when it appears. Click as fast as you can and see how fast you caught it... \n**Good Luck!** \n\nYou caught it in **{round(time_taken, 5)} seconds**",
            inline=False,
        )
        await pie1.edit(embed=em)
        async with aiosqlite.connect("./databases/pie.db") as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS pie (user_id INTEGER, time_taken REAL)"
            )
            await db.execute(
                "INSERT INTO pie (user_id, time_taken) VALUES (?, ?)",
                (ctx.author.id, time_taken),
            )
            await db.commit()
            await db.close()

    @commands.slash_command(
        name="pieleaderboard", description="View the pie leaderboard"
    )
    async def pie_leaderboard(self, ctx):
        """View the pie leaderboard."""
        async with aiosqlite.connect("./databases/pie.db") as db:
            # get the 10 fastest times
            data = await db.execute(
                "SELECT user_id, time_taken FROM pie ORDER BY time_taken ASC"
            )
            rows = await data.fetchall()
        em = discord.Embed(color=discord.Color.orange())
        em.add_field(
            name="🥧  __Catch The Pie Leaderboard__  🥧",
            value="Here are the top 10 people who caught the pie the fastest...",
            inline=False,
        )
        for i, row in enumerate(rows[:10]):
            user = await self.bot.fetch_user(row[0])
            em.add_field(
                name=f"{i+1}. {user}",
                value=f"**{round(row[1], 5)} seconds**",
                inline=False,
            )
        await ctx.send(embed=em)

    @commands.command(name="pielb")
    async def pie_leaderboard__command(self, ctx):
        """View the pie leaderboard."""
        async with aiosqlite.connect("./databases/pie.db") as db:
            # get the 10 fastest times
            data = await db.execute(
                "SELECT user_id, time_taken FROM pie ORDER BY time_taken ASC"
            )
            rows = await data.fetchall()
        em = discord.Embed(color=discord.Color.orange())
        for i in range(10):
            user = await self.bot.fetch_user(rows[i][0])
            em.add_field(
                name=f"{i+1}. {user}",
                value=f"**{round(rows[i][1], 5)} seconds**",
                inline=False,
            )
        await ctx.send(embed=em)

    @commands.command(name="hack")
    async def hecker(self, ctx, member: discord.Member):
        """Hack someone and get their details."""
        used_words = [
            "Nerd",
            "Sucker",
            "Noob",
            "Sup",
            "Yo",
            "Wassup",
            "Nab",
            "Nub",
            "fool",
            "stupid",
            "b1tch",
            "fvck",
            "idiot",
        ]
        mails = ["@gmail.com", "@hotmail.com", "@yahoo.com"]

        hacking = await ctx.send(f"Hacking {member.name}....")
        await asyncio.sleep(1.55)
        await hacking.edit(content="Finding info....")
        await asyncio.sleep(1.55)
        await hacking.edit(
            content=f"Discord email address: {member.name}{random.choice(mails)}"
        )
        await asyncio.sleep(2)
        await hacking.edit(content=f"Password: x2yz{member.name}xxy65")
        await asyncio.sleep(2)
        await hacking.edit(content=f"Injecting trojan horse")
        await asyncio.sleep(2)
        await hacking.edit(content=f"Most used words: {random.choice(used_words)}")
        await asyncio.sleep(1.55)
        await hacking.edit(content="IP address: 127.0.0.1:50")
        await asyncio.sleep(1.55)
        await hacking.edit(content="Selling information to the government....")
        await asyncio.sleep(2)
        await hacking.edit(
            content=f"Reporting {member.name} to Discord for violating ToS"
        )
        await asyncio.sleep(2)
        await hacking.edit(content="Hacking medical records.....")
        await asyncio.sleep(1.55)
        await hacking.edit(
            content=f"{ctx.author.mention} successfully hacked {member.mention}"
        )
        await ctx.send("The ultimate, totally real hacking has been completed!")

    @commands.slash_command(name="hack")
    async def hecker_slash(self, ctx, member: discord.Member):
        """Hack someone and get their details."""
        used_words = [
            "Nerd",
            "Sucker",
            "Noob",
            "Sup",
            "Yo",
            "Wassup",
            "Nab",
            "Nub",
            "fool",
            "stupid",
            "b1tch",
            "fvck",
            "idiot",
            "Bruh",
            "LAMO",
        ]
        mails = ["@gmail.com", "@hotmail.com", "@yahoo.com", "@outlook.com"]
        await ctx.respond(f"Powering Up all systems....")
        await asyncio.sleep(1.55)
        hacking = await ctx.send(f"Hacking {member.name}....")
        await asyncio.sleep(1.55)
        await hacking.edit(content="Finding info....")
        await asyncio.sleep(1.55)
        await hacking.edit(
            content=f"Discord email address: {member.name}{random.choice(mails)}"
        )
        await asyncio.sleep(2)
        await hacking.edit(content=f"Password: x2yz{member.name}xxy65")
        await asyncio.sleep(2)
        await hacking.edit(content=f"Injecting trojan horse")
        await asyncio.sleep(2)
        await hacking.edit(content=f"Most used words: {random.choice(used_words)}")
        await asyncio.sleep(1.55)
        await hacking.edit(content="IP address: 127.0.0.1:50")
        await asyncio.sleep(1.55)
        await hacking.edit(content="Selling information to the government....")
        await asyncio.sleep(2)
        await hacking.edit(
            content=f"Reporting {member.name} to Discord for violating ToS"
        )
        await asyncio.sleep(2)
        await hacking.edit(content="Hacking medical records.....")
        await asyncio.sleep(1.55)
        await hacking.edit(
            content=f"{ctx.author.mention} successfully hacked {member.mention}"
        )
        await ctx.send("The ultimate, totally real hacking has been completed!")

    @commands.command(aliases=["ss"], name="screenshot")
    async def screenshot__command(self, ctx, *, url):
        """Takes a screenshot from a given URL."""
        url = url.replace("https://", "")
        await ctx.send(f"https://image.thum.io/get/https://{url}")

    @commands.slash_command(name="screenshoter")
    async def screenshot____slash(self, ctx, *, url):
        """Takes a screenshot from a given URL."""
        url = url.replace("https://", "")
        await ctx.respond(f"https://image.thum.io/get/https://{url}")

    @commands.command(
        name="runcode",
        usage="runcode [language] [code]",
        description="Runs code",
        help="This command is used to run code. It supports many languages.",
    )
    async def runcode_(self, ctx, lang: str, *, code):
        code = code.replace("`", "")
        data = {"language": lang, "source": f"""{code}"""}
        url = "https://emkc.org/api/v1/piston/execute"

        data = await get.post_get_json(url, data)
        print(data)
        if data["ran"] == True:
            Embed = discord.Embed(
                title="Code Output",
                description=f"```\n{data['output']}```",
                color=discord.Color.green(),
            )
            await ctx.send(embed=Embed)
        if data["stderr"] != "":
            Embed = discord.Embed(
                title="Errors",
                description=f"```\n{data['stderr']}```",
                color=discord.Color.red(),
            )
            await ctx.send(embed=Embed)

    @commands.command(aliases=["boredom"], name="bored")
    async def bored__c(self, ctx):
        try:
            BASE_URL = "http://www.boredapi.com/api/activity?"
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                data = response.json()
                activity = data["activity"]
                accessibility = data["accessibility"]
                type = data["type"]
                participants = data["participants"]
                price = data["price"]

                e = discord.Embed(
                    title=f"If your bored, you should try {activity}",
                    color=discord.Colour.blue(),
                )
                e.add_field(name="Accessibility", value=accessibility)
                e.add_field(name="Type", value=type)
                e.add_field(name="Participants", value=participants)
                e.add_field(name="Price", value=price)
                await ctx.send(embed=e)

            else:
                # showing the error message
                await ctx.send("I've had a connection issue .")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            await ctx.send("I've had a connection issue .")

    @commands.slash_command(name="bored")
    async def bored__slash(self, ctx):
        try:
            BASE_URL = "http://www.boredapi.com/api/activity?"
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                data = response.json()
                activity = data["activity"]
                accessibility = data["accessibility"]
                type = data["type"]
                participants = data["participants"]
                price = data["price"]

                e = discord.Embed(
                    title=f"If your bored, you should try {activity}",
                    color=discord.Colour.blue(),
                )
                e.add_field(name="Accessibility", value=accessibility)
                e.add_field(name="Type", value=type)
                e.add_field(name="Participants", value=participants)
                e.add_field(name="Price", value=price)
                await ctx.respond(embed=e)

            else:
                # showing the error message
                await ctx.respond("I've had a connection issue .")
        except Exception as e:
            await ctx.respond(f"Error: {e}")
            await ctx.respond("I've had a connection issue .")

    @commands.group(pass_context=True, invoke_without_command=True)
    async def ascii(self, ctx, *, msg):
        """Convert text to ascii art."""
        if ctx.invoked_subcommand is None:
            if msg:
                font = "big"
                msg = str(figlet_format(msg.strip(), font=font))
                if len(msg) > 2000:
                    await ctx.send("Message too long, RIP.")
                else:
                    await ctx.message.delete()
                    await ctx.send("```\n{}\n```".format(msg))
            else:
                await ctx.send(
                    "Please input text to convert to ascii art. Ex: ``>ascii stuff``"
                )

    @commands.group(pass_context=True, invoke_without_command=True)
    async def slantascii(self, ctx, *, msg):
        """Convert text to ascii art."""
        if ctx.invoked_subcommand is None:
            if msg:
                font = "slant"
                msg = str(figlet_format(msg.strip(), font=font))
                if len(msg) > 2000:
                    await ctx.send("Message too long, RIP.")
                else:
                    await ctx.message.delete()
                    await ctx.send("```\n{}\n```".format(msg))
            else:
                await ctx.send(
                    "Please input text to convert to ascii art. Ex: ``>ascii stuff``"
                )

    #@commands.command(help="It shows Tea photo")
    #async def tea(self, ctx):
    #    async with aiohttp.ClientSession() as session:
    #        request = await session.get("https://hotbeverage.herokuapp.com/json/tea")
    #        teajason = await request.json()

    #    embed = discord.Embed(title="TEA!", color=discord.Color.purple())
    #    embed.set_image(url=teajason["img_url"])
    #    await ctx.send(embed=embed)

    #@commands.command(help="It shows coffee photo")
    #async def coffee(self, ctx):
    #    async with aiohttp.ClientSession() as session:
    #        request = await session.get("https://hotbeverage.herokuapp.com/json/coffee")
    #        teajason = await request.json()

    #    embed = discord.Embed(title="coffee!", color=discord.Color.purple())
    #    embed.set_image(url=teajason["img_url"])
    #    await ctx.send(embed=embed)


    @commands.command(name="freestuff", help="Shows free stuff")
    async def freestuf_commands(self, ctx):
        await ctx.send("Claim a Free gift", view=MyView())

    @commands.slash_command(name="freestuff", description="Shows free stuff")
    async def freestuff_slassh(self, ctx):
        await ctx.respond("Claim a Free gift", view=MyView())

    @commands.command(
        help="This will put a pixelate effect over the profile",
        extras={"category": "Search"},
        usage="[@member]",
        description="Image overlays for you discord profile pic",
    )
    async def pixelatethis(self, ctx, urls):
        hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
        URL = "https://some-random-api.com/canvas/pixelate?avatar={}".format(urls)
        req = urllib.request.Request(URL, headers=hdr)
        response = urllib.request.urlopen(req)
        f = io.BytesIO(response.read())
        await ctx.send(file=discord.File(f, "pixelate.png"))

    #API is deprecated. Hopes to get it back soon

    #    @commands.command(name="i_wish")
    #    async def i_wish_(self, ctx, *, message):
    #        hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
    #        text = message.replace(" ", "%20")
    #        URL = "http://api.michaelparker.ml/filters/I_wish?text={}".format(text)
    #        req = urllib.request.Request(URL, headers=hdr)
    #        response = urllib.request.urlopen(req)
    #        f = io.BytesIO(response.read())
    #        await ctx.send(file=discord.File(f, "wish.png"))
#
    #    @commands.slash_command(name="i_wish")
    #    async def i_wish(self, ctx, *, message):
    #        hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
    #        text = message.replace(" ", "%20")
    #        URL = "http://api.michaelparker.ml/filters/I_wish?text={}".format(text)
    #        req = urllib.request.Request(URL, headers=hdr)
    #        response = urllib.request.urlopen(req)
    #        f = io.BytesIO(response.read())
    #        await ctx.respond(file=discord.File(f, "wish.png"))
#
    #    @commands.command(name="if_they_could_read")
    #    async def if_they_could_read_(self, ctx, *, message):
    #        hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
    #        text = message.replace(" ", "%20")
    #        URL = "http://api.michaelparker.ml/Memes/if_the_could_read?text={}".format(text)
    #        req = urllib.request.Request(URL, headers=hdr)
    #        response = urllib.request.urlopen(req)
    #        f = io.BytesIO(response.read())
    #        await ctx.send(file=discord.File(f, "read.png"))
#
    #    @commands.slash_command(name="if_they_could_read")
    #    async def if_they_could_read__s(self, ctx, *, message):
    #        text = message.replace(" ", "%20")
    #        text = text.replace("’", "%E2%80%99")
    #        URL = "http://api.michaelparker.ml/Memes/if_the_could_read?text={}".format(text)
    #        req = urllib.request.Request(URL)
    #        response = urllib.request.urlopen(req)
    #        f = io.BytesIO(response.read())
    #        await ctx.respond(file=discord.File(f, "read.png"))
#
    #    @commands.command(name="um_dad")
    #    async def um_dad__(self, ctx, *, message):
    #        hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
    #        text = message.replace(" ", "%20")
    #        URL = "http://api.michaelparker.ml/Memes/um_dad?text={}".format(text)
    #        req = urllib.request.Request(URL, headers=hdr)
    #        response = urllib.request.urlopen(req)
    #        f = io.BytesIO(response.read())
    #        await ctx.send(file=discord.File(f, "read.png"))
#
    #    @commands.slash_command(name="um_dad")
    #    async def um_dad___S(self, ctx, *, message):
    #        text = message.replace(" ", "%20")
    #        text = text.replace("’", "%E2%80%99")
    #        URL = "http://api.michaelparker.ml/Memes/um_dad?text={}".format(text)
    #        req = urllib.request.Request(URL)
    #        response = urllib.request.urlopen(req)
    #        f = io.BytesIO(response.read())
    #        await ctx.respond(file=discord.File(f, "read.png"))
#
    #    @commands.command(name="headache")
    #    async def headache__(self, ctx, *, message):
    #        text = message.replace(" ", "%20")
    #        text = text.replace("’", "%E2%80%99")
    #        URL = "https://michaelapi.herokuapp.com/Memes/headache?text={}".format(text)
    #        req = urllib.request.Request(URL)
    #        response = urllib.request.urlopen(req)
    #        f = io.BytesIO(response.read())
    #        await ctx.send(file=discord.File(f, "read.png"))
#
    #    @commands.slash_command(name="headache")
    #    async def headache___S(self, ctx, *, message):
    #        text = message.replace(" ", "%20")
    #        text = text.replace("’", "%E2%80%99")
    #        URL = "https://michaelapi.herokuapp.com/Memes/headache?text={}".format(text)
    #        req = urllib.request.Request(URL)
    #        response = urllib.request.urlopen(req)
    #        f = io.BytesIO(response.read())
    #        await ctx.respond(file=discord.File(f, "read.png"))

    @commands.command(hidden=True)
    async def im_blue(self, ctx):
        await ctx.send(
            """
                        I'm blue
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di
                I'm blue
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di
                Da ba dee da ba di"""
        )

    @commands.command(name="slap")
    async def slap__command(self, ctx, member: discord.Member):
        await ctx.send(f"{ctx.author.mention} slapped {member.mention}")
        img = slap(member.avatar.url, ctx.author.avatar.url)
        await ctx.send(file=discord.File(img, "slap.gif"))

    @commands.slash_command(name="slap")
    async def slap__slash(self, ctx, member: discord.Member):
        await ctx.respond(f"{ctx.author.mention} slapped {member.mention}")
        img = slap(member.avatar.url, ctx.author.avatar.url)
        await ctx.respond(file=discord.File(img, "slap.gif"))

    @commands.command(name="kill")
    async def kill__command(self, ctx, member: discord.Member):
        await ctx.send(f"{ctx.author.mention} killed {member.mention}")
        img = stab(member.avatar.url, ctx.author.avatar.url)
        await ctx.send(file=discord.File(img, "kill.gif"))

    @commands.slash_command(name="kill")
    async def kill__slash(self, ctx, member: discord.Member):
        await ctx.respond(f"{ctx.author.mention} killed {member.mention}")
        img = stab(member.avatar.url, ctx.author.avatar.url)
        await ctx.respond(file=discord.File(img, "kill.gif"))

    @commands.command(name="hug")
    async def hug__command(self, ctx, member: discord.Member):
        await ctx.send(f"{ctx.author.mention} gave {member.mention} a massive hug")
        img = snuggle(member.avatar.url, ctx.author.avatar.url)
        await ctx.send(file=discord.File(img, "hug.gif"))

    @commands.command(name="huggle")
    async def hug__slash(self, ctx, member: discord.Member):
        await ctx.respond(f"{ctx.author.mention} gave {member.mention} a massive hug")
        img = snuggle(member.avatar.url, ctx.author.avatar.url)
        await ctx.respond(file=discord.File(img, "hug.gif"))

    # @commands.slash_command(name="compatibility_check",description="Check how compatible you are with another user"	)
    # async def compatibility_check(self,ctx, member : discord.Member):
    #    await ctx.respond(f"{ctx.author.mention} and {member.mention} are {random.randint(0,100)}% compatible :heart:")

    # @commands.command(name="match_making")
    # async def match_making(self,ctx):
    #    await ctx.send(f"{ctx.author.mention} and {random.choice(ctx.guild.members)} are {random.randint(0,100)}% compatible :heart:")

    @commands.command(
        name="todayschess",
        help="Gets you todays chess challenge",
    )
    async def todaysChess_(self, ctx):
        url = "https://chesspuzzle.net/Daily/Api"
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"{data['Puzzle']}", color=0x20BEFF)
        embed.set_image(url=data["Image"])
        embed.add_field(name="To Start:", value=data["Text"], inline=False)
        embed.add_field(name="url:", value=data["Link"], inline=False)
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.send(embed=embed)

    @commands.slash_command(name="todayschess", help="Gets you todays chess challenge")
    async def todaysChess(self, ctx):
        url = "https://chesspuzzle.net/Daily/Api"
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"{data['Puzzle']}", color=0x20BEFF)
        embed.set_image(url=data["Image"])
        embed.add_field(name="To Start:", value=data["Text"], inline=False)
        embed.add_field(name="url:", value=data["Link"], inline=False)
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
