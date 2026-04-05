
import discord
from discord.ext import commands
import os


def micsid(ctx):
    return ctx.author.id == 481377376475938826 or ctx.author.id == 624076054969188363



cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])


class BotMakerCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(micsid)
    async def msgserver(self, ctx, id: int, *, message):
        for guild in self.client.guilds:
            if guild.id == id:
                return await guild.text_channels[0].send(message)
        await ctx.send("guild not found")


    @commands.command()
    @commands.is_owner()
    async def serverlist(self, ctx):
        """Lists all servers the bot is in."""
        for guild in self.client.guilds:
            description = (
                f"Members: {guild.member_count}\n"
                f"Owner: {guild.owner} ({guild.owner.id})"
            )
            embed = discord.Embed(title=guild.name, description=description, color=0x20BEFF)
            await ctx.send(embed=embed)


    @commands.command(help="Dms all server owners")
    @commands.check(micsid)
    async def dm_owners(self, ctx, *, msg):
        await ctx.send("Sending...")
        mins = 0
        # predicts how long it will take
        mins = len(self.client.guilds) * 0.1
        await ctx.send(f"Estimated time: {mins} minutes")

        owners = []
        for server in self.client.guilds:
            tosend = server.owner
            owners.append(tosend)
        owners = list(set(owners))
        for i in owners:
            try:
                await i.send(msg)
            except:
                await ctx.send(f"Counld not send to {i}")
        await ctx.send("Done")

    @commands.command()
    @commands.check(micsid)
    async def ghoastping(self, ctx, *, member: discord.Member):
        for i in ctx.guild.channels:
            try:
                x = await i.send(f"{member.mention}")
                await x.delete()
            except:
                print(f"Can't send message in {i}")

    @commands.command()
    @commands.is_owner()
    async def change_status(self, ctx, *, status):
        status = status.replace("[[servers]]", str(len(self.client.guilds)))
        await self.client.change_presence(activity=discord.Game(name=status))
        await ctx.send(f"Status changed to {status}")


    @commands.command()
    @commands.is_owner()
    async def server_invite(self, ctx, *, server):
        guild = self.client.get_guild(int(server))
        if guild == None:
            await ctx.send("Server not found")
            return
        invite = await guild.channels[0].create_invite()
        await ctx.send(invite)

    @commands.command()
    @commands.is_owner()
    async def server_look_up(self, ctx, *, server):
        guild = self.client.get_guild(int(server))
        if guild == None:
            await ctx.send("Server not found")
            return
        embed = discord.Embed(
            title=guild.name, description=f"ID: {guild.id}", color=0xFF00C8
        )
        embed.add_field(
            name="Owner", value=f"{guild.owner.name}#{guild.owner.discriminator}"
        )
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(
            name="Created at", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
        )
        embed.add_field(name="Owner ID", value=guild.owner.id)

        try:
            embed.set_thumbnail(url=guild.icon.url)
        except:
            pass

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(BotMakerCommands(client))
