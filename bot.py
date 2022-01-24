from typing import Text
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

load_dotenv()

from discordLevelingSystem import DiscordLevelingSystem, RoleAward, LevelUpAnnouncement
from discord.ext import commands, tasks

intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.guilds=True
intents.all

client = commands.Bot(command_prefix = '.', intents=intents, presences = True, members = True, guilds=True)


async def update_activity(client):
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} servers! | .help"))
    print("Updated presence")

@client.event
async def on_ready():
    # Setting `Playing ` status
    print("we have powered on, I an alive.")
    await update_activity(client)
    channel = client.get_channel(925787897527926805)
    await channel.send("Online")


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms ping time')




@client.command()
async def vote(ctx):
    await ctx.send("Like the bot vote here https://top.gg/bot/902240397273743361")
    await ctx.send("Like the bot vote here https://discordbotlist.com/bots/simplex-bot")
    
    
@client.command(aliases=["Hello", "hi", "Hi"])
async def hello(ctx):
    await ctx.send('Hi')


@client.command()
async def contribute(ctx):
    await ctx.send('If you want to help can take a look here https://github.com/micfun123/Simplex_bot')

@client.command(help = "tells you about the maker of the bot", aliases=["maker"])
async def Maker(ctx):
    await ctx.send("This Bot was made by Michael you can find him as @michaelrbparker on Twitter if you want a bot.  His discord is Mic#8372. Want to support him buy him a coffee https://www.buymeacoffee.com/Michaelrbparker")

@client.command(help = "Link to the discord")
async def link(ctx):
    await ctx.send("This Bot was made by Michael you can find him as @michaelrbparker on Twitter if you want a bot. Want to support him buy him a coffee https://www.buymeacoffee.com/Michaelrbparker. This will help get faster updates as well as keeping the bot online")

@client.command()
async def server(ctx):
    await ctx.send('Want to join the sever join here https://discord.gg/d2gjWqFsTP ')

@client.command(aliases=["8ball", "eightball", "eight_ball", "Eight_ball"]) #8ball game
async def _8ball(ctx, *, question):
    responses = ['magic eight ball maintains Signs point to yes.',
                 'magicball affirms My reply is no.',
                 'magic ball answers Signs point to yes.',
                 'magicball affirms Yes definitely.',
                 'magicball affirms Yes.',
                 '8 ball magic said Most likely.',
                 'magic ball answers Very doubtful.',
                 'magic 8 ball answers Without a doubt.',
                 'mystic eight ball said Most likely.',
                 "magic ball answers Don't count on it.",
                 'Magic ball says 100% No',
                 'Magic ball does not know have you tryed google?',
                 "Its not looking so good"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    
@client.command(aliases=["doggo"], help = "It shows you a Dog photo as well as a fact") #shows a dog photo and a fact
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()

   embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.set_footer(text=factjson['fact'])
   await ctx.send(embed=embed)

@client.command(help = "It shows you a cat photo as well as a fact") #shows cat photo and fact
async def cat(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      catjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/cat')
      factjson = await request2.json()

   embed = discord.Embed(title="Cat!", color=discord.Color.purple())
   embed.set_image(url=catjson['link'])
   embed.set_footer(text=factjson['fact'])
   await ctx.send(embed=embed)


@client.command(aliases=["Joke", "jokes", "Jokes"], help = "It tells a joke")  #tells a joke
async def joke(ctx):
   async with aiohttp.ClientSession() as session:
      # This time we'll get the joke request as well!
      request = await session.get('https://some-random-api.ml/joke')
      jokejson = await request.json()


   embed = discord.Embed(title="I know its funny", color=discord.Color.purple())
   embed.set_footer(text=jokejson['joke'])
   await ctx.send(embed=embed) 

           

#gets user info of user on the discord
@client.command(aliases=["userinfo"] ,help = "Finds info about users on the discord.")
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title=f"{user}'s info", description=f"Here's {user}'s info", color=0x00ff00)
    embed.add_field(name="Username:", value=user.name, inline=True)
    embed.add_field(name="ID:", value=user.id, inline=True)
    embed.add_field(name="Status:", value=user.status, inline=True)
    embed.add_field(name="Highest Role:", value=user.top_role, inline=True)
    embed.add_field(name="Joined:", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)


#unban user 
@client.command(help = "Unbans a user from the server")
@commands.has_permissions(kick_members=True)
async def unban(ctx, user: discord.User, *, reason=None):
    await ctx.guild.unban(user, reason=reason)

@client.command(hidden = True)
async def bond(ctx):
    await ctx.send('Hello Mr. Bond I was not expecting you, currenty Misfire does not have a secret service. I hear Artica is lovely this time of year.')

@client.command(hidden = True)
async def easter_egg(ctx):
    await ctx.send("Did you think i would just give you the easter eggs. have fun finding them and good luck.")
    
@client.command()
async def invite(ctx):
    await ctx.send("Invite the bot here https://discord.com/api/oauth2/authorize?client_id=902240397273743361&permissions=8&scope=bot")

@client.command(hidden=True)
async def echo(ctx, *, content:str):
    await ctx.send(content)
    
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
            if x['emoji'] == payload.emoji.name and x["message_id"] == payload.message_id:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])
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
        if x['emoji'] == payload.emoji.name and x["message_id"] == payload.message_id:
            guild = await client.fetch_guild(payload.guild_id)
            role = guild.get_role(x['role_id'])
            member = await guild.fetch_member(payload.user_id)
            await member.remove_roles(role)
        else:
            pass
        
