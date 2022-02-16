import discord
from discord.ext import commands
import json
from datetime import datetime


def log(log):
    now = datetime.now()
    timern = now.strftime("%d/%m/%Y %H:%M:%S")

    with open('./other/log.txt', 'a') as f:
        f.write('\n')
        f.write(f"{timern} | {log}")

async def update_activity(client):
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} servers! | .help"))
    print("Updated presence")

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        cha = self.client.get_channel(925787897527926805)
        await cha.send(embed=discord.Embed(title="Join", description=f"Joined: {guild.name}"))
        await update_activity(self.client)
       
            

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        await update_activity(self.client)
        cha = self.client.get_channel(925787897527926805)
        await cha.send(embed=discord.Embed(title="Leave", description=f"Left: {guild.name}"))

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
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
                        minutes = minutes - (hours*60)
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


#    @commands.Cog.listener()
#    async def on_command_error(
#        self, ctx: commands.Context, error: commands.CommandError
#    ):
#        """Error handler.
#        Args:
#            ctx (commands.Context): Provided by system.
#            error (commands.CommandError): The error object.
#        Raises:
#            error: Raises error if undocumented.
#        """
#        toRaise = False
#        # raise error
#        # Command not found
#        if isinstance(error, commands.CommandNotFound):
#            if self.bot.command_prefix == '.':
#                if ctx.message.content[1] == "@":
#                    return
#                if ctx.message.content[1] == "#":
#                    return
#                if ctx.message.content[1] == ":":
#                    return
#                if ctx.message.content[1] == "a":
#                    return
#            await ctx.message.add_reaction("⁉️")
#            message = "Command not found."
#            log(message)
#        # On cooldown
#        elif isinstance(error, commands.CommandOnCooldown):
#            await ctx.message.add_reaction("❌")
#            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
#            log(message)
#        # User doesn't have permissions
#        elif isinstance(error, commands.MissingPermissions):
#            await ctx.message.add_reaction("🔐")
#            message = "No permissions."
#            log(message)
#        elif isinstance(error, commands.BadArgument):
#            await ctx.message.add_reaction("🤏")
#            message = "Bad arguement."
#            log(message)
#        # Not enough args
#        elif isinstance(error, commands.UserInputError):
#            await ctx.message.add_reaction("🤏")
#            message = f"Not all required arguements were passed, do `{self.bot.command_prefix}help {ctx.message.content[len(self.bot.command_prefix):]}`"
#            log(message)
#        elif isinstance(error, commands.MissingRequiredArgument):
#            await ctx.message.add_reaction("🤏")
#            message = f"Not all required arguements were passed, do `{self.bot.command_prefix}help {ctx.message.content[len(self.bot.command_prefix):]}`"
#            log(message)
#        # Mentioned member not found
#        elif isinstance(error, commands.MemberNotFound):
#            await ctx.message.add_reaction("🤷‍♂️")
#            message = "Couldn't find that member."
#            log(message)
#        # Bot doesn't have permissions
#        elif isinstance(error, discord.errors.Forbidden):
#            await ctx.message.add_reaction("📛")
#            message = "Bot doesn't have the permissions needed."
#            log(message)
#        # notowner
#        elif isinstance(error, commands.NotOwner):
#            await ctx.message.add_reaction("📛")
#            message = "You are not the bot owner."
#            log(message)
#        else:
#            message = "This is an undocumented error, it has been reported and will be patched in the next update."
#            toRaise = True
#            log(message)
#        await ctx.reply(embed=discord.Embed(title=message, color=0x992D22))
#        if toRaise:
#            # If this is an undocumented error, the code in this block will be run.
#            raise error
            

def setup(bot):
    bot.add_cog(Events(bot))

