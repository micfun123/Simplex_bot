import discord
import random
from discord.ext import commands
import qrcode
import numexpr as ne
import numpy

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

def setup(bot):
    bot.add_cog(Fun(bot))