lvlembed = discord.Embed()
lvlembed.set_author(name=LevelUpAnnouncement.Member.name, icon_url=LevelUpAnnouncement.Member.avatar_url)
lvlembed.description = f'Congrats {LevelUpAnnouncement.Member.mention}! You are now level {LevelUpAnnouncement.LEVEL} 😎'

announcement = LevelUpAnnouncement(lvlembed)

lvl = DiscordLevelingSystem(rate=1, per=60, level_up_announcement=announcement)
lvl.connect_to_database_file(r'databases/DiscordLevelingSystem.db')

@client.event
async def on_message(message):
    await lvl.award_xp(amount=15, message=message)
    await client.process_commands(message)

@client.command(aliases=['lvl'])
async def rank(ctx, member:discord.Member=None):
    if member == None:
      data = await lvl.get_data_for(ctx.author)
    else:
      data = await lvl.get_data_for(member)

    LEVELS_AND_XP = {
        '0': 0,'1': 100,'2': 255,'3': 475,
        '4': 770,'5': 1150,'6': 1625,'7': 2205,'8': 2900,'9': 3720,'10': 4675,'11': 5775,'12': 7030,
        '13': 8450,'14': 10045,'15': 11825,'16': 13800,'17': 15980,'18': 18375,'19': 20995,'20': 23850,
        '21': 26950,'22': 30305,'23': 33925,'24': 37820,'25': 42000,'26': 46475,'27': 51255,'28': 56350,
        '29': 61770,'30': 67525,'31': 73625,'32': 80080,'33': 86900,'34': 94095,'35': 101675,'36': 109650,
        '37': 118030,'38': 126825,'39': 136045,'40': 145700,'41': 155800,'42': 166355,'43': 177375,'44': 188870,
        '45': 200850,'46': 213325,'47': 226305,'48': 239800,'49': 253820,'50': 268375,'51': 283475,'52': 299130,
        '53': 315350,'54': 332145,'55': 349525,'56': 367500,'57': 386080,'58': 405275,'59': 425095,'60': 445550,
        '61': 466650,'62': 488405,'63': 510825,'64': 533920,'65': 557700,'66': 582175,'67': 607355,'68': 633250,
        '69': 659870,'70': 687225,'71': 715325,'72': 744180,'73': 773800,'74': 804195,'75': 835375,'76': 867350,
        '77': 900130,'78': 933725,'79': 968145,'80': 1003400,'81': 1039500,'82': 1076455,'83': 1114275,'84': 1152970,
        '85': 1192550,'86': 1233025,'87': 1274405,'88': 1316700,'89': 1359920,'90': 1404075,'91': 1449175,'92': 1495230,
        '93': 1542250,'94': 1590245,'95': 1639225,'96': 1689200,'97': 1740180,'98': 1792175,'99': 1845195,'100': 1899250
    }
    
    if member == None:
      member = ctx.author
    else:
      pass
    arank = data.xp
    brank = LEVELS_AND_XP[f"{data.level+1}"]
    frac = arank/brank
    percentage = "{:.0%}".format(frac)
    percentage = int(percentage[:-1])

    user_data = {  # Most likely coming from database or calculation
    "name": f"{member.name}",  # The user's name
    "xp": arank,
    "level": data.level,
    "next_level_xp": brank,
    "percentage": percentage,
    "rank": data.rank
    }

    background = Editor(Canvas((934, 282), "#23272a"))
    profile_image = load_image(str(member.display_avatar.url))
    profile = Editor(profile_image).resize((150, 150)).circle_image()


    poppins = Font.poppins(size=30)

    background.rectangle((20, 20), 894, 242, "#2a2e35")
    background.paste(profile, (50, 50))
    background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
    background.bar(
        (260, 180),
        max_width=630,
        height=40,
        percentage=user_data["percentage"],
        fill="#00fa81",
        radius=20,
    )
    background.text((270, 120), user_data["name"], font=poppins, color="#00fa81")
    background.text(
        (870, 125),
        f"{user_data['xp']} / {user_data['next_level_xp']}",
        font=poppins,
        color="#00fa81",
        align="right",
    )

    rank_level_texts = [
        Text("Rank ", color="#00fa81", font=poppins),
        Text(f"{user_data['rank']}", color="#1EAAFF", font=poppins),
        Text("   Level ", color="#00fa81", font=poppins),
        Text(f"{user_data['level']}", color="#1EAAFF", font=poppins),
    ]

    background.multicolor_text((850, 30), texts=rank_level_texts, align="right")

    # send
    background.save(f"rank{member.id}.png")
    await ctx.send(file=discord.File(f"rank{member.id}.png"))
    os.remove(f"rank{member.id}.png")


