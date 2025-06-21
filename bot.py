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
        return "."

# Basic permission check
def mic(ctx):
    try:
        return ctx.author.id == 481377376475938826
    except:
        return False

# Bot setup
bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False),
)

# Optional: Help command override
class NewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, color=discord.Color.blue())
            embed.set_footer(text="Thank you for using Simplex!")
            await destination.send(embed=embed)

bot.help_command = NewHelp()

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

@commands.is_owner()
@bot.command(pass_context=True)
async def broadcast(ctx, *, msg):
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                await channel.send(msg)
                break
            except Exception:
                continue

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
                await bot.load_extension(f"cogs.{file[:-3]}")
                print(f"🔹 Loaded cog: {file}")
            except Exception as e:
                print(f"❌ Failed to load cog {file}: {e}")


# Start bot
if __name__ == "__main__":
    async def main():
        await load_cogs()
        await bot.start(TOKEN)

    asyncio.run(main())
