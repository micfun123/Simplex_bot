from urllib.request import proxy_bypass
import discord
import datetime
import requests
from discord.ext import commands 
from discord.commands import slash_command
from dotenv import load_dotenv
import os
import json
import time
from geopy.geocoders import Nominatim

load_dotenv()

API_KEY = os.environ['Nasa']

class Nasa(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="apod", description="NASA Astronomy Picture of the Day")
    async def apod_(self, ctx):
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

    @slash_command(name="apod", description="NASA Astronomy Picture of the Day")
    async def apod(self, ctx):
        """
        NASA Astronomy Picture of the Day (Slash Command)
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
        await ctx.respond(embed=embed)

    #where is ISS
    @commands.command(name="iss", description="Where is ISS")
    async def iss_(self, ctx):
        """
        Where is ISS
        """
        
        url = 'https://api.wheretheiss.at/v1/satellites/25544'
        response = requests.get(url)
        data = response.json()
        velocity = data['velocity']
        latitude = data['latitude']
        longitude = data['longitude']
        altitude = data['altitude']
        visibility = data['visibility']
        
        em = discord.Embed(title='Where is ISS', description='', color=0x00168B)
        em.add_field(name='Latitude', value=latitude, inline=True)
        em.add_field(name='Longitude', value=longitude, inline=True)
        em.add_field(name='Altitude', value=f"{altitude}km", inline=True)
        em.add_field(name='Velocity', value=f"{velocity}km/hr", inline=True)
        em.add_field(name='Visibility', value=visibility, inline=True)
        em.set_footer(text=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        await ctx.send(embed=em)
        
   
        
        
def setup(client):
    client.add_cog(Nasa(client))