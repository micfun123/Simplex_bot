from datetime import timedelta 
import datetime
from lib2to3.pgen2.token import AWAIT
from threading import activeCount
import discord
from discord.ext import commands
import asyncio
import time
import os
import psutil
import requests
import qrcode
import io
from PIL import Image
from simpcalc import simpcalc
from PyDictionary import PyDictionary
dictionary=PyDictionary()

calculator = simpcalc.Calculate()

def get_lines():
    lines = 0
    files = []
    for i in os.listdir():
        if i.endswith(".py"):
            files.append(i)
    for i in os.listdir("cogs/"):
        if i.endswith(".py"):
            files.append(f"cogs/{i}")
    for i in files:
        count = 0
        with open(i, 'r',encoding="utf8") as f:
            for line in f:
                count += 1
        lines += count
    return lines

class utilities(commands.Cog):
    ''' All the utilities commands '''
    def __init__(self, client): 
        self.client = client 
    

    @commands.command(aliases=['sug', 'suggestion'])
    async def suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_channel(908969607266730005)
        await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.send("Thank you for you suggestion!")

    @commands.command()
    async def serverinfo(self,ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        channelamount = str(len(ctx.guild.channels))
        vcamounts = str(len(ctx.guild.voice_channels))
        roleamount = str(len(ctx.guild.roles))


        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Created: ", value=f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}>", inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        embed.add_field(name="Channel Count", value=channelamount, inline=True)
        embed.add_field(name="Voice Channel Count", value=vcamounts, inline=True)
        embed.add_field(name="Role Count", value=roleamount, inline=True)



        await ctx.send(embed=embed)


    #gets user info of user on the discord
    @commands.command(aliases=["userinfo", "ui", "Whois"] ,help = "Finds info about users on the discord.")
    async def info(self,ctx, user: discord.Member):
        embed = discord.Embed(title=f"{user}'s info", description=f"Here's {user}'s info", color=0x00ff00)
        embed.add_field(name="Username:", value=user.name, inline=True)
        embed.add_field(name="ID:", value=user.id, inline=True)
        embed.add_field(name="Status:", value=user.status, inline=True)
        embed.add_field(name="Highest Role:", value=user.top_role, inline=True)
        embed.add_field(name="Joined Server:", value=user.joined_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"), inline=True)
        embed.add_field(name="Created Account:", value=user.created_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"), inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['Report'])
    async def bug(self, ctx, *, bug):
        channelbug = await self.client.fetch_channel(911996728167759902)
        await channelbug.send(f"Bug report:\n{bug}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.send("Thank you for reporting this bug!")

    @commands.command(aliases=["channel_stats", "channel_health", "channel_info", "channel_information"])
    async def channel_status(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        server_id = self.client.get_guild(self.client.guilds[0].id)

        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Channel Health:")

        async with ctx.channel.typing():
            count = 0
            async for message in channel.history(limit=500000, after=datetime.today() - timedelta(days=100)): count += 1

            if count >= 5000:
                average = "OVER 5000!"
                healthiness = "VERY HEALTHY"

            else:
                try:
                    average = round(count / 100, 2)

                    if 0 > server_id.member_count / average: healthiness = "VERY HEALTHY"
                    elif server_id.member_count / average <= 5: healthiness = "HEALTHY"
                    elif server_id.member_count / average <= 10: healthiness = "NORMAL"
                    elif server_id.member_count / average <= 20: healthiness = "UNHEALTHY"
                    else: healthiness = "VERY UNHEALTHY"

                except ZeroDivisionError:
                    average = 0
                    healthiness = "VERY UNHEALTHY"

            embed.add_field(name="­", value=f"# of members: {server_id.member_count}", inline=False)
            embed.add_field(name="­", value=f'# of messages per day on average in "{channel}" is: {average}', inline=False)
            embed.add_field(name="­", value=f"Channel health: {healthiness}", inline=False)

            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['getcolor'])
    async def getcolour(self, ctx, *, colour_codes):
        """Posts color of given hex"""
        await ctx.message.delete()
        colour_codes = colour_codes.split()
        size = (60, 80) if len(colour_codes) > 1 else (200, 200)
        if len(colour_codes) > 5:
            return await ctx.send(self.bot.bot_prefix + "Sorry, 5 colour codes maximum")
        for colour_code in colour_codes:
            if not colour_code.startswith("#"):
                colour_code = "#" + colour_code
            image = Image.new("RGB", size, colour_code)
            with io.BytesIO() as file:
                image.save(file, "PNG")
                file.seek(0)
                await ctx.send("Colour with hex code {}:".format(colour_code), file=discord.File(file, "colour_file.png"))
            await asyncio.sleep(1) 


    @commands.has_permissions(change_nickname=True)
    @commands.command(aliases=['nick'], pass_context=True, no_pm=True)
    async def nickname(self, ctx, *, txt=None):
        """Change your nickname on a server. Leave empty to remove nick."""
        await ctx.message.delete()
        await ctx.message.author.edit(nick=txt)
        await ctx.send(self.bot.bot_prefix + 'Changed nickname to: `%s`' % txt)

    @commands.command(name = "botinfo", help = "Finds info about the bot.")
    async def botinfo_(self, ctx):
        em = discord.Embed(title = 'Simplex')
        em.add_field(inline = False,name="Server Count", value=f"{len(self.client.guilds)}")
        mlist = []
        for i in list(self.client.get_all_members()):
            mlist.append(i.name)
        em.add_field(inline = False,name="User Count", value=len(mlist))
        em.add_field(inline = False,name="Active users", value=f"{len(set(mlist))}")
        em.add_field(inline = False,name="Ping", value=f"{round(self.client.latency * 1000)}ms")
        em.set_footer(text="Made by the Simplex Dev Team")
        em.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
        em.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
        em.add_field(name = 'Available Memory', value = f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline = False)
        em.add_field(name="Python code", value=f"{get_lines()} of code",inline = False)
        em.add_field(name="Commands", value=f"{len(self.client.commands)} of commands")

        await ctx.send(embed = em)


    @commands.slash_command(name = "botinfo", description = "Finds info about the bot.")
    async def botinfo(self, ctx):
        em = discord.Embed(title = 'Simplex')
        em.add_field(inline = False,name="Server Count", value=f"{len(self.client.guilds)}")
        mlist = []
        for i in list(self.client.get_all_members()):
            mlist.append(i.name)
        em.add_field(inline = False,name="User Count", value=len(mlist))
        em.add_field(inline = False,name="Active users", value=f"{len(set(mlist))}")
        em.add_field(inline = False,name="Ping", value=f"{round(self.client.latency * 1000)}ms")
        em.set_footer(text="Made by the Simplex Dev Team")
        em.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
        em.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
        em.add_field(name = 'Available Memory', value = f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline = False)
        em.add_field(name="Python code", value=f"{get_lines()} of code",inline = False)
        em.add_field(name="Commands", value=f"{len(self.client.commands)} of commands")

        await ctx.respond(embed = em)

    @commands.command(name="avatar",aliases=["av", "pfp"])
    async def avatar_(self, ctx, *, member: discord.Member = None):
        if not member:member=ctx.message.author

        message = discord.Embed(title=str(member), color=discord.Colour.orange())
        message.set_image(url=member.avatar.url)

        await ctx.send(embed=message)

    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 
        global startTime 
        startTime = time.time()

    @commands.command(name='Uptime')
    async def _uptime(self,ctx):

        # what this is doing is creating a variable called 'uptime' and assigning it
        # a string value based off calling a time.time() snapshot now, and subtracting
        # the global from earlier
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        e = discord.Embed(title="Uptime", description=uptime, color=0x8BE002)
        await ctx.send(embed=e)

    @commands.command(aliases=['qr'], help = "Generate a QR code")
    async def qrcode(self, ctx, *, url):
        await ctx.message.delete()
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

    @commands.command(aliases = ["donate"], help = "Donate to the bot")
    async def donation(self,ctx):
        em = discord.Embed(title = 'Donation', description = 'Donate to the bot to help keep it running!', color = 0x8BE002)
        em.add_field(name = ':BTC :', value = '**3Fi97A4fLw8Yycv7F3DwSfMgBJ3zjB1AFL**')
        em.add_field(name = ':ETH :', value = '**0x7Cfa740738ab601DCa9740024ED8DB585E2ed7478**')
        em.add_field(name = ':Doge :', value = '**DQVkWKqGoTGUY9MeN3HiUt49JfcC9aE7fp**')
        em.add_field(name = ':MPL  :', value = '**0xbDBb6403CA6D1681F0ef7A2603aD65a9F09AF138**')
        em.add_field(name = ':XMR  :', value = '**43rsynRD1qtCA1po9myFsc7ti5havFcXUZPdSZuMexU4DnEyno55TE16eWqFkMLMbwZ7DuRW4ow5kcWzQQYu96NH7XMk6cE**')
        em.add_field(name="Buy me a coffee", value="[Click here](https://www.buymeacoffee.com/Michaelrbparker)")
        await ctx.send(embed = em)
        

    @commands.command(name="calc", aliases=["calculate"], help = "Calculate something")
    async def _calc__(self, ctx, *, equation):
        calc = simpcalc.Calculate()
        ans = await calc.calculate(equation)
        await ctx.send(f"The equation is: {equation}\nThe answer is: {ans}")

    @commands.command(name="dict", aliases=["dictionary"], help = "Look up a word")
    async def _dict__(self, ctx, *, word):
        try:
            definition = dictionary.meaning(word)
            em = discord.Embed(title = word, description = definition, color = 0x8BE002)
            await ctx.send(embed = em)
        except:
            await ctx.send("Word not found")


def setup(bot):
    bot.add_cog(utilities(bot))