from pydoc import describe
from discord import Embed
import wikipedia
from discord.ext import commands, tasks
import json
import aiosqlite
import os
import discord
import random
from tools import log
import asyncio
import feedparser
import requests



class lookup(commands.Cog):
    def __init__(self, client): 
        self.client = client 
        self.rss_loop.start()




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
        
    @commands.command()
    async def nyt_top(self, ctx):
        """
        Get a most populare articale from the New York Times
        """
        url = "https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={}".format(os.environ.get("NYT_API_KEY"))
        r = requests.get(url)
        json_data = r.json()
        title = json_data["results"][0]["title"]
        url = json_data["results"][0]["url"]
        Embed = discord.Embed(title="Most Popular Article", description="Most Popular Article from the New York Times", color=0x00ff00)
        Embed.add_field(name="Title", value=title, inline=False)
        Embed.add_field(name="Link", value=url, inline=False)
        await ctx.send(embed=Embed)

    @commands.command()
    async def nyt_search(self, ctx, *, query):
        """
        Search for an article from the New York Times
        """
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&api-key={}".format(query, os.environ.get("NYT_API_KEY"))
        r = requests.get(url)
        json_data = r.json()
        title = json_data["response"]["docs"][0]["headline"]["main"]
        url = json_data["response"]["docs"][0]["web_url"]
        Embed = discord.Embed(title="Search Result", description="Search Result from the New York Times", color=0x00ff00)
        Embed.add_field(name="Title", value=title, inline=False)
        Embed.add_field(name="Link", value=url, inline=False)
        await ctx.send(embed=Embed)

    @commands.command()
    async def nyt_random(self, ctx):
        """
        Get a random article from the New York Times
        """
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key={}".format(os.environ.get("NYT_API_KEY"))
        r = requests.get(url)
        json_data = r.json()
        title = json_data["response"]["docs"][0]["headline"]["main"]
        url = json_data["response"]["docs"][0]["web_url"]
        Embed = discord.Embed(title="Random Article", description="Random Article from the New York Times", color=0x00ff00)
        Embed.add_field(name="Title", value=title, inline=False)
        Embed.add_field(name="Link", value=url, inline=False)
        await ctx.send(embed=Embed)
        
     #feet to cm
    @commands.command(help = "Convert feet to cm")
    async def ftocm(self, ctx, *, feet):
        try:
            cm = int(feet) * 30.48
            await ctx.send(f"{feet} feet is {cm} cm")
        except:
            await ctx.send("Invalid input")

    #cm to feet
    @commands.command(help = "Convert cm to feet")
    async def cmtof(self, ctx, *, cm):
        try:
            feet = int(cm) / 30.48
            await ctx.send(f"{cm} cm is {feet} feet")
        except:
            await ctx.send("Invalid input")

    #m to km
    @commands.command(help = "Convert m to km")
    async def mtokm(self, ctx, *, m):
        try:
            km = int(m) / 1000
            await ctx.send(f"{m} m is {km} km")
        except:
            await ctx.send("Invalid input")
    
    #km to m
    @commands.command(help = "Convert km to m")
    async def kmtom(self, ctx, *, km):
        try:
            m = int(km) * 1000
            await ctx.send(f"{km} km is {m} m")
        except:
            await ctx.send("Invalid input")

    #f to m
    @commands.command(help = "Convert f to m")
    async def ftom(self, ctx, *, f):
        try:
            m = int(f) * 0.3048
            await ctx.send(f"{f} f is {m} m")
        except:
            await ctx.send("Invalid input")

    #m to f
    @commands.command(help = "Convert m to f")
    async def mtof(self, ctx, *, m):
        try:
            f = int(m) / 0.3048
            await ctx.send(f"{m} m is {f} f")
        except:
            await ctx.send("Invalid input")

    #in to cm
    @commands.command(help = "Convert in to cm")
    async def intocm(self, ctx, *, ins):
        try:
            cm = int(ins) * 2.54
            await ctx.send(f"{ins} in is {cm} cm")
        except:
            await ctx.send("Invalid input")

    #cm to in
    @commands.command(help = "Convert cm to in")
    async def cmtoin(self, ctx, *, cm):
        try:
            ins = int(cm) / 2.54
            await ctx.send(f"{cm} cm is {ins} in")
        except:
            await ctx.send("Invalid input")
    
        #farenheit to celsius
    @commands.command(help = "Convert farenheit to celsius")
    async def ftoc(self, ctx, *, f):
        try:
            c = (int(f) - 32) * 5/9
            await ctx.send(f"{f} farenheit is {c} celsius")
        except:
            await ctx.send("Invalid input")
    
    #celsius to farenheit
    @commands.command(help = "Convert celsius to farenheit")
    async def ctof(self, ctx, *, c):
        try:
            f = (int(c) * 9/5) + 32
            await ctx.send(f"{c} celsius is {f} farenheit")
        except:
            await ctx.send("Invalid input")


    @commands.command(help = "Searches for images")
    async def image(self,ctx,search):
        token = os.getenv("serpapi")
        try:
            URL = f'https://serpapi.com/search.json?q={search}&tbm=isch&ijn=0&api_key={token}'
            results = requests.get(URL).json()
            em = discord.Embed(title=search,description="This is the image you searched for", color=0x00ff00)
            num = random.randint(0,10)
            url = results["images_results"][num]["original"]
            print(url)
            em.set_image(url=url)
            await ctx.send(embed=em)
        except:
            await ctx.send("The dev has ran out of credit. Please DM the bot to let him know.")


    @commands.slash_command(name="free_game", description="Get a free game")
    async def free(self, ctx):
        numnber = random.randint(0,100)
        apiurl = "https://www.freetogame.com/api/games"
        r = requests.get(apiurl)
        json_data = r.json()
        title = json_data[numnber]["title"]
        url = json_data[numnber]["game_url"]
        thumbnail = json_data[numnber]["thumbnail"]
        short_description = json_data[numnber]["short_description"]
        Embed = discord.Embed(title="Free Game", description=title, color=0x00ff00)
        Embed.add_field(name="Link", value=url, inline=False)
        Embed.add_field(name="Description", value=short_description, inline=False)
        Embed.set_thumbnail(url=thumbnail)
        
        await ctx.respond(embed=Embed)

    #@commands.command()
    #@commands.is_owner()
    #async def makerss_file(self, ctx):
    #    async with aiosqlite.connect("databases/rss.db") as db:
    #        await db.execute("CREATE TABLE IF NOT EXISTS rss (name text, url text, channel text,guild text,lastpost text)")
    #        await db.commit()
    #    await ctx.send("Done")

    @commands.slash_command(description="Allows you to manage your server RSS feeds")
    @commands.has_permissions(manage_guild=True)
    async def rss(self, ctx, *, options:discord.Option(str, "Select option", required=True, choices=["add", "remove", "list", "update"])):
        if options == "list":
            #open the sql database
            async with aiosqlite.connect("databases/rss.db") as db:
                cursor = await db.execute("SELECT * FROM rss WHERE guild = ?", (str(ctx.guild.id),))
                rows = await cursor.fetchall()
                if len(rows) == 0:
                    await ctx.respond("No feeds have been added yet")
                else:
                    Embed = discord.Embed(title="RSS Feeds", description="All the RSS feeds in the database", color=0x00ff00)
                    for row in rows:
                        Embed.add_field(name=row[0], value=row[1], inline=False)
                    await ctx.respond(embed=Embed)
        elif options == "add":
            async with aiosqlite.connect("databases/rss.db") as db:
                await db.execute("CREATE TABLE IF NOT EXISTS rss (name text, url text, channel text,guild text)")
                await db.commit()
            await ctx.respond("What is the name of the feed?")
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                name = await self.client.wait_for("message", check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.respond("You took too long to respond")
            else:
                await ctx.respond("What is the url of the feed?")
                try:
                    url = await self.client.wait_for("message", check=check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.respond("You took too long to respond")
                else:
                    await ctx.respond("What channel do you want to send the feed to?")
                    try:
                        channel = await self.client.wait_for("message", check=check, timeout=60)
                        #remove the # from the channel
                        channelinfo = channel.content.replace("#", "")
                        #remove the < and > from the channel
                        channelinfo = channelinfo.replace("<", "")
                        channelinfo = channelinfo.replace(">", "")

                        #verify the channel exists
                        channelcheck = self.client.get_channel(int(channelinfo))
                        if channelcheck == None:
                            await ctx.respond("That channel does not exist")
                            return
                        
                    except asyncio.TimeoutError:
                        await ctx.respond("You took too long to respond")
                    else:
                        async with aiosqlite.connect("databases/rss.db") as db:
                            await db.execute("INSERT INTO rss VALUES (?,?,?,?,?)", (name.content, url.content, channelinfo, ctx.guild.id,None))
                            await db.commit()
                        await ctx.respond("Done")

        elif options == "remove":
            async with aiosqlite.connect("databases/rss.db") as db:
                await db.execute("CREATE TABLE IF NOT EXISTS rss (name text, url text, channel text,guild text)")
                await db.commit()
            await ctx.respond("What is the name of the feed you want to remove?")
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                name = await self.client.wait_for("message", check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.respond("You took too long to respond")
            else:
                async with aiosqlite.connect("databases/rss.db") as db:
                    await db.execute("DELETE FROM rss WHERE name=? AND guild=?", (name.content, ctx.guild.id))
                    await db.commit()
                await ctx.respond("Done removing feed")
                
            
    @tasks.loop(seconds=60)
    async def rss_loop(self):
        print("Running RSS Loop")
        async with aiosqlite.connect("databases/rss.db") as db:
            await db.execute("CREATE TABLE IF NOT EXISTS rss (name text, url text, channel text,guild text, lastpost text)")
            await db.commit()
            cursor = await db.execute("SELECT * FROM rss")
            rows = await cursor.fetchall()
            for row in rows:
                
                feed = feedparser.parse(row[1])
                if row[4] == None:
                    await db.execute("UPDATE rss SET lastpost=? WHERE name=? AND guild=?", (feed.entries[0].link, row[0], row[3]))
                    await db.commit()
                else:
                    if feed.entries[0].link != row[4]:
                        channel = await self.client.fetch_channel(row[2])
                        print(channel)
                        Embed = discord.Embed(title=feed.entries[0].title, color=0x00ff00)

                        try:
                            Embed.description = feed.channel["description"]
                        except:
                            pass


                        try:
                            Embed.set_thumbnail(url=feed.channel["image"]["href"])
                        except:
                            try:
                                Embed.set_thumbnail(url=feed.entries[0].media_thumbnail[0]["url"])
                            except:
                                pass

                        try:
                            Embed.author(name=feed.channel["title"])
                        except:
                            pass

                        try:
                            Embed.set_footer(text=feed.entries[0].author)
                        except:
                            pass

                    
                        Embed.add_field(name="Link", value=feed.entries[0].link, inline=False)

                        try:
                            Embed.add_field(name="Summary", value=feed.entries[0].description, inline=False)
                        except:
                            try:
                                Embed.add_field(name="Summary", value=feed.entries[0].summary, inline=False)
                            except:
                                pass
                            




                        await channel.send(embed=Embed)
                        await db.execute("UPDATE rss SET lastpost=? WHERE name=? AND guild=?", (feed.entries[0].link, row[0], row[3]))
                        await db.commit()


             

    @rss_loop.before_loop
    async def before_rss_loop(self):
        await self.client.wait_until_ready()
        print("RSS Loop is ready")


    


def setup(client):
    client.add_cog(lookup(client))
    
