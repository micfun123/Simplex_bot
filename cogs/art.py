from random import random, choice
import discord
from discord.ext import commands
from PIL import Image
import sys
from io import BytesIO


from numpy import size

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    import urllib.request

import io

from colorthief import ColorThief


class Art(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(help="Shows a colour from image")
    async def DominantColour(self, ctx, *, URL: str):
        user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
        url = URL
        headers = {
            "User-Agent": user_agent,
        }
        request = urllib.request.Request(url, None, headers)
        fd = urllib.request.urlopen(request)
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        em = discord.Embed(title="Dominant colour", color=0x20BEFF)
        em.add_field(
            name="RGB of dominant colour", value=f"{color_thief.get_color(quality=1)}"
        )
        size = (100, 100)
        colour_code = color_thief.get_color(quality=1)
        image = Image.new("RGB", size, colour_code)
        with io.BytesIO() as file:
            image.save(file, "PNG")
            file.seek(0)
            await ctx.send(file=discord.File(file, filename="colour.png"))
        await ctx.send(embed=em)

    @commands.command(help="Shows a colour palette from image")
    async def Palette(self, ctx, *, URL: str):
        user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
        url = URL
        headers = {
            "User-Agent": user_agent,
        }
        request = urllib.request.Request(url, None, headers)
        fd = urllib.request.urlopen(request)
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        em = discord.Embed(title="Palette", color=0x20BEFF)
        colorpal = color_thief.get_palette(color_count=6, quality=1)
        for i in range(len(colorpal)):
            em.add_field(name=f"{i+1}", value=f"{colorpal[i]}")
            size = (100, 100)
            colour_code = colorpal[i]
            image = Image.new("RGB", size, colour_code)
            with io.BytesIO() as file:
                image.save(file, "PNG")
                file.seek(0)
                await ctx.send(file=discord.File(file, filename="colour.png"))

        await ctx.send(embed=em)

    # art prompt command
    @commands.command(name="artprompt", help="Prompts you to draw")
    async def ArtPrompt_command(self, ctx):
        lines = open("databases/ArtPrompt.txt").read().splitlines()
        myline = choice(lines)
        em = discord.Embed(
            title="Art Prompt. Have fun making", description=f"{myline}", color=0x20BEFF
        )
        await ctx.send(embed=em)

    @discord.slash_command(name="artprompt")
    async def artprompt_slashs(self, ctx):
        lines = open("databases/ArtPrompt.txt").read().splitlines()
        myline = choice(lines)
        em = discord.Embed(
            title="Art Prompt. Have fun making", description=f"{myline}", color=0x20BEFF
        )
        await ctx.respond(embed=em)

    # style prompt command
    @commands.command(name="styleprompt", help="Prompts you a Style to draw")
    async def StylePrompt_command(self, ctx):
        lines = open("databases/StylePrompt.txt").read().splitlines()
        myline = choice(lines)
        em = discord.Embed(
            title="Style Prompt. Have fun making",
            description=f"{myline}",
            color=0x20BEFF,
        )
        await ctx.send(embed=em)

    @discord.slash_command(name="styleprompt")
    async def styleprompt_slash(self, ctx):
        lines = open("databases/StylePrompt.txt").read().splitlines()
        myline = choice(lines)
        em = discord.Embed(
            title="Style Prompt. Have fun making",
            description=f"{myline}",
            color=0x20BEFF,
        )
        await ctx.respond(embed=em)



def setup(client):
    client.add_cog(Art(client))
