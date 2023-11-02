import discord
from discord.ext import commands
import json
import os
from os import listdir
from os.path import isfile, join
import datetime
import humanfriendly
import sqlite3
import asyncio
import random
import re
import io
import chat_exporter


def micsid(ctx):
    return ctx.author.id == 481377376475938826 or ctx.author.id == 624076054969188363


def log(log):
    now = datetime.now()
    timern = now.strftime("%d/%m/%Y %H:%M:%S")

    with open("./other/log.txt", "a") as f:
        f.write("\n")
        f.write(f"{timern} | {log}")


cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])


class embed_makers(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Title", placeholder="Enter a title", required=True
            )
        )
        self.add_item(
            discord.ui.InputText(label="description", style=discord.InputTextStyle.long)
        )
        self.add_item(
            discord.ui.InputText(
                label="colour", placeholder="Enter a colour (in hex)", required=True
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="footer", placeholder="Enter a footer (optional)", required=False
            )
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.children[0].value, description=self.children[1].value
        )
        try:
            embed.colour = int(self.children[2].value, 16)
        except:
            pass
        try:
            embed.set_footer(text=self.children[3].value)
        except:
            pass
        # post the embed to the channel not reply
        await interaction.response.send_message("embed sent", ephemeral=True)
        await interaction.channel.send(embed=embed)


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.is_owner()
    # @commands.command()
    # async def make_file_table_ticketrs(self, ctx):
    #    con = sqlite3.connect('databases/ticket_channel_id.db')
    #    cur = con.cursor()
    #    cur.execute("CREATE table ticket_channel_id (userid it, channel_id int)")
    #    con.commit()
    #    con.close()
    #    await ctx.send("Table created")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reactrole(self, ctx):
        await ctx.send("Please use the slash command /reactrole")

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
        embedVar = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=embedVar)
        await msg.add_reaction(emoji)
        with open("react.json") as json_file:
            data = json.load(json_file)

            new_react_role = {
                "role_name": role.name,
                "role_id": role.id,
                "emoji": emoji,
                "message_id": msg.id,
            }

            data.append(new_react_role)

        with open("react.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.respond("Done", ephemeral=True)

    @commands.has_permissions(kick_members=True)  # kicks a person
    @commands.command(help="kicks a person from server")
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(
            title=f":boot: Kicked {user.name}!",
            description=f"Reason: {reason}\nBy: {ctx.author.mention}",
        )
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)

    @commands.has_permissions(kick_members=True)  # warn a user with Dms
    @commands.command(help="Dms the User with a warning")
    async def warn(self, ctx, user: discord.User, *, message=None):
        await ctx.message.delete()
        if message == None:
            await ctx.send("Please provide a message")
        else:
            await user.send(f"You have been warned in {ctx.guild.name} for {message}")
            await ctx.send(f"Warned {user.mention} for {message}")

    @commands.command(
        name="removereactions",
        help="Clear reactions from a message in the current channel",
    )
    @commands.has_permissions(manage_messages=True)
    async def removereactions(self, ctx, id: int):
        message = await ctx.channel.fetch_message(id)
        await message.clear_reactions()
        await ctx.send("Removed")

    @commands.command()
    @commands.check(micsid)
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=0x20BEFF,
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(micsid)
    async def serverlist(self, ctx):
        servers = list(self.client.guilds)
        guild = self.client.get_guild(id)
        for i in servers:
            a = join(
                i.name
                + " | "
                + str(i.member_count)
                + " | "
                + str(i.owner.name)
                + " | "
                + str(i.owner.id)
            )
            embed = discord.Embed(title=f"{i.name}", description=f"{a}", color=0x20BEFF)
            await ctx.send(embed=embed)

    # embed maker
    @commands.command(name="embed", help="Creates an embed")
    @commands.has_permissions(manage_messages=True)
    async def embedmaker_command(self, ctx):
        await ctx.send("This commmand has moved to slash commands")

    @commands.slash_command(name="embed", description="Creates an embed")
    @commands.has_permissions(manage_messages=True)
    async def embedmaker_slash(self, ctx: discord.ApplicationContext):
        modal = embed_makers(title="Embed Maker")
        await ctx.send_modal(modal)
        await ctx.respond("Done", ephemeral=True)

    @commands.command(aliases=["sendmsg"])
    @commands.check(micsid)
    async def dm(self, ctx, member: discord.Member, *, message):
        await ctx.message.delete()
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def regex_clear(self, ctx, limit=100, *, regex):
        await ctx.message.delete()
        regex = re.compile(regex)
        deleted = 0
        async for message in ctx.channel.history(limit=limit):
            if regex.search(message.content):
                await message.delete()
                deleted += 1
        await ctx.send(f"Deleted {deleted} messages.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        role = ctx.guild.default_role

        if role not in channel.overwrites:
            overwrites = {role: discord.PermissionOverwrite(send_messages=False)}
            await channel.edit(overwrites=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(
                embed=discord.Embed(
                    title="This channel is now under lockdown",
                    color=discord.Colour.orange(),
                )
            )
        elif (
            channel.overwrites[role].send_messages is True
            or channel.overwrites[role].send_messages is None
        ):
            overwrites = channel.overwrites[role]
            overwrites.send_messages = False
            await channel.set_permissions(role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(
                embed=discord.Embed(
                    title="This channel is now under lockdown.",
                    color=discord.Colour.orange(),
                )
            )
        else:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = True
            await channel.set_permissions(role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have removed {channel.mention} from lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(
                embed=discord.Embed(
                    title="This channel is no longer under lockdown.",
                    color=discord.Colour.orange(),
                )
            )

    @commands.command(aliases=["sm", "slowdown"])
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(ctx, seconds: int):
        """
        Sets slowmode for the current channel.
        """
        try:
            if seconds > 21600:
                await ctx.send("Slowmode cannot be more than 6 hours.")
                return
            elif seconds < 0:
                await ctx.send("Slowmode cannot be less than 0.")
                return
            elif seconds == 0:
                await ctx.channel.edit(slowmode_delay=0)
                await ctx.send("Slowmode has been disabled.")
                return

            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"Slowmode set to {seconds} seconds.")

        except discord.Forbidden:
            await ctx.send("I don't have permission to manage this channel.")

    @commands.command(aliases=["mute"])
    @commands.guild_only()
    @commands.has_guild_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, time, *, reason=None):
        """
        Timeouts a user for a set amount of time.
        Use 5m for 5 minutes, 1h for 1 hour, etc.
        """
        if reason is None:
            reason = "No reason provided"
        time = humanfriendly.parse_timespan(time)
        await member.timeout(
            until=discord.utils.utcnow() + datetime.timedelta(seconds=time),
            reason=reason,
        )
        await ctx.send(
            f"{member.mention} has been muted for {time} seconds.\nReason: {reason}"
        )

    @commands.command(aliases=["sn"])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member: discord.Member, *, nick):
        """
        Set a custom nick-name.
        """
        await member.edit(nick=nick)
        await ctx.send(f"Nickname for {member.name} was changed to {member.mention}")

    # make the ban command here

    @commands.command(aliases=["mb"])
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def massban(self, ctx, members: commands.Greedy[discord.Member], *, reason):
        """
        Mass bans multiple members from the server. Reason is required.
        """
        if not len(members):
            await ctx.send("One or more required arguments are missing.")

        else:
            for target in members:
                await target.ban(reason=reason, delete_message_days=0)
                await ctx.send(f"Banned `{target}`")

    @commands.command(aliases=["ub"])
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        """
        Unbans a member from the server using their ID.
        """
        try:
            user = self.bot.get_user(id)
            await ctx.guild.unban(
                discord.Object(id=id), reason=f"Unbanned by {ctx.author}"
            )
            await ctx.send(f"Unbanned `{user}`")

        except discord.NotFound:
            await ctx.send("Member not found.")

    @commands.command()
    async def invites(self, ctx, user: discord.Member = None):
        if user is None:
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == ctx.author:
                    total_invites += i.uses
            await ctx.send(
                f"You've invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!"
            )
        else:
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == user:
                    total_invites += i.uses

            await ctx.send(
                f"{user} has invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!"
            )

    @commands.command(help="Shows a leaderboard of the most invites on ther server")
    async def inviteslb(self, ctx, user: discord.Member = None):
        em = discord.Embed(title="Leaderboard")
        total_invites = {}
        for invite in await ctx.guild.invites():
            try:
                total_invites[invite.inviter.name] += invite.uses
            except KeyError:
                total_invites[invite.inviter.name] = invite.uses
        total_invites = dict(
            sorted(total_invites.items(), reverse=True, key=lambda item: item[1])
        )
        fields = [
            em.add_field(name=k, value=v, inline=False)
            for k, v in total_invites.items()
        ]

        await ctx.send(embed=em)

    @commands.command(
        help="Moves a message across servers or channels. Must use command on channel with the message"
    )
    @commands.has_permissions(manage_messages=True)
    async def MoveMessage(self, ctx, channel: discord.TextChannel, message_id: int):
        """
        Moves a message to a different channel.
        """
        # Fetches the message
        msg = await ctx.channel.fetch_message(message_id)
        webhook = await channel.create_webhook(name="Mover")
        for message in channel.history(limit=100):
            await webhook.send(
                content=message.content,
                username=f"{msg.author.name}",
                avatar_url=f"{msg.author.avatar.url}",
            )
            # If the message has attachments then send those too
            if msg.attachments is not None:
                for i in msg.attachments:
                    await webhook.send(i.url)

        # Delete the webhook
        await webhook.delete()

    # move channel
    @commands.command(
        help="Moves a channel across servers or channels. Must use command on channel with the channel"
    )
    @commands.has_permissions(manage_channels=True)
    async def MoveChannel(
        self, ctx, tochannel: discord.TextChannel, fromchannel: discord.TextChannel
    ):
        """
        Moves a messages to a different channel.
        """
        # Fetches the message
        webhook = await tochannel.create_webhook(name="Mover")
        async for message in fromchannel.history(limit=None):
            # detect if the message is a empy embed
            try:
                await webhook.send(
                    content=message.content,
                    username=f"{message.author.name}",
                    avatar_url=f"{message.author.avatar.url}",
                )
            except:
                await webhook.send(embed=message.embeds[0])
            if message.attachments is not None:
                for i in message.attachments:
                    await webhook.send(i.url)

    @commands.command(help="Delete all messages from a user on the server")
    @commands.has_guild_permissions(manage_messages=True)
    async def purgeuser(self, ctx, user: discord.Member):
        """
        Purges all messages from a user across all channels.
        """
        for channel in ctx.guild.text_channels:
            await channel.purge(limit=None, check=lambda m: m.author == user)
        await ctx.send(f"{user}'s messages have been deleted.")

    @commands.has_guild_permissions(manage_messages=True)
    @commands.command(
        help="Delete all messages from a user on the server in time frame"
    )
    async def timepurgeuser(self, ctx, user: discord.Member, time: int):
        """
        Purges all messages from a user across all channels.
        """
        dt = datetime.datetime.now() - datetime.timedelta(minutes=time)
        naive = dt.replace(tzinfo=None)
        for channel in ctx.guild.text_channels:
            for messages in await channel.history(limit=None).flatten():
                discordnaive = messages.created_at.replace(tzinfo=None)
                if discordnaive < naive:
                    await channel.purge(check=lambda m: m.author == user)
        await ctx.send(
            f"{user}'s messages have been deleted. this was only in the last {time} minutes."
        )

    # remove role from all
    @commands.command(help="Remove a role from all members")
    @commands.has_guild_permissions(manage_roles=True)
    async def removeroleall(self, ctx, role: discord.Role):
        predicted_time = len(ctx.guild.members) * 1.5
        await ctx.send(
            f"starting to remove {role} to all. This will take {predicted_time}"
        )
        """
        Removes a role from all members.
        """
        if role.position > ctx.guild.me.top_role.position:
            await ctx.send("The role is higher than my highest role.")
            return
        await ctx.send(f"starting to remove {role} to all")
        for member in ctx.guild.members:
            await member.remove_roles(role)
        await ctx.send(f"{role} has been removed from all members.")

    # add role to all
    @commands.command(help="Add a role to all members")
    @commands.has_guild_permissions(manage_roles=True)
    async def giveroleall(self, ctx, role: discord.Role):
        """
        Adds a role to all members.
        """
        # predicte how long it will take based on the amount of members and rate limit
        predicted_time = len(ctx.guild.members) * 1.5
        await ctx.send(
            f"starting to give {role} to all. This will take {predicted_time} seconds"
        )
        if role.position > ctx.guild.me.top_role.position:
            await ctx.send("The role is higher than my highest role.")
            return
        await ctx.send(f"starting to give {role} to all")
        for member in ctx.guild.members:
            try:
                await member.add_roles(role)
            except:
                pass
        await ctx.send(f"{role} has been added to all members.")

    # remove role from user
    @commands.command(help="Remove a role from a user")
    @commands.has_guild_permissions(manage_roles=True)
    async def removerole(self, ctx, user: discord.Member, role: discord.Role):
        """
        Removes a role from a user.
        """
        if role.position > ctx.guild.me.top_role.position:
            await ctx.send("The role is higher than my highest role.")
            return
        await user.remove_roles(role)
        await ctx.send(f"{role} has been removed from {user}.")

    # add role to user
    @commands.command(help="Add a role to a user")
    @commands.has_guild_permissions(manage_roles=True)
    async def giverole(self, ctx, user: discord.Member, *, role: discord.Role):
        """
        Adds a role to a user.
        """
        if role.position > ctx.guild.me.top_role.position:
            await ctx.send("The role is higher than my highest role.")
            return
        await user.add_roles(role)
        await ctx.send(f"{role} has been added to {user}.")

    # remove all roles from user
    @commands.command(help="Remove all roles from a user")
    @commands.has_guild_permissions(manage_roles=True)
    async def removerolesfromuser(self, ctx, member: discord.Member):
        """
        Removes all roles from a user.
        """
        for i in member.roles:
            try:
                await member.remove_roles(i)
            except:
                print(f"Can't remove the role {i} I do not have the perms")
        await ctx.send(f"All roles have been removed from {member}.")

    # make ticket
    @commands.command(name="maketicket", help="Make a ticket")
    async def maketicket__command(self, ctx):
        """
        Makes a ticket.
        """
        channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.author.name}")
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await channel.set_permissions(ctx.guild.default_role, read_messages=False)
        await channel.set_permissions(ctx.author, send_messages=True)
        await channel.set_permissions(ctx.author, read_messages=True)
        con = sqlite3.connect("databases/ticket_channel_id.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO ticket_channel_id VALUES (?, ?)", (ctx.author.id, channel.id)
        )
        con.commit()
        con.close()

        await channel.send(
            f"{ctx.author.mention} You have been assigned a ticket. Please use the ticket channel to communicate with the staff team. When you or a staff member belives the ticket is solved please use .closeticket <reason> "
        )
        await ctx.send(
            f"{ctx.author.mention} Your ticket has been created. Please use the ticket channel to communicate with the staff team."
        )
        await ctx.message.delete()

    @commands.slash_command(name="maketicket", help="Make a ticket")
    async def maketicket__slash(self, ctx):
        """
        Makes a ticket.
        """
        channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.author.name}")
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await channel.set_permissions(ctx.guild.default_role, read_messages=False)
        await channel.set_permissions(ctx.author, send_messages=True)
        await channel.set_permissions(ctx.author, read_messages=True)
        con = sqlite3.connect("databases/ticket_channel_id.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO ticket_channel_id VALUES (?, ?)", (ctx.author.id, channel.id)
        )
        con.commit()
        con.close()

        await channel.send(
            f"{ctx.author.mention} You have been assigned a ticket. Please use the ticket channel to communicate with the staff team. When you or a staff member belives the ticket is solved please use .closeticket <reason> "
        )
        await ctx.respond(
            f"{ctx.author.mention} Your ticket has been created. Please use the ticket channel to communicate with the staff team."
        )
        await ctx.message.delete()

    # close ticket command
    @commands.command(help="Close a ticket")
    async def closeticket(self, ctx, *, reason: str):
        if ctx.channel.name.startswith("ticket-"):
            """
            Closes a ticket.
            """
            # Creates a message
            transcript = await chat_exporter.export(
                ctx.channel,
                limit=1000,
                tz_info=str("UTC"),
                military_time=True,
            )
            if transcript is None:
                return
            transcript_file = discord.File(
                io.BytesIO(transcript.encode()),
                filename=f"transcript-{ctx.channel.name}.html",
            )
            # send with out embed
            await ctx.send(file=transcript_file, content="Here is the transcript")

            await ctx.send(f"{ctx.author.mention} closed a ticket.\nReason: {reason}")
            await ctx.message.delete()
            # rename the channel old name + archive
            await ctx.channel.edit(name=f"{ctx.channel.name}-closed-Ticket")
            # try remove all users in channel perms
            con = sqlite3.connect("databases/ticket_channel_id.db")
            cur = con.cursor()
            data = cur.execute(
                "SELECT * FROM ticket_channel_id WHERE channel_id = ?",
                (ctx.channel.id,),
            ).fetchall()
            user = self.client.get_user(data[0][0])
            await user.send(
                f"your ticket on {ctx.guild.name} has been closed for {reason}"
            )
            con.commit()
            con.close()
            for i in ctx.channel.members:
                try:
                    await ctx.channel.set_permissions(i, send_messages=False)
                    await ctx.channel.set_permissions(i, read_messages=False)
                except:
                    print(f"Can't remove perms from {i}")
            con = sqlite3.connect("databases/ticket_channel_id.db")
            cur = con.cursor()
            cur.execute(
                "DELETE FROM ticket_channel_id WHERE channel_id = ?", (ctx.channel.id,)
            )
            con.commit()
            con.close()
            await ctx.send("To remove all ticket channels please use .deletetickets ")
        else:
            await ctx.send("This channel is not a ticket!")

    # deleat all old ticket
    @commands.command(help="Delete all old tickets")
    @commands.has_permissions(administrator=True)
    async def deletetickets(self, ctx):
        """
        Deletes all old tickets.
        """
        for channel in ctx.guild.text_channels:
            if "-closed-ticket" in channel.name:
                await channel.delete()
        await ctx.send(f"All old tickets have been deleted.")

    @commands.command(help="Prints all server roles and amount of members")
    async def roles(self, ctx):
        em = discord.Embed(
            title="The roles of the server",
            description="Shows you the amount of members in each role. ",
            color=0x00FF00,
        )
        roles = ctx.guild.roles
        roles.reverse()
        for i in roles:
            if i.name == "@everyone" or i.is_bot_managed() or i.is_integration():
                roles.remove(i)

        # if roles are to long split them into 2 embeds
        if len(roles) > 25:
            for i in roles[:25]:
                em.add_field(name=i.name, value=len(i.members))
            await ctx.send(embed=em)
            em = discord.Embed(
                title="The roles of the server",
                description="Shows you the amount of members in each role. ",
                color=0x00FF00,
            )
            for i in roles[25:]:
                em.add_field(
                    name=i.name,
                    value=len(i.members),
                )
            await ctx.send(embed=em)
        else:
            for i in roles:
                em.add_field(name=i.name, value=len(i.members))
            await ctx.send(embed=em)

    @commands.command(help="Reset all user names nick names")
    @commands.has_permissions(administrator=True)
    async def nicknamereset(self, ctx):
        await ctx.send("Nicknames reseting")
        for member in ctx.guild.members:  # loop through every member in the guild
            try:
                await member.edit(nick=None)
            except:
                await ctx.send(f"cannot reset user {i}")
        await ctx.send("No more nick names. balence has been restored")

    @commands.command(help="UserID lookup")
    async def userid(self, ctx, memberid: int):
        member = ctx.guild.get_member(memberid)
        await ctx.send(f"{member} has the id {memberid}")

    @commands.has_permissions(administrator=True)
    @commands.command(help="Randomly bans a user")
    async def banrandom(self, ctx):
        await ctx.send("Are you sure you want to ban a random person? (yes/no)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.client.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
        else:
            if msg.content.lower() == "yes":
                await ctx.send("Ok, banning a random person now.")
                members = ctx.guild.members
                random_member = random.choice(members)
                await ctx.send(f"Banned {random_member}")
                await random_member.ban()
            elif msg.content.lower() == "no":
                await ctx.send("Ok, not banning a random person.")
            else:
                await ctx.send("That is not a valid answer. Please use yes or no")

    @commands.command(help="Exports all messages in a channel to html")
    @commands.has_permissions(administrator=True)
    async def export(
        self,
        ctx: commands.Context,
        limit=2000,
        tz_info: str = "UTC",
        military_time: bool = True,
    ):
        """Exports all messages in a channel to html"""
        await ctx.send("All systems go")
        await ctx.send("Exporting chat... (This is limited to 2000 messages)")
        transcript = await chat_exporter.export(
            ctx.channel, limit=limit, tz_info=tz_info, military_time=military_time
        )
        if transcript is None:
            return
        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{ctx.channel.name}.html",
        )
        # send with out embed
        # if file is too big, discord will not send it

        await ctx.send(file=transcript_file, content="Here is the transcript")


def setup(client):
    client.add_cog(Moderation(client))
