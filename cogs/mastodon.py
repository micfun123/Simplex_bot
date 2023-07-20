from discord.ext import commands, tasks
import aiosqlite
import discord
from mastodon import Mastodon
import asyncio
from datetime import datetime,time
import requests
import os
from dotenv import load_dotenv
import re

load_dotenv()




class mastodon(commands.Cog):
    def __init__(self, client): 
        self.client = client
        #start the rss looper task
        self.mastodon_looper.start()

    @commands.slash_command(name="mastodon_manage", description="Manage the mastodon feeds")
    @commands.has_permissions(manage_channels=True)
    async def mastodon_manage(self, ctx, channel:discord.TextChannel, username:str,action:str):
        action = action.lower()
        if action == "add":
            async with aiosqlite.connect("databases/mastodon.db") as db:
                await db.execute("INSERT INTO mastodon (channel_id, guild_id, username, last_posted) VALUES (?, ?, ?, ?)", (channel.id, channel.guild.id, username, "0"))
                await db.commit()
            await ctx.respond("Done")
        elif action == "remove":
            async with aiosqlite.connect("databases/mastodon.db") as db:
                await db.execute("DELETE FROM mastodon WHERE channel_id = ? AND guild_id = ? AND username = ?", (channel.id, channel.guild.id, username))
                await db.commit()
            await ctx.respond("Done")
        elif action == "list":
            async with aiosqlite.connect("databases/mastodon.db") as db:
                cursor = await db.execute("SELECT * FROM mastodon WHERE guild_id = ?", (channel.guild.id,))
                data = await cursor.fetchall()
                embed = discord.Embed(title="Mastodon feeds", description="Here are all the mastodon feeds for this server", color=0x00ff00)
                for row in data:
                    embed.add_field(name=f"{row[2]}", value=f"Channel: <#{row[0]}>\nUsername: {row[2]}\nLast posted: {row[3]}", inline=False)
                await ctx.respond(embed=embed)

        else:
            await ctx.respond("That is not a valid action, valid actions are: add, remove,list")
        await ctx.respond("Thank you for using simplex voting and donating helps keep this bot free.", ephemeral=True)



    #mastodon loop
    @tasks.loop(seconds=20)
    async def mastodon_looper(self):
        async with aiosqlite.connect("databases/mastodon.db") as db:
            cursor = await db.execute("SELECT * FROM mastodon")
            data = await cursor.fetchall()
            for row in data:
                try:
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
                        link = users_posts[0]["url"]
                        time = users_posts[0]["created_at"]
                        if link == None:
                            message = f"**{username}** just posted on mastodon\n{link} \n {time}"
                            await tosend.send(message)
                        await db.execute("UPDATE mastodon SET last_posted = ? WHERE username = ?", (last_post, username))
                        await db.commit()
                    else:
                        pass
                except:
                    pass
            


    #wait intill the loop is ready
    @mastodon_looper.before_loop
    async def before_mastodon_looper(self):
        await self.client.wait_until_ready()
        print("Mastodon loop is ready")

        









def setup(client):
    client.add_cog(mastodon(client))
    
