import discord
import random
import aiohttp
import os
from os import listdir
from os.path import isfile, join
import json
import os
from dotenv import load_dotenv
from easy_pil import Editor, Canvas, Font, load_image, Text
from discordLevelingSystem import DiscordLevelingSystem, RoleAward, LevelUpAnnouncement
import asyncio

load_dotenv()


def mic(ctx):
    return ctx.author.id == 481377376475938826


def get_prefix(client, message):  ##first we define get_prefix
    with open(
        "prefixes.json", "r"
    ) as f:  ##we open and read the prefixes.json, assuming it's in the same file
        prefixes = json.load(f)  # load the json as prefixes
    return prefixes[str(message.guild.id)]  # recieve the prefix for the guild id given


def get_prefixe_guildid(client, guildid):  ##first we define get_prefix
    with open(
        "prefixes.json", "r"
    ) as f:  ##we open and read the prefixes.json, assuming it's in the same file
        prefixes = json.load(f)  # load the json as prefixes
    return prefixes[str(guildid)]  # recieve the prefix for the guild id given


from discord.ext import commands, tasks


intents = discord.Intents.all()
intents.presences = False
intents.members = True
intents.guilds = True
intents.voice_states = True


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def on_ready(self):
        """Called upon the READY event"""

        print("Bot is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""

        print(endpoint, "raised", error)

class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        messages = []
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=discord.Color.random())
            emby.set_footer(text=ending_note)
            message = await destination.send(embed=emby)
            messages.append(message)

        await asyncio.sleep(300)  # Wait for 5 minutes (300 seconds)
        for message in messages:
            await message.delete()  # Delete each message after 5 minutes


client = MyBot(
    command_prefix=(get_prefix),
    intents=intents,
    members=True,
    guilds=True,
    voice_states=True,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False)

)

client.help_command = NewHelpName()

# Custom ending note
ending_note = "Thank you for using simplex!\nIf you have any questions or concerns feel free to DM me.\n or join the support server https://discord.gg/d2gjWqFsTP. This will self destruct in 5 minutes."


async def update_activity(client):
    await client.change_presence(
        activity=discord.Game(f"On {len(client.guilds)} servers! | .help")
    )
    print("Updated presence")


@client.event
async def on_guild_join(guild):  # when the bot joins the guild
    with open("prefixes.json", "r") as f:  # read the prefix.json file
        prefixes = json.load(f)  # load the json file

    prefixes[str(guild.id)] = "."  # default prefix

    with open(
        "prefixes.json", "w"
    ) as f:  # write in the prefix.json "message.guild.id": "."
        json.dump(
            prefixes, f, indent=4
        )  # the indent is to make everything look a bit neater


@client.event
async def on_guild_remove(guild):  # when the bot is removed from the guild
    with open("prefixes.json", "r") as f:  # read the file
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))  # find the guild.id that bot was removed from

    with open("prefixes.json", "w") as f:  # deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)

    # get_guild_count



@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):  # command: bl!changeprefix ...
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:  # writes the new prefix into the .json
        json.dump(prefixes, f, indent=4)

    await ctx.send(
        f"Prefix changed to: {prefix}"
    )  # confirms the prefix it's been changed to
    # next step completely optional: changes bot nickname to also have prefix in the nickname
    name = f"{prefix}BotBot"


@client.event
async def on_ready():
    # Setting `Playing ` status
    print("we have powered on, I an alive.")
    await update_activity(client)
    channel = client.get_channel(925787897527926805)
    await channel.send("Online")


@client.command(hidden=True)
@commands.check(mic)
async def prefix(ctx):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    for guild in client.guilds:
        prefixes[str(guild.id)] = "."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@client.command(help="Gives you the ping of the bot")
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms ping time")


@client.command(help="Provides the voting link for the bot. This helps the bot")
async def vote(ctx):
    await ctx.send("Like the bot vote here https://top.gg/bot/902240397273743361")


@client.command(aliases=["source"], help="Gives you the source code of the bot")
async def contribute(ctx):
    await ctx.send(
        "If you want to help can take a look here https://github.com/micfun123/Simplex_bot"
    )


