
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
        """Converts RGB to hex"""
        try:
            color = int(color, 16)
            red = color >> 16
            green = (color >> 8) & 255
            blue = color & 255
            embed = discord.Embed(title="Hex", description=f"{color}", color=color)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Invalid color")
    
    @commands.command(help = "Shows a colour palette from image")
    async def palette(self, ctx, *, URL: str):
        fd = urlopen(URL)
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        em = discord.Embed(title="Dominant colour", color=0x20BEFF)
        em.add_field(name="RGB of dominant colour", value=f"{color_thief.get_color(quality=1)}")
        em.add_field(name="HEX of dominant colour", value=f"{color_thief.get_color(quality=1, format='hex')}")
        #turn RGB to image
        size = (100, 100)
        colour_code = color_thief.get_color(quality=1)
        image = Image.new("RGB", size, colour_code)
        with io.BytesIO() as file:
            image.save(file, "PNG")
            file.seek(0)
            em.set_image(file=discord.File(file, "colour_file.png"))

        await ctx.send(file=discord.File("palette.png"))
        
        print(color_thief.get_palette(quality=1))



def setup(client):
    client.add_cog(Art(client))
    
