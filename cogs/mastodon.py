from discord.ext import commands, tasks
import aiosqlite
import discord
from mastodon import Mastodon
import asyncio
from datetime import datetime,time
import requests
import os
from dotenv import load_dotenv

load_dotenv()




class mastodon(commands.Cog):
    def __init__(self, client): 
        self.client = client
        #start the rss looper task
        self.mastodon_looper.start()



    @commands.command()
    @commands.is_owner()
    async def make_mastodon_file(self, ctx):
        async with aiosqlite.connect("databases/mastodon.db") as db:
            await db.execute("CREATE TABLE IF NOT EXISTS mastodon (channel_id int, guild_id int, username text,last_posted text)")
            await db.commit()
        await ctx.respond("Done")


    @commands.slash_command(name="mastodon_manage", description="Manage the mastodon feeds")
    @commands.has_permissions(manage_channels=True)
    async def mastodon_manage(self, ctx, channel:discord.TextChannel, username:str):
        async with aiosqlite.connect("databases/mastodon.db") as db:
            await db.execute("INSERT INTO mastodon (channel_id, guild_id, username, last_posted) VALUES (?, ?, ?, ?)", (channel.id, channel.guild.id, username, "0"))
            await db.commit()
        await ctx.respond("Done")



    #mastodon loop
    @tasks.loop(seconds=20)
    async def mastodon_looper(self):
        async with aiosqlite.connect("databases/mastodon.db") as db:
            cursor = await db.execute("SELECT * FROM mastodon")
            data = await cursor.fetchall()
            for row in data:
                guild = self.client.get_guild(row[1])
                username = row[2]
                last_posted = row[3]
                #get the last post
                client_id_temp = os.getenv("MASTODON_CLIENT_ID")
                client_secret_temp = os.getenv("MASTODON_CLIENT_SECRET")
                access_token_temp = os.getenv("MASTODON_ACCESS_TOKEN")
                mastodon_client = Mastodon(client_id=client_id_temp, client_secret=client_secret_temp, access_token=access_token_temp,api_base_url="https://mastodon.social")
                userid = mastodon_client.account_search(username)[0]["id"]
                users_posts = mastodon_client.account_statuses(userid)
                last_post = users_posts[0]["id"]
                #check if the last post is the same as the last posted
                if int(last_post) != int(last_posted):
                    print(last_post)
                    #send the post
                    tosend = await self.client.fetch_channel(int(row[0]))
                    content = users_posts[0]["content"]
                    #just get the raw text remove the html
                    content = content.replace("<p>", "")
                    content = content.replace("</p>", "")
                    content = content.replace("<br />", "\n")
                    embed = discord.Embed(title=f"New post from {username}", description=content, color=discord.Color.random())
                    embed.set_footer(text="Powered by Mastodon")
                    await tosend.send(embed=embed)
                    await db.execute("UPDATE mastodon SET last_posted = ? WHERE channel_id = ?", (last_post, row[0]))
                    await db.commit()
                else:
                    pass
                await asyncio.sleep(5)
            await db.commit()


    #wait intill the loop is ready
    @mastodon_looper.before_loop
    async def before_mastodon_looper(self):
        await self.client.wait_until_ready()
        print("Mastodon loop is ready")

        









def setup(client):
    client.add_cog(mastodon(client))
    
