import imp
<<<<<<< HEAD
from datetime import datetime, timedelta
=======
import psutil

>>>>>>> 5dae97baa2fa239deacdcea8f91ab9d351862b3e
import discord
from discord.ext import commands
import asyncio


class utilities(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    

    @commands.command(aliases=['sug'])
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


        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)

<<<<<<< HEAD

    


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

=======
>>>>>>> 5dae97baa2fa239deacdcea8f91ab9d351862b3e
def setup(bot):
    bot.add_cog(utilities(bot))