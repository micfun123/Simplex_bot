from urllib.request import proxy_bypass
import discord
import datetime
import requests
from discord.ext import commands
from dotenv import load_dotenv
import os
import json


load_dotenv()

API_KEY = os.environ['Nasa']

class Nasa(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def apod(self, ctx, extra:str=None):
        """
        NASA Astronomy Picture of the Day
        """
        
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        url = 'https://api.nasa.gov/planetary/apod?api_key={NASA}&thumbs=True&hd'
        response = requests.get(url.format(NASA=API_KEY))
        data = response.json()
        embed = discord.Embed(title=data['title'], description=data['explanation'], color=0x00168B)
        if data["media_type"] == "image":
            embed.set_image(url=data["hdurl"])
        elif data["media_type"] == "video":
                embed.set_image(url=data['thumbnail'])
        embed.add_field(name='Link to image of the day/video', value=data['url'], inline=False)
        embed.set_footer(text=f'{date}')
        await ctx.send(embed=embed)

    @commands.slash_command(name="apod", description="NASA Astronomy Picture of the Day")
    async def apod_(self, ctx, extra:str=None):
        """
        NASA Astronomy Picture of the Day
        """
        
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        url = 'https://api.nasa.gov/planetary/apod?api_key={NASA}&thumbs=True&hd'
        response = requests.get(url.format(NASA=API_KEY))
        data = response.json()
        embed = discord.Embed(title=data['title'], description=data['explanation'], color=0x00168B)
        if data["media_type"] == "image":
            embed.set_image(url=data["hdurl"])
        elif data["media_type"] == "video":
                embed.set_image(url=data['thumbnail'])
        embed.add_field(name='Link to image of the day/video', value=data['url'], inline=False)
        embed.set_footer(text=f'{date}')
        await ctx.reply(embed=embed)
        
        
def setup(client):
    client.add_cog(Nasa(client))