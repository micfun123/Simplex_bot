import discord
from discord.ext import commands
import json
import os
from os import listdir
from os.path import isfile, join
import datetime
import humanfriendly

def micsid(ctx):
    return ctx.author.id == 481377376475938826 or ctx.author.id == 624076054969188363


def log(log):
    now = datetime.now()
    timern = now.strftime("%d/%m/%Y %H:%M:%S")

    with open('./other/log.txt', 'a') as f:
        f.write('\n')
        f.write(f"{timern} | {log}")

  

cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])

class Moderation(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    
    @commands.command()
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

    @commands.has_permissions(kick_members=True)  #kicks a person
    @commands.command(help = "kicks a person from server")
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)
            
     

    @commands.has_permissions(kick_members=True)  #warn a user with Dms
    @commands.command(help = "Dms the User with a warning")
    async def warn(self, ctx, user: discord.User, *, message=None):
        message = message or "This Message is a warning"
        await discord.User.send(user, message + (f"** Warned by {ctx.message.author} From server {message.server.name}**"))

    @commands.command(name="removereactions",help="Clear reactions from a message in the current channel")
    @commands.has_permissions(manage_messages=True)
    async def removereactions(self, ctx, id:int):
        message = await ctx.channel.fetch_message(id)
        await message.clear_reactions()
        await ctx.send("Removed")
        
    @commands.command()
    @commands.check(micsid)
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0x20BEFF)
        await ctx.send(embed=embed)
  
    @commands.command()
    @commands.check(micsid)
    async def serverlist(self, ctx):
        servers = list(self.client.guilds)
        guild = self.client.get_guild(id)
        for i in servers:
            a = join(i.name+' | '+str(i.member_count) +' | ' + str(i.owner.name) + ' | ' + str(i.owner.id))
            embed = discord.Embed(title=f"{i.name}", description=f"{a}", color=0x20BEFF)
            await ctx.send(embed=embed)
            
    #embed maker
    @commands.command(name="embed", help="Creates an embed")
    @commands.has_permissions(manage_messages=True)
    async def embedmaker_command(self,ctx,titeltext,descriptiontext,colour):
        embed = discord.Embed()
        embed.title = titeltext
        embed.description = descriptiontext
        embed.color = int(colour, 16)

        
        await ctx.send(embed=embed)
        
    @commands.slash_command(name="embed", help="Creates an embed")
    @commands.has_permissions(manage_messages=True)
    async def embedmaker_slash(self,ctx,titeltext,descriptiontext,colour):
        embed = discord.Embed()
        embed.title = titeltext
        embed.description = descriptiontext
        embed.color = int(colour, 16)

        
        await ctx.respond(embed=embed)

    @commands.command(aliases=['sendmsg'])
    @commands.check(micsid)
    async def dm(self, ctx, member: discord.Member, *, message):
        await ctx.message.delete()
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        role = ctx.guild.default_role

        if role not in channel.overwrites:
            overwrites = {
                role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(embed=discord.Embed(title="This channel is now under lockdown", color=discord.Colour.orange()))
        elif channel.overwrites[role].send_messages is True or \
                channel.overwrites[role].send_messages is None:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = False
            await channel.set_permissions(role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(embed=discord.Embed(title="This channel is now under lockdown.", color=discord.Colour.orange()))
        else:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = True
            await channel.set_permissions(role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have removed {channel.mention} from lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(embed=discord.Embed(title="This channel is no longer under lockdown.", color=discord.Colour.orange()))

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
        await member.timeout(until=discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
        await ctx.send(f"{member.mention} has been muted for {time} seconds.\nReason: {reason}")


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
    async def massban(self, ctx, members:commands.Greedy[discord.Member], *, reason):
        """
        Mass bans multiple members from the server. Reason is required.
        """
        if not len(members):
            await ctx.send("One or more required arguments are missing.")

        else:
            for target in members:
                await target.ban(reason=reason, delete_message_days=0)
                await ctx.send(f"Banned `{target}`")

    @commands.command(aliases=['ub'])
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        """
        Unbans a member from the server using their ID.
        """
        try:
            user = self.bot.get_user(id)
            await ctx.guild.unban(discord.Object(id=id), reason=f'Unbanned by {ctx.author}')
            await ctx.send(f'Unbanned `{user}`')

        except discord.NotFound:
            await ctx.send('Member not found.')

    
    @commands.command()
    async def invites(self, ctx, user:discord.Member=None):
        if user is None:
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == ctx.author:
                    total_invites += i.uses
            await ctx.send(f"You've invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")
        else:
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == user:
                    total_invites += i.uses

            await ctx.send(f"{user} has invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")

     
    @commands.command(help= "Shows a leaderboard of the most invites on ther server")
    async def inviteslb(self, ctx, user:discord.Member=None):
        em = discord.Embed(title="Leaderboard")
        total_invites = {}
        for invite in await ctx.guild.invites():
            try:
                total_invites[invite.inviter.name] += invite.uses
            except KeyError:
                total_invites[invite.inviter.name] = invite.uses
        total_invites = dict(sorted(total_invites.items(), reverse=True,  key=lambda item: item[1]))
        fields = [em.add_field(name=k, value=v, inline=False) for k, v in total_invites.items()]
        
        await ctx.send(embed=em)

    
    @commands.command(help = "Moves a message across servers or channels. Must use command on channel with the message")
    @commands.has_permissions(manage_messages=True)
    async def MoveMessage(self, ctx, channel: discord.TextChannel, message_id: int):
        """
        Moves a message to a different channel.
        """
        # Fetches the message
        msg = await ctx.channel.fetch_message(message_id)
        webhook = await channel.create_webhook(name="Mover")
        for message in channel.history(limit=100):
            await webhook.send(content=message.content,username=f"{msg.author.name}",avatar_url=f"{msg.author.avatar.url}")
            # If the message has attachments then send those too
            if msg.attachments is not None:
                for i in msg.attachments:
                    await webhook.send(i.url)

        # Delete the webhook
        await webhook.delete()

    #move channel
    @commands.command(help = "Moves a channel across servers or channels. Must use command on channel with the channel")
    @commands.has_permissions(manage_channels=True)
    async def MoveChannel(self, ctx, tochannel: discord.TextChannel, fromchannel: discord.TextChannel):
        """
        Moves a messages to a different channel.
        """
        # Fetches the message
        webhook = await tochannel.create_webhook(name="Mover")
        async for message in fromchannel.history(limit = None):
            #detect if the message is a empy embed
            try:
                    await webhook.send(content=message.content,username=f"{message.author.name}",avatar_url=f"{message.author.avatar.url}")
            except:
                    await webhook.send(embed=message.embeds[0])
            if message.attachments is not None:
                    for i in message.attachments:
                        await webhook.send(i.url)
            


    
    @commands.command(help = "Delete all messages from a user on the server")
    @commands.has_guild_permissions(manage_messages=True)
    async def purgeuser(self, ctx, user: discord.Member):
        """
        Purges all messages from a user across all channels.
        """
        for channel in ctx.guild.text_channels:
            await channel.purge(limit=None, check=lambda m: m.author == user)       
        await ctx.send(f"{user}'s messages have been deleted.")
    
    @commands.has_guild_permissions(manage_messages=True)
    @commands.command(help = "Delete all messages from a user on the server in time frame")
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
        await ctx.send(f"{user}'s messages have been deleted. this was only in the last {time} minutes.")

    #remove role from all
    @commands.command(help = "Remove a role from all members")
    @commands.has_guild_permissions(manage_roles=True)
    async def removeroleall(self, ctx, role: discord.Role):
        """
        Removes a role from all members.
        """
        for member in ctx.guild.members:
            await member.remove_roles(role)
        await ctx.send(f"{role} has been removed from all members.")


    #add role to all
    @commands.command(help = "Add a role to all members")
    @commands.has_guild_permissions(manage_roles=True)
    async def giveroleall(self, ctx, role: discord.Role):
        """
        Adds a role to all members.
        """
        for member in ctx.guild.members:
            await member.add_roles(role)
        await ctx.send(f"{role} has been added to all members.")

    #remove role from user
    @commands.command(help = "Remove a role from a user")
    @commands.has_guild_permissions(manage_roles=True)
    async def removerole(self, ctx, user: discord.Member, role: discord.Role):
        """
        Removes a role from a user.
        """
        await user.remove_roles(role)
        await ctx.send(f"{role} has been removed from {user}.")

    #add role to user
    @commands.command(help = "Add a role to a user")
    @commands.has_guild_permissions(manage_roles=True)
    async def giverole(self, ctx, user: discord.Member, role: discord.Role):
        """
        Adds a role to a user.
        """
        await user.add_roles(role)
        await ctx.send(f"{role} has been added to {user}.")

    #remove all roles from user
    @commands.command(help = "Remove all roles from a user")
    @commands.has_guild_permissions(manage_roles=True)
    async def removerolesfromuser(self, ctx, member: discord.Member):
        """
        Removes all roles from a user.
        """
        for i in member.roles:
            try:
                await member.remove_roles(i)
            except:
                print(f"Can't remove the role {i}")
        await ctx.send(f"All roles have been removed from {member}.")

   #make ticket
    @commands.command(help = "Make a ticket")
    async def maketicket(self, ctx):
        """
        Makes a ticket.
        """
        channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.author.name}")
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await channel.set_permissions(ctx.guild.default_role, read_messages=False)
        await channel.set_permissions(ctx.author, send_messages=True)
        await channel.set_permissions(ctx.author, read_messages=True)
        await channel.send(f"{ctx.author.mention} You have been assigned a ticket. Please use the ticket channel to communicate with the staff team. When you or a staff member belives the ticket is solved please use .closeticket <reason> ")
        await ctx.send(f"{ctx.author.mention} Your ticket has been created. Please use the ticket channel to communicate with the staff team.")
        await ctx.message.delete()
        
        

    #close ticket command
    @commands.command(help = "Close a ticket")
    async def closeticket(self, ctx, *, reason: str):
        """
        Closes a ticket.
        """
        if ctx.channel.name.startswith("ticket-"):
            # Creates a message
            await ctx.send(f"{ctx.author.mention} closed a ticket.\nReason: {reason}")
            await ctx.message.delete()
            # rename the channel old name + archive
            await ctx.channel.edit(name=f"{ctx.channel.name}-closed-Ticket")
            #try remove all users in channel perms
            for i in ctx.channel.members:
                try:
                    await ctx.channel.set_permissions(i, send_messages=False)
                    await ctx.channel.set_permissions(i, read_messages=False)
                except:
                    print(f"Can't remove perms from {i}")
        else:
            await ctx.send("This channel is not a ticket!")
        

    #deleat all old ticket
    @commands.command(help = "Delete all old tickets")
    @commands.has_guild_permissions(administrator=True)
    async def deletetickets(self, ctx):
        """
        Deletes all old tickets.
        """
        for channel in ctx.guild.text_channels:
            if "-closed-ticket" in channel.name:
                await channel.delete()
        await ctx.send(f"All old tickets have been deleted.")
        
    
    @commands.command(help="Prints all server roles and amount of members")
    async def roles(self,ctx):
        em = discord.Embed(title="The roles of the server",description="Shows you the amount of members in each role. ", color=0x00ff00)
        for roles in ctx.guild.roles:
            em.add_field(name=f"{roles.name} :",value=len(roles.members),inline=False)
        await ctx.send(embed=em)


    @commands.command(help="Reset all user names nick names")
    @commands.has_permissions(administrator=True)
    async def nicknamereset(self,ctx):
        await ctx.send("Nicknames reseting")
        for member in ctx.guild.members: # loop through every member in the guild
            try:
                await member.edit(nick=None)
            except:
                await ctx.send(f"cannot reset user {i}")
        await ctx.send("No more nick names. balence has been restored")    
    

def setup(client):
    client.add_cog(Moderation(client))