@client.command(help="tells you about the maker of the bot")
async def maker(ctx):
    await ctx.send(
        "This Bot was made by Michael you can find him as @michaelrbparker on Twitter if you want a bot.  His discord is Mic#8372. Want to support him buy him a coffee https://www.buymeacoffee.com/Michaelrbparker"
    )


@client.command(help="Link to the discord")
async def link(ctx):
    await ctx.send(
        "This Bot was made by Michael you can find him as @michaelrbparker on Twitter if you want a bot. Want to support him buy him a coffee https://www.buymeacoffee.com/Michaelrbparker. This will help get faster updates as well as keeping the bot online"
    )


@client.command()
async def server(ctx):
    await ctx.send("Want to join the sever join here https://discord.gg/d2gjWqFsTP ")


@client.command(hidden=True)
async def bond(ctx):
    await ctx.send(
        "Hello Mr. Bond I was not expecting you, currenty Simplex World does not have a secret service. I hear Artica is lovely this time of year."
    )


@client.command(hidden=True)
async def easter_egg(ctx):
    await ctx.send(
        "Did you think i would just give you the easter eggs. have fun finding them and good luck."
    )


@client.command(hidden=True)
async def echo(ctx, *, content: str):
    await ctx.send(f"{content} \n \n \n ||This was sent by {ctx.author}||")


@commands.is_owner()
@client.command(pass_context=True)
async def broadcast(ctx, *, msg):
    for server in client.guilds:
        for channel in server.text_channels:
            try:
                await channel.send(msg)
            except Exception:
                continue
            else:
                break


@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    with open("react.json") as f:
        data = json.load(f)
        for x in data:
            if (
                x["emoji"] == payload.emoji.name
                and x["message_id"] == payload.message_id
            ):
                role = discord.utils.get(
                    client.get_guild(payload.guild_id).roles, id=x["role_id"]
                )
                await payload.member.add_roles(role)
            else:
                pass


@client.event
async def on_raw_reaction_remove(payload):
    if not payload.guild_id:
        return
    with open("react.json") as f:
        data = json.load(f)
    for x in data:
        if x["emoji"] == payload.emoji.name and x["message_id"] == payload.message_id:
            guild = await client.fetch_guild(payload.guild_id)
            role = guild.get_role(x["role_id"])
            member = await guild.fetch_member(payload.user_id)
            await member.remove_roles(role)
        else:
            pass


@client.command(
    aliases=["purge"],
    help="Command were clear given number of messages if no number given 5 messages will be cleared as well as limited to 5",
)  # clear command
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


@client.event
async def on_message(message):
    if client.user.mentioned_in(message) and message.mention_everyone is False:
        if message.author.bot:
            return
        else:
            if message.reference is None:
                prefix = get_prefix(client, message)
                await message.channel.send(
                    f"Hello {message.author.mention} I am Simplex Bot the worlds best discord bot. My prefix for this server is {prefix} \n To see all of my commands type {prefix}help. If you need to speak to a dev feel free to DM me the bot"
                )
    if (
        "simplex" in message.clean_content.lower()
        and "love" in message.clean_content.lower()
    ):
        await message.add_reaction("❤")
        await message.add_reaction("<:SimplexLove:1035258994115231856>")

    if "hate simplex" in message.clean_content.lower():
        await message.add_reaction("💔")

    if "fuck simplex" in message.clean_content.lower():
        await message.add_reaction("🖕")

    if "fuck you simplex" in message.clean_content.lower():
        await message.add_reaction("🖕")

    await client.process_commands(message)


TOKEN = os.getenv("DISCORD_TOKEN")


def start_bot(client):
    lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
    no_py = [s.replace(".py", "") for s in lst]
    startup_extensions = ["cogs." + no_py for no_py in no_py]
    try:
        for cogs in startup_extensions:
            client.load_extension(cogs)  # Startup all cogs
            print(f"Loaded {cogs}")

        print("\nAll Cogs Loaded\n===============\nLogging into Discord...")
        client.run(
            TOKEN
        )  # Token do not change it here. Change it in the .env if you do not have a .env make a file and put DISCORD_TOKEN=Token

    except Exception as e:
        print(
            f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!"
        )


start_bot(client)
