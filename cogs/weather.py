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
            await ctx.send(f"{CITY:-^30}")
            await ctx.send(f"Temperature: {x} degrees celcius")
            await ctx.send(f"Feels Like {y} degrees celcius")
            await ctx.send(f"Humidity: {humidity}")
            await ctx.send(f"Pressure: {pressure}")
            await ctx.send(f"Weather Report: {report[0]['main']}")
        else:
            # showing the error message
            await ctx.send("I've had a connection issue, Sir. Should be fixed momentarily")


    @commands.slash_command()
    async def weather(self, ctx, *, city):
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
            await ctx.respond(f"{city:-^30} \n Temperature: {x} degrees celcius \n Feels Like {y} degrees celcius \n Humidity: {humidity} \n Pressure: {pressure} \n Weather Report: {report[0]['main']}")
        else:
            # showing the error message
            await ctx.respond("I've had a connection issue, Sir. Should be fixed momentarily")

def setup(client):
    client.add_cog(Weather(client))
