
import discord
from discord.ext import commands
from discord import option
import os
import aiosqlite
import asyncio

def micsid(ctx):
    return ctx.author.id == 481377376475938826 or ctx.author.id == 624076054969188363

class BotMakerCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db_path = "databases/announcement.db"

    # --- Owner Announcement Commands ---

    @commands.command(name="announce", help="Send a message to all announcement channels")
    @commands.is_owner()
    async def announce(self, ctx, *, message):
        """Sends a message (with optional attachments) to all configured announcement channels."""
        await ctx.send("🔄 Sending announcements...")
        total = 0
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT ServerID, channel FROM server") as cursor:
                configs = await cursor.fetchall()
        
        config_map = {guild_id: channel_id for guild_id, channel_id in configs}

        for guild in self.client.guilds:
            channel_id = config_map.get(guild.id)
            target = None
            
            if channel_id:
                target = guild.get_channel(channel_id)
            
            if not target:
                target = guild.system_channel

            if target:
                try:
                    if ctx.message.attachments:
                        file = await ctx.message.attachments[0].to_file()
                        await target.send(message, file=file)
                    else:
                        await target.send(message)
                    total += 1
                except:
                    pass
            
            await asyncio.sleep(0.05) # Rate limit protection

        await ctx.send(f"✅ Sent to {total} out of {len(self.client.guilds)} servers")

    @commands.command(name="announce_embed")
    @commands.is_owner()
    async def announce_embed(self, ctx, title, *, message):
        """Sends an embed announcement to all configured channels."""
        await ctx.send("🔄 Sending embed announcements...")
        total = 0
        embed = discord.Embed(title=title, description=message, color=0x00FF00)
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT ServerID, channel FROM server") as cursor:
                configs = await cursor.fetchall()
        
        config_map = {guild_id: channel_id for guild_id, channel_id in configs}

        for guild in self.client.guilds:
            channel_id = config_map.get(guild.id)
            target = guild.get_channel(channel_id) if channel_id else guild.system_channel
            
            if target:
                try:
                    await target.send(embed=embed)
                    total += 1
                except:
                    pass
            await asyncio.sleep(0.05)

        await ctx.send(f"✅ Sent to {total} out of {len(self.client.guilds)} servers")

    # --- Guild Setup Slash Command ---

    @discord.slash_command(name="announcement_setup", description="Set the channel for bot announcements")
    @commands.has_permissions(administrator=True)
    @option("channel", discord.TextChannel, description="The channel where bot news will be posted")
    async def announce_setup_slash(self, ctx, channel: discord.TextChannel):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO server (ServerID, channel) VALUES (?, ?)
                ON CONFLICT(ServerID) DO UPDATE SET channel = EXCLUDED.channel
            """, (ctx.guild.id, channel.id))
            await db.commit()
        await ctx.respond(f"✅ Announcement channel set to {channel.mention}")

    # --- Original BotOwner Commands ---
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
