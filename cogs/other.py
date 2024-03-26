from datetime import timedelta
import datetime
from lib2to3.pgen2.token import AWAIT
from pydoc import describe
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
import matplotlib.pyplot as plt
import random
from io import BytesIO
from base69 import encode_base69, decode_base69
import sympy
import matplotlib.pyplot as plt
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def latex_to_image(latex_expression):
    # Configure matplotlib to use the Agg backend
    plt.switch_backend("Agg")
    plt.rcParams["text.usetex"] = True
    plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"

    # Create a figure and plot the LaTeX expression
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, f"${latex_expression}$", fontsize=16, ha="center")

    # Set the size of the figure
    fig.set_size_inches(3, 1)

    # Convert the figure to a PNG image in memory
    image_stream = io.BytesIO()
    FigureCanvas(fig).print_png(image_stream)

    # Close the figure
    plt.close(fig)

    # Return the image stream
    image_stream.seek(0)
    return image_stream


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
        with open(i, "r", encoding="utf8") as f:
            for line in f:
                count += 1
        lines += count
    return lines


class utilities(commands.Cog):
    """All the utilities commands"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["sug", "suggestion"])
    async def suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_channel(908969607266730005)
        em = discord.Embed(
            title="Suggestion:", description=f"{suggestion}", color=discord.Color.blue()
        )
        em.set_footer(text=f"ID: {ctx.author.id}, By: {ctx.author.name}")
        x = await sid.send(embed=em)
        await x.add_reaction("✅")
        await x.add_reaction("❌")
        await ctx.send("Thank you for you suggestion!")

    @commands.command(name="serverinfo", help="Shows the server info")
    async def serverinfo_commands(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        channelamount = str(len(ctx.guild.channels))
        vcamounts = str(len(ctx.guild.voice_channels))
        roleamount = str(len(ctx.guild.roles))
        bots = str(len([m for m in ctx.guild.members if m.bot]))
        peopleusers = str(len([m for m in ctx.guild.members if not m.bot]))
        emoji_amount = str(len(ctx.guild.emojis))
        verificationlevel = str(ctx.guild.verification_level)
        if description == "None":
            description = "No Server description"

        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=discord.Color.blue(),
        )
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except:
            pass
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(
            name="Created: ",
            value=f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}>",
            inline=True,
        )
        embed.add_field(name="Member Count: ", value=memberCount, inline=True)
        embed.add_field(name="Real Users:", value=peopleusers, inline=True)
        embed.add_field(name="Bots", value=bots, inline=True)
        embed.add_field(name="Channel Count", value=channelamount, inline=True)
        embed.add_field(name="Voice Channel Count", value=vcamounts, inline=True)
        embed.add_field(name="Role Count", value=roleamount, inline=True)
        embed.add_field(name="Emoji Count", value=emoji_amount, inline=True)
        embed.add_field(name="Verification Level", value=verificationlevel, inline=True)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
        )

        await ctx.send(embed=embed)

    @commands.slash_command(name="server_info", description="Shows the server info")
    async def serverinfo_slash(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        channelamount = str(len(ctx.guild.channels))
        vcamounts = str(len(ctx.guild.voice_channels))
        roleamount = str(len(ctx.guild.roles))
        bots = str(len([m for m in ctx.guild.members if m.bot]))
        peopleusers = str(len([m for m in ctx.guild.members if not m.bot]))
        emoji_amount = str(len(ctx.guild.emojis))
        verificationlevel = str(ctx.guild.verification_level)

        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(
            name="Created: ",
            value=f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}>",
            inline=True,
        )
        embed.add_field(name="Member Count: ", value=memberCount, inline=True)
        embed.add_field(name="Real Users:", value=peopleusers, inline=True)
        embed.add_field(name="Bots", value=bots, inline=True)
        embed.add_field(name="Channel Count", value=channelamount, inline=True)
        embed.add_field(name="Voice Channel Count", value=vcamounts, inline=True)
        embed.add_field(name="Role Count", value=roleamount, inline=True)
        embed.add_field(name="Emoji Count", value=emoji_amount, inline=True)
        embed.add_field(name="Verification Level", value=verificationlevel, inline=True)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
        )

        await ctx.send(embed=embed)

    # gets user info of user on the discord
    @commands.command(
        aliases=["userinfo", "ui", "Whois"],
        help="Finds info about users on the discord.",
    )
    async def info(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(
            title=f"{user}'s info", description=f"Here's {user}'s info", color=0x00FF00
        )
        embed.add_field(name="Username:", value=user.name, inline=True)
        embed.add_field(name="ID:", value=user.id, inline=True)
        embed.add_field(name="Status:", value=user.status, inline=True)
        embed.add_field(name="Highest Role:", value=user.top_role, inline=True)
        embed.add_field(
            name="Joined Server:",
            value=user.joined_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"),
            inline=True,
        )
        embed.add_field(
            name="Created Account:",
            value=user.created_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"),
            inline=True,
        )
        embed.add_field(name="Bot?", value=user.bot, inline=True)
        embed.add_field(
            name="All Roles:",
            value=", ".join([role.mention for role in user.roles]),
            inline=True,
        )
        try:
            embed.set_footer(
                text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
            )
        except:
            embed.set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url="https://cdn.discordapp.com/embed/avatars/0.png",
            )
        try:
            embed.set_thumbnail(url=user.avatar.url)
        except:
            embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        await ctx.send(embed=embed)

    @commands.slash_command(
        name="userinfo", description="Finds info about users on the discord."
    )
    async def info_slash(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(
            title=f"{user}'s info", description=f"Here's {user}'s info", color=0x00FF00
        )
        embed.add_field(name="Username:", value=user.name, inline=True)
        embed.add_field(name="ID:", value=user.id, inline=True)
        embed.add_field(name="Status:", value=user.status, inline=True)
        embed.add_field(name="Highest Role:", value=user.top_role, inline=True)
        embed.add_field(
            name="Joined Server:",
            value=user.joined_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"),
            inline=True,
        )
        embed.add_field(
            name="Created Account:",
            value=user.created_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"),
            inline=True,
        )
        embed.add_field(name="Bot?", value=user.bot, inline=True)
        embed.add_field(
            name="All Roles:",
            value=", ".join([role.mention for role in user.roles]),
            inline=True,
        )
        try:
            embed.set_footer(
                text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
            )
        except:
            embed.set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url="https://cdn.discordapp.com/embed/avatars/0.png",
            )
        try:
            embed.set_thumbnail(url=user.avatar.url)
        except:
            embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        await ctx.respond(embed=embed)

    @commands.command(aliases=["Report"])
    async def bug(self, ctx, *, bug):
        channelbug = await self.client.fetch_channel(911996728167759902)
        await channelbug.send(
            f"Bug report:\n{bug}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}"
        )
        await ctx.send("Thank you for reporting this bug!")

    # @commands.command(aliases=["channel_stats", "channel_health", "channel_info", "channel_information"])
    # async def channel_status(self, ctx, channel: discord.TextChannel = None):
    #    if not channel:
    #        channel = ctx.channel
    #
    #    server_id = self.client.get_guild(self.client.guilds[0].id)
    #
    #    embed = discord.Embed(colour=discord.Colour.orange())
    #    embed.set_author(name="Channel Health:")
    #
    #    async with ctx.channel.typing():
    #        count = 0
    #        async for message in channel.history(limit=500000, after=datetime.today() - timedelta(days=100)): count += 1
    #
    #        if count >= 5000:
    #            average = "OVER 5000!"
    #            healthiness = "VERY HEALTHY"
    #
    #        else:
    #            try:
    #                average = round(count / 100, 2)
    #
    #                if 0 > server_id.member_count / average: healthiness = "VERY HEALTHY"
    #                elif server_id.member_count / average <= 5: healthiness = "HEALTHY"
    #                elif server_id.member_count / average <= 10: healthiness = "NORMAL"
    #                elif server_id.member_count / average <= 20: healthiness = "UNHEALTHY"
    #                else: healthiness = "VERY UNHEALTHY"
    #
    #            except ZeroDivisionError:
    #                average = 0
    #                healthiness = "VERY UNHEALTHY"
    #
    #        embed.add_field(name="­", value=f"# of members: {server_id.member_count}", inline=False)
    #        embed.add_field(name="­", value=f'# of messages per day on average in "{channel}" is: {average}', inline=False)
    #        embed.add_field(name="­", value=f"Channel health: {healthiness}", inline=False)
    #
    #        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["getcolor"])
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
                await ctx.send(
                    "Colour with hex code {}:".format(colour_code),
                    file=discord.File(file, "colour_file.png"),
                )
            await asyncio.sleep(1)

    @commands.has_permissions(change_nickname=True)
    @commands.command(aliases=["nick"], pass_context=True, no_pm=True)
    async def nickname(self, ctx, *, txt=None):
        """Change your nickname on a server. Leave empty to remove nick."""
        await ctx.message.delete()
        await ctx.message.author.edit(nick=txt)
        await ctx.send(self.bot.bot_prefix + "Changed nickname to: `%s`" % txt)

    @commands.command(name="botinfo", help="Finds info about the bot.")
    async def botinfo_(self, ctx):
        em = discord.Embed(title="Simplex")
        em.add_field(
            inline=False, name="Server Count", value=f"{len(self.client.guilds)}"
        )
        mlist = []
        for i in list(self.client.get_all_members()):
            mlist.append(i.name)
        em.add_field(inline=False, name="User Count", value=len(mlist))
        em.add_field(inline=False, name="Active users", value=f"{len(set(mlist))}")
        em.add_field(
            inline=False, name="Ping", value=f"{round(self.client.latency * 1000)}ms"
        )
        em.set_footer(text="Made by the Simplex Dev Team")
        em.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%", inline=False)
        em.add_field(
            name="Memory Usage",
            value=f"{psutil.virtual_memory().percent}%",
            inline=False,
        )
        em.add_field(
            name="Available Memory",
            value=f"{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%",
            inline=False,
        )
        em.add_field(name="Python code", value=f"{get_lines()} of code", inline=False)
        em.add_field(name="Commands", value=f"{len(self.client.commands)} of commands")

        await ctx.send(embed=em)

    @commands.slash_command(name="botinfo", description="Finds info about the bot.")
    async def botinfo(self, ctx):
        em = discord.Embed(title="Simplex")
        em.add_field(
            inline=False, name="Server Count", value=f"{len(self.client.guilds)}"
        )
        mlist = []
        for i in list(self.client.get_all_members()):
            mlist.append(i.name)
        em.add_field(inline=False, name="User Count", value=len(mlist))
        em.add_field(inline=False, name="Active users", value=f"{len(set(mlist))}")
        em.add_field(
            inline=False, name="Ping", value=f"{round(self.client.latency * 1000)}ms"
        )
        em.set_footer(text="Made by the Simplex Dev Team")
        em.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%", inline=False)
        em.add_field(
            name="Memory Usage",
            value=f"{psutil.virtual_memory().percent}%",
            inline=False,
        )
        em.add_field(
            name="Available Memory",
            value=f"{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%",
            inline=False,
        )
        em.add_field(name="Python code", value=f"{get_lines()} of code", inline=False)
        em.add_field(name="Commands", value=f"{len(self.client.commands)} of commands")

        await ctx.respond(embed=em)

    @commands.command(name="avatar", aliases=["av", "pfp"])
    async def avatar_(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.message.author

        message = discord.Embed(title=str(member), color=discord.Colour.orange())
        message.set_image(url=member.avatar.url)

        await ctx.send(embed=message)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self} has been loaded")
        global startTime
        startTime = time.time()

    @commands.command(name="Uptime")
    async def _uptime(self, ctx):
        # what this is doing is creating a variable called 'uptime' and assigning it
        # a string value based off calling a time.time() snapshot now, and subtracting
        # the global from earlier
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
        e = discord.Embed(title="Uptime", description=uptime, color=0x8BE002)
        await ctx.send(embed=e)

    @commands.command(aliases=["qr"], help="Generate a QR code")
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
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        img.save("qrcode.png")
        await ctx.send(file=discord.File("qrcode.png"))

    @commands.command(aliases=["donate"], help="Donate to the bot")
    async def donation(self, ctx):
        em = discord.Embed(
            title="Donation",
            description="Donate to the bot to help keep it running by covering my monthly costs. Anything extra that gets donated will be saved for future projects and to help fund uni. It may not be much to you by anything means a lot to me. Thank you for your kindness",
            color=0x8BE002,
        )
        em.add_field(
            name="Buy me a coffee",
            value="[Click here](https://www.buymeacoffee.com/Michaelrbparker)",
        )
        em.add_field(
            name="Monaro",
            value="43rsynRD1qtCA1po9myFsc7ti5havFcXUZPdSZuMexU4DnEyno55TE16eWqFkMLMbwZ7DuRW4ow5kcWzQQYu96NH7XMk6cE",
        )
        em.add_field(name="BTC", value="bc1qlp29r6llr8g6afpnwpdcdwlkawk7svzyw24emf")
        await ctx.send(embed=em)

    @commands.command(name="calc", aliases=["calculate"], help="Calculate something")
    async def _calc__(self, ctx, *, equation):
        calc = simpcalc.Calculate()
        ans = await calc.calculate(equation)
        await ctx.send(f"The equation is: {equation}\nThe answer is: {ans}")

    @commands.slash_command(name="latex", description="Convert LaTeX to image")
    async def _latex_slash(self, ctx, expression: str):
        try:
            # Configure matplotlib to use the Agg backend
            plt.switch_backend("Agg")
            plt.rcParams["text.usetex"] = True
            plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"

            # Calculate the required canvas size based on the length of the expression
            expression_length = len(expression)
            width = math.ceil(math.sqrt(expression_length))  # Round up the square root
            height = math.ceil(expression_length / width)

            # Create a figure and plot the LaTeX expression
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, f"${expression}$", fontsize=16, ha="center")

            # Set the size of the figure based on the calculated dimensions
            if width < 3:
                width = 3
            if height < 1:
                height = 1
            fig.set_size_inches(width, height)

            # Save the image to a file
            fig.savefig("latex.png")

            # Send the image
            await ctx.respond(file=discord.File("latex.png"))

            # Close the figure
            plt.close(fig)

            # Delete the image
            os.remove("latex.png")
        except Exception as e:
            await ctx.respond(f"Error: {e}")

    @commands.command(name="latex", aliases=["tex"], help="Convert LaTeX to image")
    async def _latex_(self, ctx, *, expression: str):
        try:
            # Configure matplotlib to use the Agg backend
            plt.switch_backend("Agg")
            plt.rcParams["text.usetex"] = True
            plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"

            # Calculate the required canvas size based on the length of the expression
            expression_length = len(expression)
            width = math.ceil(math.sqrt(expression_length))  # Round up the square root
            height = math.ceil(expression_length / width)

            # Create a figure and plot the LaTeX expression
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, f"${expression}$", fontsize=16, ha="center")

            # Set the size of the figure based on the calculated dimensions
            if width < 3:
                width = 3
            if height < 2:
                height = 2

            fig.set_size_inches(width, height)

            # Save the image to a file
            fig.savefig("latex.png")

            # Send the image
            await ctx.send(file=discord.File("latex.png"))

            # Close the figure
            plt.close(fig)

            # Delete the image
            os.remove("latex.png")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    # random num generator between two numbers
    @commands.command(name="rand", aliases=["random"], help="Generate a random number")
    async def _rand_(self, ctx, start: int, end: int):
        await ctx.message.delete()
        await ctx.send(f"The random number is: {random.randint(start, end)}")

    @commands.slash_command(name="rand", description="Generate a random number")
    async def _rand_slash(self, ctx, start: int, end: int):
        await ctx.respond(f"The random number is: {random.randint(start, end)}")

    # remind me
    @commands.command(
        name="remind", aliases=["remindme"], help="Remind me to do something"
    )
    async def _remind_(self, ctx, time: str, *, message):
        await ctx.message.delete()
        # dont allow any pings
        message = message.replace("@", "")
        embed = discord.Embed(
            title="Reminder",
            description=f"Reminder set for {time} from now",
            color=0x8BE002,
        )
        await ctx.send(embed=embed)
        await asyncio.sleep(int(time) * 60)
        embed = discord.Embed(
            title="Reminder", description=f"{message}", color=0x8BE002
        )
        await ctx.send(embed=embed)
        await ctx.send(f"{ctx.author.mention}")

    # detect if user joins a vc
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            if after.channel.name == "CUSTOM VC":
                # make a vc
                vc = await after.channel.clone()
                vc.name = member.name
                await vc.edit(name=member.name)
                await member.move_to(vc)
        # if user leaves a vc
        if before.channel is not None and after.channel is None:
            if before.channel.name == member.name:
                await member.move_to(None)
                await before.channel.delete()

    @commands.slash_command(describe="shows staff list")
    async def staff(self, ctx):
        staff = []
        for user in ctx.guild.members:
            if user.guild_permissions.administrator:
                if user.bot:
                    pass
                else:
                    staff.append(user.mention)
        embed = discord.Embed(
            title="Staff:", description=f"{', '.join(staff)}", color=0x8BE002
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(name="base69_encode", description="Encode a int to base69")
    async def _base69_encode_(self, ctx, *, num):
        await ctx.respond(encode_base69(int(num)))

    @commands.slash_command(name="base69_decode", description="Decode a base69 to int")
    async def _base69_decode_(self, ctx, *, int):
        await ctx.respond(decode_base69(int))

    @commands.slash_command(name="vote_simplex", description="Vote for simplex")
    async def _vote_simplex_(self, ctx):
        await ctx.respond("https://top.gg/bot/902240397273743361")

    @commands.command(description="gets the list of buy me a coffee supporters")
    async def supporters(self, ctx):
        token = os.getenv("BUYMEACOFFEE")
        headers = {"Authorization": f"Bearer {token}"}
        if not token:
            await ctx.send("No token found.")
        else:
            try:
                r = requests.get(
                    "https://developers.buymeacoffee.com/api/v1/subscriptions?status=active",
                    headers=headers,
                )

                r.raise_for_status()  # Raises an HTTPError for bad responses
                data = r.json()["data"]

                if data:
                    members = []
                    for entry in data:
                        payer_name = entry.get(
                            "payer_name", "N/A"
                        )  # Default to 'N/A' if 'payer_name' is not present

                        members.append(payer_name)
                        em = discord.Embed(
                            title="Supporters",
                            description=f"{', '.join(members)}",
                            color=0x8BE002,
                        )
                        em.set_footer(
                            text="Thank you for supporting Simplex, if you would like to support us, please use the donation command"
                        )
                        await ctx.send(embed=em)
                else:
                    await ctx.send("No active supporters found.")
            except requests.exceptions.RequestException as e:
                await ctx.send(f"An error occurred: {e}")


    async def fetch_supporters(self, url, headers):
        supporters = []
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            supporters.extend(data['data'])
            url = data.get('next_page_url')
        return supporters
    

    @commands.command(name="teaboard",description="A leaderboard of the top 10 buy me a coffee supporters")
    async def teaboard__command(self, ctx):
        try:
            token = os.getenv("BUYMEACOFFEE")
            headers = {"Authorization": f"Bearer {token}"}
            url = "https://developers.buymeacoffee.com/api/v1/supporters"
            
            # Fetch all supporters
            supporters = await self.fetch_supporters(url, headers)
            
            # Aggregate total coffees donated by each supporter
            supporter_totals = {}
            for supporter in supporters:
                supporter_name = supporter['supporter_name']
                coffees_donated = supporter['support_coffees']
                supporter_totals[supporter_name] = supporter_totals.get(supporter_name, 0) + coffees_donated
            
            # Sort supporters by total coffees donated
            sorted_supporters = sorted(supporter_totals.items(), key=lambda x: x[1], reverse=True)
            
            # Create leaderboard
            names = [f"{supporter[0]} - {supporter[1]} coffees" for supporter in sorted_supporters[:10]]
            
            embed = discord.Embed(
                title="Top 10 Supporters",
                description="Thank you to our top 10 supporters for their generous donations!",
                color=0x8BE002
            )
            for i, name in enumerate(names):
                embed.add_field(name=f"{i + 1}.", value=name, inline=False)
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.slash_command(name="teaboard", description="A leaderboard of the top 10 buy me a coffee supporters")
    async def teaboard_slash(self, ctx):
        try:
            token = os.getenv("BUYMEACOFFEE")
            headers = {"Authorization": f"Bearer {token}"}
            url = "https://developers.buymeacoffee.com/api/v1/supporters"
            
            # Fetch all supporters
            supporters = await self.fetch_supporters(url, headers)
            
            # Aggregate total coffees donated by each supporter
            supporter_totals = {}
            for supporter in supporters:
                supporter_name = supporter['supporter_name']
                coffees_donated = supporter['support_coffees']
                supporter_totals[supporter_name] = supporter_totals.get(supporter_name, 0) + coffees_donated
            
            # Sort supporters by total coffees donated
            sorted_supporters = sorted(supporter_totals.items(), key=lambda x: x[1], reverse=True)
            
            # Create leaderboard
            names = [f"{supporter[0]} - {supporter[1]} coffees" for supporter in sorted_supporters[:10]]
            
            embed = discord.Embed(
                title="Top 10 Supporters",
                description="Thank you to our top 10 supporters for their generous donations!",
                color=0x8BE002
            )
            for i, name in enumerate(names):
                embed.add_field(name=f"{i + 1}.", value=name, inline=False)
            await ctx.respond(embed=embed)
            
        except Exception as e:
            await ctx.respond(f"An error occurred: {e}")

def setup(client):
    client.add_cog(utilities(client))
