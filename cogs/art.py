
from turtle import color
import discord
from discord.ext import commands
from PIL import Image
import sys

from numpy import size

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

import io

from colorthief import ColorThief


class Art(commands.Cog):
    def __init__(self, client): 
        self.client = client 

    #colour converter
    @commands.command()
    async def hextorgb(self, ctx, *, color: str):
        """Converts a hex color to RGB"""
        try:
            color = int(color, 16)
            red = color >> 16
            green = (color >> 8) & 255
            blue = color & 255
            embed = discord.Embed(title="RGB", description=f"{red}, {green}, {blue}", color=color)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Invalid color")

    #hex converter
    @commands.command()
    async def RGBtoHex(self, ctx, *, color: str):
        """Converts RGB to Hex"""
        try:
            color = color.split(",")
            red = int(color[0])
            green = int(color[1])
            blue = int(color[2])
            embed = discord.Embed(title="Hex", description=f"#{red:02x}{green:02x}{blue:02x}", color=0x00ff00)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Invalid color")
        
    @commands.command(help = "Shows a colour from image")
    async def DominantColour(self, ctx, *, URL: str):
        fd = urlopen(URL)
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        em = discord.Embed(title="Dominant colour", color=0x20BEFF)
        em.add_field(name="RGB of dominant colour", value=f"{color_thief.get_color(quality=1)}")
        await ctx.send(embed=em)

    @commands.command(help = "Shows a colour palette from image")
    async def Palette(self, ctx, *, URL: str):
        fd = urlopen(URL)
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        em = discord.Embed(title="Palette", color=0x20BEFF)
        colorpal = color_thief.get_palette(color_count=10, quality=1)
        for i in range(len(colorpal)):
            em.add_field(name=f"{i+1}", value=f"{colorpal[i]}")
        await ctx.send(embed=em)



def setup(client):
    client.add_cog(Art(client))
    
