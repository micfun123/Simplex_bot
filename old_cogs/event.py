import discord
from discord.ext import commands
import json
from datetime import datetime


def log(log):
    now = datetime.now()
    timern = now.strftime("%d/%m/%Y %H:%M:%S")

    with open("./other/log.txt", "a") as f:
        f.write("\n")
        f.write(f"{timern} | {log}")


async def update_activity(client):
    await client.change_presence(
        activity=discord.Game(f"been a good boy on {len(client.guilds)}!")
    )
    print("Updated presence")


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        cha = self.client.get_channel(925787897527926805)
        await cha.send(
            embed=discord.Embed(
                title="Join",
                description=f"Joined: {guild.name}\n Owner: {guild.owner}\n Members: {guild.member_count}\n Server ID: {guild.id}",
                color=discord.Color.green(),
            )
        )
        await update_activity(self.client)
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name="Here's some stuff to get you started:")
        embed.add_field(
            name="Default Prefix: `.`",
            value="This can be changed later using `.changeprefix`",
        )
        embed.add_field(
            name="Disable Leveling", value="To disable leveling, use `.toggle_leveling`"
        )
        embed.add_field(
            name="Set Welcome",
            value="You can use `.welcome` to set a welcome message and channel ",
        )
        embed.add_field(
            name="Log messages",
            value="Use `.setLogChannel` to set a channel for logging removed,edited messages",
        )
        embed.add_field(
            name="Bot Announcements",
            value="Use `.set_announcment_channel [channel]` to set a channel for simplex announcements. Theses Announcments will include bug fixes and updates",
        )
        embed.add_field(
            name="Support",
            value="If you need support feel free to dm Me (the bot) and a human will reply to you ASAP or join the [Support Server](https://discord.gg/DCQWucrh2G) ",
        )
        embed.add_field(
            name="Sub_Reddit",
            value="If you want to support or to talk about the bot we also have a [Sub Reddit](https://www.reddit.com/r/SimplexBot/) ",
        )
        embed.add_field(
            name="Twitter",
            value="Maybe take a look at out twitter for events such as AMA and more! [Twitter](https://twitter.com/simplexbot) ",
        )
        embed.add_field(
            name="mastodon",
            value="We also have a mastodon account [Mastodon](https://mastodon.social/@simplex_bot) ",
        )
        embed.set_footer(
            text=f"Thank You - Simplex is now on {len(self.client.guilds)} servers!"
        )

        await guild.system_channel.send(
            content="**Thanks for inviting me! :wave: **", embed=embed
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await update_activity(self.client)
        cha = self.client.get_channel(925787897527926805)
        await cha.send(
            embed=discord.Embed(
                title="Leave",
                description=f"Left: {guild.name}",
                color=discord.Color.red(),
            )
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):

            async def better_time(cd: int):
                time = f"{cd}s"
                if cd > 60:
                    minutes = cd - (cd % 60)
                    seconds = cd - minutes
                    minutes = int(minutes / 60)
                    time = f"{minutes}min {seconds}s"
                    if minutes > 60:
                        hoursglad = minutes - (minutes % 60)
                        hours = int(hoursglad / 60)
                        minutes = minutes - (hours * 60)
                        time = f"{hours}h {minutes}min {seconds}s"
                return time

            cd = round(error.retry_after)
            if cd == 0:
                cd = 1
            retry_after = await better_time(cd)
            em = discord.Embed(
                title="Wow buddy, Slow it down\nThis command is on cooldown",
                description=f"Try again in **{retry_after}**",
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                title="Missing a requred value/arg",
                description="You haven't passed in all value/arg",
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(
                title="Missing permissions",
                description="You don't have permissions to use this commands",
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.BotMissingPermissions):
            em = discord.Embed(
                title="Missing permissions",
                description="I don't have permissions to use this commands",
            )
            await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_appliaction_command_error(self, ctx, error):
        log(f"ERROR: {error}")
        print(error)

        if isinstance(error, commands.CommandOnCooldown):

            async def better_time(cd: int):
                time = f"{cd}s"
                if cd > 60:
                    minutes = cd - (cd % 60)
                    seconds = cd - minutes
                    minutes = int(minutes / 60)
                    time = f"{minutes}min {seconds}s"
                    if minutes > 60:
                        hoursglad = minutes - (minutes % 60)
                        hours = int(hoursglad / 60)
                        minutes = minutes - (hours * 60)
                        time = f"{hours}h {minutes}min {seconds}s"
                return time

            cd = round(error.retry_after)
            if cd == 0:
                cd = 1
            retry_after = await better_time(cd)
            em = discord.Embed(
                title="Wow buddy, Slow it down\nThis command is on cooldown",
                description=f"Try again in **{retry_after}**",
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                title="Missing a requred value/arg",
                description="You haven't passed in all value/arg",
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(
                title="Missing permissions",
                description="You don't have permissions to use this commands",
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.BotMissingPermissions):
            em = discord.Embed(
                title="Missing permissions",
                description="I don't have permissions to use this commands",
            )
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Events(client))
