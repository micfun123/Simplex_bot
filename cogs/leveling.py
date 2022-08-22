import discord
import json
from discord.ext import commands
from discordLevelingSystem import DiscordLevelingSystem, LevelUpAnnouncement
from easy_pil import Editor, Canvas, Font, load_image_async, Text
import os
from tools import log, mic
import random
LevelUPresponses = [f'Congrats {LevelUpAnnouncement.Member.mention}! You are now level {LevelUpAnnouncement.LEVEL} 😎',
                 f'Well done {LevelUpAnnouncement.Member.mention}! You are now level {LevelUpAnnouncement.LEVEL} have a 🥇',
                 f'{LevelUpAnnouncement.Member.mention} you are now level {LevelUpAnnouncement.LEVEL}! Keep going you are amazing!',
                 f"You are {LevelUpAnnouncement.Member.mention} and now you're at level {LevelUpAnnouncement.LEVEL}!",
                 f'Wow you are now level {LevelUpAnnouncement.LEVEL}! good job {LevelUpAnnouncement.Member.mention}'
                 ]


lvlembed = discord.Embed(color=discord.Color.green())
lvlembed.set_author(name=LevelUpAnnouncement.Member.name)
lvlembed.description = random.choice(LevelUPresponses)

announcement = LevelUpAnnouncement(lvlembed)

lvl = DiscordLevelingSystem(rate=1, per=60,level_up_announcement=announcement)
lvl.connect_to_database_file(r'databases/DiscordLevelingSystem.db')


async def level_on(guild):
    guild_id = str(guild)
    with open("databases/leveling.json") as f:
        data = json.load(f)
    if guild_id not in data:
        data[guild_id] = True
        with open("databases/leveling.json", 'w') as f:
            json.dump(data, f, indent=4)
        return True
    if data[guild_id]:
        return True 
    else:
        return False

async def lb(self, ctx):
    data = await lvl.each_member_data(ctx.guild, sort_by='rank')
    em = discord.Embed(title="Leaderboard")
    n = 0
    for i in data:
      em.add_field(name=f'{i.rank}: {i.name}', value=f'Level: {i.level}, Total XP: {i.total_xp}', inline=False)
      n += 1
      if n == 10:
        break 
    await ctx.send(embed=em)


async def biglb(self, ctx):
    data = await lvl.each_member_data(ctx.guild, sort_by='rank')
    em = discord.Embed(title="Leaderboard")
    n = 0
    for i in data:
      em.add_field(name=f'{i.rank}: {i.name}', value=f'Level: {i.level}, Total XP: {i.total_xp}', inline=False)
      n += 1
      if n == 50:
        break 
    await ctx.send(embed=em)



class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toggle_leveling(self, ctx):

        with open("databases/leveling.json") as f:
            data = json.load(f)
        if str(ctx.guild.id) not in data:
            data[str(ctx.guild.id)] = True
            await ctx.send("Leveling On")
            
        if data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)] = False
            await ctx.send("Leveling Off")

        else:
            data[str(ctx.guild.id)] = True
            await ctx.send("Leveling On")

        with open("databases/leveling.json", 'w') as f:
            json.dump(data, f, indent=4)

        if data[str(ctx.guild.id)]:
            return True

        return False


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await lvl.reset_member(member)

    @commands.command(aliases=['lvl'], help="This command shows your rank for the leveling system.", description="Shows your rank image")
    async def rank(self, ctx, member:discord.Member=None):
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
        profile_image = await load_image_async(str(member.avatar.url))
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
        background.save(f"tempstorage/rank{member.id}.png")
        await ctx.send(file=discord.File(f"tempstorage/rank{member.id}.png"))
        os.remove(f"tempstorage/rank{member.id}.png")


    @commands.command(aliases=['lb'], help="This command shows the leaderboard for this server.\nIt is sorted by most highest level to lowest.")
    async def leaderboard(self, ctx):
        await lb(self, ctx)

    @commands.command(aliases=['biglb'], help="This command shows the leaderboard for this server.\nIt is sorted by most highest level to lowest.")
    async def bigleaderboard(self, ctx):
        await biglb(self, ctx)

    @commands.command(aliases=['fulllb'], help="This command shows the leaderboard for this server.\nIt is sorted by most highest level to lowest.")
    async def fullleaderboard(self, ctx):
        data = await lvl.each_member_data(ctx.guild, sort_by='rank')
        em = discord.Embed(title="Leaderboard")
        n = 0
        for i in data:
            em.add_field(name=f'{i.rank}: {i.name}', value=f'Level: {i.level}, Total XP: {i.total_xp}', inline=False)
            n += 1
            if n == 20:
                await ctx.send(embed=em)
                n = 0
                return
        await ctx.send(embed=em)


    #reset users xp to 0
    @commands.command(aliases=['reset'], help="This command resets the xp of a user to 0.")
    @commands.has_permissions(administrator=True)
    async def resetxp(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        await ctx.send(f"{member.mention}'s xp has been reset to 0.")
        await lvl.reset_member(member)

    #give xp to a user
    @commands.command(help="This command gives xp to a user.")
    @commands.has_permissions(administrator=True)
    async def givexp(self, ctx, member:discord.Member, xp:int):
        await ctx.send(f"{member.mention} has received {xp} xp.")
        await lvl.add_xp(member, xp)

    #give xp to all user
    @commands.command(help="This command gives xp to all users.")
    @commands.has_permissions(administrator=True)
    async def givexpall(self, ctx, xp:int):
        for i in ctx.guild.members:
            await lvl.add_xp(i, xp)
        await ctx.send(f"All users have received {xp} xp.")
        
        
    #reset all users on server
    @commands.command(aliases=['resetall'], help="This command resets all users xp to 0.")
    @commands.has_permissions(administrator=True)
    async def resetallxp(self, ctx):
        await ctx.send("All users xp will be reset 0. This may take a hot second")
        for member in ctx.guild.members:
            await lvl.reset_member(member)
        await ctx.send("All users xp has been reset to 0.")
        

    @commands.Cog.listener()
    async def on_message(self, message):
            level_toggle =  await level_on(message.guild.id)
            if level_toggle:
                await lvl.award_xp(amount=15, message=message)
    

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await lvl.reset_member(member)

    @commands.command(help="Checks and recalculates the ranks from xp amounts")
    @commands.is_owner()
    async def recalculateranks(self, ctx, *, member:discord.Member=None):
        await ctx.send("Recalculating ranks...")
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
        targetxp = await lvl.get_data_for(member)
        temp = 0 
        xpamount = targetxp.total_xp
        print(xpamount)
        for level, xp in LEVELS_AND_XP.items():
            if(temp + xp >= xpamount):
                await ctx.send(f"{member.mention} is level {level}")
                break
            temp += xp
        await lvl.set_level(member, int(level))
        
        

        


def setup(client):
    client.add_cog(Leveling(client))