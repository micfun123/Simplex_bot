import discord
import discord
from discord.ext import commands
import json
from simpcalc import simpcalc
import asyncio
import sqlite3
import aiosqlite
from base69 import decode_base69

calculator = simpcalc.Calculate()

# Counting


async def counting(msg, guild, channel, m):
    if m.author.bot:
        return
    
    try:
        if msg.startswith("69*|"):
            #use base69
            msg = decode_base69(msg)
        else:
            #use simpcalc
            calc = simpcalc.Calculate()
            ans = await calc.calculate(msg)
            msg = int(ans)
    except:
        return    
    
    #con = sqlite3.connect("databases/counting.db")
    #cur = con.cursor()
    ###get counting channel
    #countingchannel = cur.execute("SELECT counting_channel FROM counting WHERE Guild_id = ?", (guild.id,)).fetchone()[0]
    #if countingchannel is None:
    #    return
    #if countingchannel != channel.id:
    #    return
    #else:
    #    ##get last number
    #    lastnumber = cur.execute("SELECT lastcounter FROM counting WHERE Guild_id = ?", (guild.id,)).fetchone()[0]
    #    lastuser = cur.execute("SELECT last_user FROM counting WHERE Guild_id = ?", (guild.id,)).fetchone()[0]
    #    highest = cur.execute("SELECT highest FROM counting WHERE Guild_id = ?", (guild.id,)).fetchone()[0]
    #    if lastnumber is None:
    #        cur.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (msg, guild.id))
    #        con.commit()
    #        con.close()
    #        return
    #    if msg == lastnumber + 1:
    #        if lastuser == m.author.id:
    #            await m.add_reaction("❌")
    #            em = discord.Embed(title=f"{m.author.display_name}, You ruined it!", description="Take it in turns and stop being selfish\nCount reset to zero")
    #            cur.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (0, guild.id))
    #            cur.execute("UPDATE counting SET last_user = ? WHERE Guild_id = ?", (None, guild.id))
    #            con.commit()
    #            con.close()
    #            return await channel.send(embed=em)
    #        else:
    #            
    #            cur.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (msg, guild.id))
    #            cur.execute("UPDATE counting SET last_user = ? WHERE Guild_id = ?", (m.author.id, guild.id))
    #            if msg == highest+1:
    #                cur.execute("UPDATE counting SET highest = ? WHERE Guild_id = ?", (msg, guild.id))
    #                await m.add_reaction("☑")
    #            else:
    #                await m.add_reaction("✅")
    #            con.commit()
    #            con.close()
    #            if msg == 69:
    #                await channel.send("nice")
    #            if msg == 420:
    #                await channel.send("nice")
    #            if msg == 42069:
    #                await channel.send("You have found the meaning of life.")
    #            return
    #    else:
    #        await m.add_reaction("❌")
    #        em = discord.Embed(title=f"{m.author.display_name}, You ruined it!", description=f"Count reset to zero. you were supposed to count {lastnumber + 1}")
    #        cur.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (0, guild.id))
    #        cur.execute("UPDATE counting SET last_user = ? WHERE Guild_id = ?", (None, guild.id))
    #        con.commit()
    #        con.close()
    #        return await channel.send(embed=em)
    
    async with aiosqlite.connect("./databases/counting.db") as db:
        counting_channel = await db.execute("SELECT counting_channel FROM counting WHERE Guild_id = ?", (guild.id,))
        counting_channel = await counting_channel.fetchone()
        if counting_channel is None:
            return
        if counting_channel[0] != channel.id:
            return
        else:
            last_number = await db.execute("SELECT lastcounter FROM counting WHERE Guild_id = ?", (guild.id,))
            last_number = await last_number.fetchone()
            last_user = await db.execute("SELECT last_user FROM counting WHERE Guild_id = ?", (guild.id,))
            last_user = await last_user.fetchone()
            highest = await db.execute("SELECT highest FROM counting WHERE Guild_id = ?", (guild.id,))
            highest = await highest.fetchone()
            attemps = await db.execute("SELECT attemps FROM counting WHERE Guild_id = ?", (guild.id,))
            attemps = await attemps.fetchone()
            attemps = attemps[0]
            attemps = int(attemps)
            if last_number is None:
                await db.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (msg, guild.id))
                await db.commit()
                return
            if msg == last_number[0] + 1:
                if last_user[0] == m.author.id:
                    await m.add_reaction("❌")
                    em = discord.Embed(title=f"{m.author.display_name}, You ruined it!", description="Take it in turns and stop being selfish\nCount reset to zero")
                    await db.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (0, guild.id))
                    await db.execute("UPDATE counting SET last_user = ? WHERE Guild_id = ?", (None, guild.id))
                    await db.commit()
                    async with aiosqlite.connect("./databases/user_count_stats.db") as db_user:
                        failed = await db_user.execute("SELECT failed FROM user_count_stats WHERE user_id = ? AND guild_id = ?", (m.author.id, guild.id))
                        failed = await failed.fetchone()
                        if failed is None:
                            await db_user.execute("INSERT INTO user_count_stats (user_id, guild_id, success, failed) VALUES (?, ?, ?, ?)", (m.author.id, guild.id, 0, 1))
                            await db_user.commit()
                        else:
                            failed = failed[0]
                            failed = int(failed)
                            failed += 1
                            await db_user.execute("UPDATE user_count_stats SET failed = ? WHERE user_id = ? AND guild_id = ?", (failed, m.author.id, guild.id))
                            await db_user.commit()
                    return await channel.send(embed=em)
                else:
                    await db.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (msg, guild.id))
                    await db.execute("UPDATE counting SET last_user = ? WHERE Guild_id = ?", (m.author.id, guild.id))
                    if msg == highest[0]+1:
                        await db.execute("UPDATE counting SET highest = ? WHERE Guild_id = ?", (msg, guild.id))
                        await m.add_reaction("☑")
                    else:
                        await m.add_reaction("✅")
                    await db.commit()
                    if msg == 42:
                        await channel.send("I see you found the answer to ultimate question of life, the universe, and everything")
                    if msg == 69:
                        await channel.send("nice")
                    if msg == 420:
                        await channel.send("nice")

                    async with aiosqlite.connect("./databases/user_count_stats.db") as db_user:
                        success = await db_user.execute("SELECT success FROM user_count_stats WHERE user_id = ? AND guild_id = ?", (m.author.id, guild.id))
                        success = await success.fetchone()
                        if success is None:
                            await db_user.execute("INSERT INTO user_count_stats (user_id, guild_id, success, failed) VALUES (?, ?, ?, ?)", (m.author.id, guild.id, 1, 0))
                            await db_user.commit()
                        else:
                            success = success[0]
                            success = int(success)
                            success += 1
                            await db_user.execute("UPDATE user_count_stats SET success = ? WHERE user_id = ? AND guild_id = ?", (success, m.author.id, guild.id))
                            await db_user.commit()
                    return
            else:
                await m.add_reaction("❌")
                em = discord.Embed(title=f"{m.author.display_name}, You ruined it!", description=f"Count reset to zero. you were supposed to count {last_number[0] + 1}")
                await db.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (0, guild.id))
                await db.execute("UPDATE counting SET last_user = ? WHERE Guild_id = ?", (None, guild.id))
                await db.execute("UPDATE counting SET attemps = ? WHERE Guild_id = ?", (attemps+1, guild.id))
                await db.commit()
                async with aiosqlite.connect("./databases/user_count_stats.db") as db_user:
                    failed = await db_user.execute("SELECT failed FROM user_count_stats WHERE user_id = ? AND guild_id = ?", (m.author.id, guild.id))
                    failed = await failed.fetchone()
                    if failed is None:
                        await db_user.execute("INSERT INTO user_count_stats (user_id, guild_id, success, failed) VALUES (?, ?, ?, ?)", (m.author.id, guild.id, 0, 1))
                        await db_user.commit()
                    else:
                        failed = failed[0]
                        failed = int(failed)
                        failed += 1
                        await db_user.execute("UPDATE user_count_stats SET failed = ? WHERE user_id = ? AND guild_id = ?", (failed, m.author.id, guild.id))
                        await db_user.commit()



                return await channel.send(embed=em)

        

