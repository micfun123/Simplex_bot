import discord
from datetime import datetime
from time import sleep
from geopy.geocoders import nominatim
from pip._vendor.requests import structures

import time
import geopy
import requests
import timezonefinder
from geopy import Nominatim
import nominatim 
from nominatim import Nominatim
from timezonefinder import TimezoneFinder
from discord.ext import commands
import dotenv
import os

class Weather(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    
    

    @commands.command()
    async def weather(self, ctx, *, CITY):
        weather_key = os.getenv("WEATHER_KEY")
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        URL = BASE_URL + "q=" + CITY + "&appid=" + weather_key + "&units=metric"
        # HTTP request
        response = requests.get(URL)
        # HTTP request
        response = requests.get(URL)
        # checking the status code of the request
        if response.status_code == 200:
            # getting data in the json format
            data = response.json()
            # getting the main dict block
            main = data['main']
            # getting temperature
            temperature = main['temp']
            feeling = main['feels_like']
            # getting the humidity
            humidity = main['humidity']   
            # getting the pressure
            pressure = main['pressure']
            # correcting temp values
            actualtemp = (temperature)
            actualfeel = (feeling)
            x = round(actualtemp)
            y = round(actualfeel)
            # weather report
            report = data['weather']
            #print
            e = discord.Embed(title="Weather Report", description="", color=0x00ff00)
            e.add_field(name="Temperature", value=str(x) + str(" degrees celcius"), inline=True)
            e.add_field(name="Feels Like", value=str(y) +  str(" degrees celcius"), inline=True)
            e.add_field(name="Humidity", value=humidity, inline=True)
            e.add_field(name="Pressure", value=pressure, inline=True)
            e.add_field(name="Weather", value=report[0]['description'], inline=True)
            e.set_thumbnail(url="https://static01.nyt.com/images/2014/12/11/technology/personaltech/11machin-illo/11machin-illo-articleLarge-v3.jpg?quality=75&auto=webp&disable=upscale")
            e.set_footer(text="Time: " + str(datetime.now()))
            await ctx.send(embed=e)
        else:
            # showing the error message
            await ctx.send("I've had a connection issue, Sir. Should be fixed momentarily")


    @commands.slash_command()
    async def weather_(self, ctx, *, city):
        weather_key = os.getenv("WEATHER_KEY")
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        URL = BASE_URL + "q=" + city + "&appid=" + weather_key + "&units=metric"
        # HTTP request
        response = requests.get(URL)
        # HTTP request
        response = requests.get(URL)
        # checking the status code of the request
        if response.status_code == 200:
            # getting data in the json format
            data = response.json()
            # getting the main dict block
            main = data['main']
            # getting temperature
            temperature = main['temp']
            feeling = main['feels_like']
            # getting the humidity
            humidity = main['humidity']   
            # getting the pressure
            pressure = main['pressure']
            # correcting temp values
            actualtemp = (temperature)
            actualfeel = (feeling)
            x = round(actualtemp)
            y = round(actualfeel)
            # weather report
            report = data['weather']
            #print
            e = discord.Embed(title="Weather Report", description="", color=0x00ff00)
            e.add_field(name="Temperature", value=str(x) + str(" degrees celcius"), inline=True)
            e.add_field(name="Feels Like", value=str(y) +  str(" degrees celcius"), inline=True)
            e.add_field(name="Humidity", value=humidity, inline=True)
            e.add_field(name="Pressure", value=pressure, inline=True)
            e.add_field(name="Weather", value=report[0]['description'], inline=True)
            e.set_thumbnail(url="https://static01.nyt.com/images/2014/12/11/technology/personaltech/11machin-illo/11machin-illo-articleLarge-v3.jpg?quality=75&auto=webp&disable=upscale")
            e.set_footer(text="Time: " + str(datetime.now()))
            await ctx.respond(embed=e)
        else:
            # showing the error message
            await ctx.respond("I've had a connection issue, Sir. Should be fixed momentarily")

def setup(client):
    client.add_cog(Weather(client))
