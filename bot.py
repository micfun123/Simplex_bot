import discord
import os
import json
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Load intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Helper function to get prefix from prefixes.json
def get_prefix(bot, message):
    try:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        return prefixes.get(str(message.guild.id), ".")
    except Exception:
        return "!"

# Bot setup
bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False),
)

class NewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        # Send the help message and schedule deletion
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, color=discord.Color.blue())
            embed.set_footer(text="Thank you for using Simplex!")
            help_message = await destination.send(embed=embed)

            # Schedule deletion after 5 minutes (300 seconds)
            async def delete_later(msg):
                await asyncio.sleep(300)
                try:
                    await msg.delete()
                except discord.NotFound:
                    pass

            # Run deletion task in background
            asyncio.create_task(delete_later(help_message))

    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

    def format_command(self, command):
        return f"**{self.get_command_signature(command)}** - {command.short_doc or 'No description'}"


# Events
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name=f"on {len(bot.guilds)} servers | .help"))

@bot.event
async def on_guild_join(guild):
    try:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
    except FileNotFoundError:
        prefixes = {}

    prefixes[str(guild.id)] = "."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    try:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id), None)
        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
    except FileNotFoundError:
        pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Easter egg response
    if "simplex" in message.content.lower() and "love" in message.content.lower():
        await message.add_reaction("❤")

    await bot.process_commands(message)

# Commands
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def vote(ctx):
    await ctx.send("Vote for the bot here: https://top.gg/bot/902240397273743361")

@bot.command(aliases=["source"])
async def contribute(ctx):
    await ctx.send("Contribute to the bot: https://github.com/micfun123/Simplex_bot")

@bot.command()
async def maker(ctx):
    await ctx.send("Made by Michael (@michaelrbparker). Buy him a coffee: https://www.buymeacoffee.com/Michaelrbparker")

@bot.command()
async def link(ctx):
    await ctx.send("Join the support server: https://discord.gg/d2gjWqFsTP")

@bot.command()
async def server(ctx):
    await ctx.send("Simplex server: https://discord.gg/d2gjWqFsTP")

@bot.command(hidden=True)
async def bond(ctx):
    await ctx.send("Hello Mr. Bond. I was not expecting you.")

@bot.command(hidden=True)
async def echo(ctx, *, content: str):
    await ctx.send(f"{content}\n\n||Sent by {ctx.author}||")

@bot.command(hidden=True)
async def easter_egg(ctx):
    await ctx.send("Did you think I'd just give you the easter eggs? Have fun finding them!")

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    try:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
    except FileNotFoundError:
        prefixes = {}

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"Prefix changed to: `{prefix}`")



@bot.command(aliases=["purge"])
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)

async def load_cogs():
    from os import listdir
    from os.path import isfile, join

    for file in listdir("./cogs"):
        if file.endswith(".py") and isfile(join("cogs", file)):
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
                print(f"🔹 Loaded cog: {file}")
            except Exception as e:
                print(f"❌ Failed to load cog {file}: {e}")


# Start bot
if __name__ == "__main__":
    async def main():
        await load_cogs()
        await bot.start(TOKEN)

    asyncio.run(main())