class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="counting_serverlb", description="Shows the server leaderboard for counting")
    async def counting_serverlb(self, ctx):
        async with aiosqlite.connect("./databases/counting.db") as db:
            highestserver = await db.execute("SELECT highest, Guild_id FROM counting ORDER BY highest DESC LIMIT 10")
            highestserver = await highestserver.fetchall()
            em = discord.Embed(title="Counting Server Leaderboard", description="The top 10 servers for counting")
            num = 1
            for i in highestserver:
                guild = self.client.get_guild(i[1])
                em.add_field(name=f"{num}: {guild.name}", value=f"{i[0]}",inline=False)
                num += 1
            await ctx.respond(embed=em)


    #@commands.is_owner()
    #@commands.command()
    #async def makedbtable(self, ctx):
    #    con = sqlite3.connect("./databases/counting.db")
    #    cur = con.cursor()
    #    cur.execute("CREATE TABLE counting (guild_id INTEGER, counting_channel INTEGER, lastcounter INTEGER,highest INTEGER, last_user INTEGER,attemps INTEGER DEFAULT 0)")
    #    con.commit()
    #    for i in self.client.guilds:
    #        cur.execute("INSERT INTO counting VALUES (?, ?, ?, ?,?)", (i.id, None, 0, 0, None))
    #    con.commit()
    #    con.close()
    #    await ctx.send("Done")

    #@commands.is_owner()
    #@commands.command(name="set_user_count_stats")
    #async def set_user_count_stats(self, ctx):
    #    async with aiosqlite.connect("./databases/user_count_stats.db") as db:
    #        await db.execute("CREATE TABLE IF NOT EXISTS user_count_stats (user_id INTEGER,guild_id INTEGER, failed INTEGER DEFAULT 0, success INTEGER DEFAULT 0)")
    #        await db.commit()
    #    await ctx.send("Done")
        


    @commands.Cog.listener()
    async def on_message(self, message):

        channel = message.channel
        msg = message.content
        guild = message.guild

        await counting(msg, guild, channel, message)

    def mic(ctx):
        return ctx.author.id == 481377376475938826

    @commands.slash_command(name="counting_stats", description="Get the stats of the counting channel")
    async def counting_stats(self, ctx):
        async with aiosqlite.connect("./databases/counting.db") as db:
            counting_channel = await db.execute("SELECT counting_channel FROM counting WHERE Guild_id = ?", (ctx.guild.id,))
            counting_channel = await counting_channel.fetchone()
            if counting_channel is None:
                return await ctx.respond("There is no counting channel set up. To set one up use `.setcountchannel`")
            if counting_channel[0] is None:
                return await ctx.respond("There is no counting channel set up. To set one up use `.setcountchannel`")
            else:
                last_number = await db.execute("SELECT lastcounter FROM counting WHERE Guild_id = ?", (ctx.guild.id,))
                last_number = await last_number.fetchone()
                last_user = await db.execute("SELECT last_user FROM counting WHERE Guild_id = ?", (ctx.guild.id,))
                last_user = await last_user.fetchone()
                highest = await db.execute("SELECT highest FROM counting WHERE Guild_id = ?", (ctx.guild.id,))
                highest = await highest.fetchone()
                attemps = await db.execute("SELECT attemps FROM counting WHERE Guild_id = ?", (ctx.guild.id,))
                attemps = await attemps.fetchone()
                place = await db.execute("SELECT highest, Guild_id FROM counting ORDER BY highest DESC")
                place = await place.fetchall()
                place = place.index((highest[0], ctx.guild.id))
                embed = discord.Embed(title=f"Counting Stats for {ctx.guild.name}", description=f"Counting channel: <#{counting_channel[0]}>",color=discord.Color.green())
                embed.add_field(name="Last number", value=last_number[0])
                embed.add_field(name="Highest number", value=highest[0])
                embed.add_field(name="Last user", value=f"<@{last_user[0]}>")
                embed.add_field(name="Attempts", value=attemps[0])
                embed.add_field(name="Place in server leaderboard", value=place+1)
                await ctx.respond(embed=embed)


    @commands.is_owner()
    @commands.has_permissions(administrator=True)
    async def set_num(self,ctx,nums):
        con = sqlite3.connect("./databases/counting.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM counting WHERE guild_id = ?", (ctx.guild.id,))
        data = cur.fetchone()
        num = int(nums)
        cur.execute("UPDATE counting SET lastcounter = ? WHERE guild_id = ?", (nums, ctx.guild.id))
        con.commit()
        con.close()
        await ctx.send(f"Numb set to {nums}")
            
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcountchannel(self, ctx, channel:discord.TextChannel):
        con = sqlite3.connect("./databases/counting.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM counting WHERE guild_id = ?", (ctx.guild.id,))
        data = cur.fetchone()
        if data is None:
            cur.execute("INSERT INTO counting VALUES (?, ?, ?, ?, ?,?)", (ctx.guild.id, channel.id, 0, 0, None, 0))
            con.commit()
            con.close()
            await ctx.send(f"Counting channel set to {channel.mention}")
        else:
            cur.execute("UPDATE counting SET counting_channel = ? WHERE guild_id = ?", (channel.id, ctx.guild.id))
            con.commit()
            con.close()
            await ctx.send(f"Counting channel set to {channel.mention}")
            
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def countingoff(self, ctx):
        con = sqlite3.connect("./databases/counting.db")
        cur = con.cursor()
        cur.execute("UPDATE counting SET counting_channel = ? WHERE guild_id = ?", (None, ctx.guild.id))
        con.commit()
        con.close()
        await ctx.send(f"Counting channel turned off")
    
            
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        con = sqlite3.connect("./databases/counting.db")
        cur = con.cursor()
        data =  cur.execute("SELECT * FROM counting WHERE guild_id = ?", (guild.id,)).fetchall()
        if not data:
            cur.execute("INSERT INTO counting VALUES (?, ?, ?, ?)", (guild.id, None, None, 0))
            con.commit()
        con.close()

    @commands.slash_command(name="user_counting_stats", description="Get the stats for the counting user")
    async def user_counting_stats(self, ctx, user:discord.User=None):
        if user is None:
            user = ctx.author
        
        async with aiosqlite.connect("./databases/user_count_stats.db") as db_user:
            person = await db_user.execute("SELECT * FROM user_count_stats WHERE user_id = ? AND guild_id = ?", (user.id, ctx.guild.id))
            person = await person.fetchone()
            if person is None:
                await ctx.respond("User has not counted yet on this server")
            
            else:
                username = await self.client.fetch_user(person[0])
                guild = await self.client.fetch_guild(person[1])
                username = username.name
                guild = guild.name
                embed = discord.Embed(title=f"Counting stats for {username} in {guild}", color=discord.Color.green())
                faileds = person[2]
                success = person[3]
                embed.add_field(name="Servers Success Counts", value=success)
                embed.add_field(name="Servers Failed Counts", value=faileds)
                accuracy = success/(success+faileds)
                embed.add_field(name="Accuracy", value=f"{str(round(accuracy*100, 2))}%")

                await ctx.respond(embed=embed)
            
            #users total stats
            data = await db_user.execute("SELECT * FROM user_count_stats WHERE user_id = ?", (user.id,))
            data = await data.fetchall()
            if data is None:
                await ctx.respond("User has not counted yet")
            else:
                success = 0
                failed = 0
                for i in data:
                    success += i[3]
                    failed += i[2]
                embed = discord.Embed(title=f"Counting stats for {username} across all servers", color=discord.Color.green())
                embed.add_field(name="Global Success Counts", value=success)
                embed.add_field(name="Global Failed counts", value=failed)
                accuracy = success/(success+failed)
                embed.add_field(name="Accuracy", value=f"{str(round(accuracy*100, 2))}%")
                await ctx.respond(embed=embed)

    #@commands.is_owner()
    #@commands.command()
    #async def countannounce(self, ctx):
    #    with open("./databases/db.json", "rb") as f:
    #        data = json.load(f)
    #    serverssent = 0
    #    #go throught list 
    #    for i in data:
    #        try:
    #            channel = await self.client.fetch_channel(i["counting_channel"])
    #            await channel.send(f"Couning has been rewriten to be more relable. Please use the new command to set the counting channel. `.setcountchannel <channel>`. This will set the channel to 0 to change the number use `.set_num <number>`. IF you find any bugs please dm the bot\n Now with a highscore marker")
    #            serverssent += 1
    #        except Exception as e:
    #            print(e)
    #            ctx.send(f"Error in {i}")
    #            pass
    #    await ctx.send(f"Sent to {serverssent} servers")

def setup(client):
    client.add_cog(Counting(client))