@client.command()
@commands.is_owner()
async def removexp(ctx, member:discord.Member, amount:int):
    await ctx.message.delete()
    await lvl.remove_xp(member=member, amount=amount)


@client.command()
@commands.is_owner()
async def setlvl(ctx, member:discord.Member, level:int):
    await ctx.message.delete()
    await lvl.set_level(member=member, level=level)

@client.command()
async def givexp(ctx, member:discord.Member, amount:int):
    await lvl.remove_xp(member=ctx.author, amount=amount)
    await lvl.add_xp(member=member, amount=amount)
    await ctx.send(f"Gave {amount} xp to {member.name}, Removed {amount} xp from {ctx.author.name}")

@client.command(aliases=["purge"], help = "Command were clear given number of messages if no number given 5 messages will be cleared as well as limited to 5")  # clear command
@commands.has_permissions(administrator=True) 
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)

@client.command()
async def leaderboard(ctx):
    data = await lvl.each_member_data(ctx.guild, sort_by='rank')
    em = discord.Embed(title="Leaderboard")
    n = 0
    for i in data:
      em.add_field(name=f'{i.rank}: {i.name}', value=f'Level: {i.level}, Total XP: {i.total_xp}', inline=False)
      n += 1
      if n == 10:
        break 
    await ctx.send(embed=em)
    # show the leaderboard whichever way you'd like
    
    
TOKEN = os.getenv("DISCORD_TOKEN")

def start_bot(client):
    lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
    no_py = [s.replace('.py', '') for s in lst]
    startup_extensions = ["cogs." + no_py for no_py in no_py]
    try:
        for cogs in startup_extensions:
            client.load_extension(cogs)  # Startup all cogs
            print(f"Loaded {cogs}")

        print("\nAll Cogs Loaded\n===============\nLogging into Discord...")
        client.run(TOKEN) # Token do not change it here. Change it in the .env if you do not have a .env make a file and put DISCORD_TOKEN=Token 

    except Exception as e:
        print(
            f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")



start_bot(client)


