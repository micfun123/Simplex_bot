import imp
from pydoc import describe
from discord import Embed
import wikipedia
from discord.ext import commands
import json
import os
import discord
import imp
from tools import log
import requests


class lookup(commands.Cog):
    def __init__(self, client): 
        self.client = client 




    @commands.command(aliases=['wikipedia'])
    async def wiki(self, ctx, *, query):
        embed = Embed(title="Wikipedia", description="Searching for {}".format(query), color=0x00ff00)
        page = wikipedia.summary(query, sentences=500)
        url = wikipedia.page(query).url
        embed.description = page
        embed.add_field(name="Link", value=url ,inline=False)
        await ctx.send(embed=embed)
       
    @commands.command()
    async def wikisearch(self, ctx, *, query):
        await ctx.send(wikipedia.search(query))

    @commands.command()
    async def covid(self, ctx,*, country):
        x = country.replace(" ", "%20")
        """
        Get Covid-19 stats from a country or the world.
        """
        try:
            url = f"https://coronavirus-19-api.herokuapp.com/countries/{x}"
            stats = requests.get(url)
            json_stats = stats.json()
            country = json_stats["country"]
            totalCases = json_stats["cases"]
            todayCases = json_stats["todayCases"]
            totalDeaths = json_stats["deaths"]
            todayDeaths = json_stats["todayDeaths"]
            recovered = json_stats["recovered"]
            active = json_stats["active"]
            critical = json_stats["critical"]
            casesPerOneMil = json_stats["casesPerOneMillion"]
            deathsPerOneMil = json_stats["deathsPerOneMillion"]
            totalTests = json_stats["totalTests"]
            testsPerOneMil = json_stats["testsPerOneMillion"]

            e = discord.Embed(
                title=f"Covid-19 stats of {country}",
                description="This is not live info. Therefore it might not be as accurate, but is approximate info.",
                color=discord.Colour.red()
            )
            e.add_field(name="Total Cases", value=totalCases, inline=True)
            e.add_field(name="Today's Cases", value=todayCases, inline=True)
            e.add_field(name="Total Deaths", value=totalDeaths, inline=True)
            e.add_field(name="Today's Deaths", value=todayDeaths, inline=True)
            e.add_field(name="Recovered", value=recovered, inline=True)
            e.add_field(name="Active", value=active, inline=True)
            e.add_field(name="Critical", value=critical, inline=True)
            e.add_field(name="Cases per one million", value=casesPerOneMil, inline=True)
            e.add_field(name="Deaths per one million", value=deathsPerOneMil, inline=True)
            e.add_field(name="Tests per one million", value=testsPerOneMil, inline=True)
            e.add_field(name="Total tests", value=totalTests, inline=True)
            e.set_thumbnail(url="https://www.osce.org/files/imagecache/10_large_gallery/f/images/hires/8/a/448717.jpg")

            await ctx.send(embed=e)
        except:
            await ctx.send(f" Invalid country name or API error! Try again later.")

    @commands.command()
    async def randomimg(self, ctx):
        """
        Get a random image from unsplash.com
        """
        url = "https://source.unsplash.com/random"
        r = requests.get(url)
        Embed = discord.Embed(title="Random Image", description="Random Image from unsplash.com", color=0x00ff00)
        Embed.set_image(url=r.url)
        await ctx.send(embed=Embed)

def setup(client):
    client.add_cog(lookup(client))
    
