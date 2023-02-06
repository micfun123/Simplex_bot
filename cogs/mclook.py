import json
import aiohttp
import asyncio
import socket
from functools import partial
import discord
from discord.ext import commands
from time import sleep
import requests

from flask import jsonify




class Minecraft(commands.Cog):
    """All the info needed on a Minecraft server"""
    def __init__(self, bot):
        
        self.bot = bot
        self.ses = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.ses.close())

   

    @commands.command(name="mcping", aliases=["mcstatus"], help= "Gets the status of a Minecraft server, Ping and player count")
    async def mc_ping(self, ctx, server: str):
        async with ctx.typing():
            url = f"https://api.mcsrvstat.us/2/{server}"
            response = requests.get(url)
            resp = response.json()
            try:
                players = resp["players"]["online"]
                playerlist = resp["players"]["list"]
                playersmax = resp["players"]["max"]
                MOTD = resp["motd"]["clean"][0]
                online = resp["online"]
                version = resp["version"]
                embed=discord.Embed(title=f"{server} is online" , description=MOTD, colour=0x00FF00)
                try:
                    mods = resp["mods"]
                    embed.add_field(name="Is modded: ", value= "True", inline=True)
                except:
                    embed.add_field(name="Is modded: ", value= "False", inline=True)
                embed.add_field(name="Players Online: ", value=f"{players} / {playersmax}", inline=True)
                embed.add_field(name="Version: ", value=version, inline=True)
                if players > 20:
                    embed.add_field(name="Player list: ", value="Too many players to display", inline=False)
                elif players > 0:
                    pass
                else:
                    for player in playerlist:
                        embed.add_field(name="Player list: ", value=player, inline=False)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title=f"{server} is offline",color=0xFF0000)
                await ctx.send(embed=embed)

    @commands.slash_command(name="mcping", description= "Gets the status of a Minecraft server, Ping and player count")
    async def mc_ping__slash(self, ctx, server: str):
            url = f"https://api.mcsrvstat.us/2/{server}"
            response = requests.get(url)
            resp = response.json()
            try:
                players = resp["players"]["online"]
                playerlist = resp["players"]["list"]
                playersmax = resp["players"]["max"]
                MOTD = resp["motd"]["clean"][0]
                online = resp["online"]
                version = resp["version"]
                embed=discord.Embed(title=f"{server} is online" , description=MOTD, colour=0x00FF00)
                try:
                    mods = resp["mods"]
                    embed.add_field(name="Is modded: ", value= "True", inline=True)
                except:
                    embed.add_field(name="Is modded: ", value= "False", inline=True)
                embed.add_field(name="Players Online: ", value=f"{players} / {playersmax}", inline=True)
                embed.add_field(name="Version: ", value=version, inline=True)
                if players > 20:
                    embed.add_field(name="Player list: ", value="Too many players to display", inline=False)
                elif players > 0:
                    pass
                else:
                    for player in playerlist:
                        embed.add_field(name="Player list: ", value=player, inline=False)
                await ctx.respond(embed=embed)
            except:
                embed=discord.Embed(title=f"{server} is offline",color=0xFF0000)
                await ctx.respond(embed=embed)

        

    @commands.command(name="mcskin", help="Gets a skin of a minecraft player")
    async def mcskin(self, ctx, *, player: str):
        async with ctx.typing():
            resp = await self.ses.get(f"https://api.mojang.com/users/profiles/minecraft/{player}")
            jj = await resp.json()
            uuid = jj.get("id")
            skin_url = f"https://mc-heads.net/body/{uuid}/right"
            download_url = f"https://mc-heads.net/download/{uuid}"
            embed = discord.Embed(color=discord.Color.green())
            embed.set_image(url=skin_url)
            await ctx.send(embed=embed)
            embed.set_image(url=download_url)
            await ctx.send(embed=embed)

    @commands.slash_command(name="mcskin",description="Gets a skin of a minecraft player")
    async def mcskin_(self, ctx, *, player: str):
        async with ctx.typing():
            resp = await self.ses.get(f"https://api.mojang.com/users/profiles/minecraft/{player}")
            jj = await resp.json()
            uuid = jj.get("id")
            skin_url = f"https://mc-heads.net/body/{uuid}/right"
            download_url = f"https://mc-heads.net/download/{uuid}"
            embed = discord.Embed(color=discord.Color.green())
            embed.set_image(url=skin_url)
            await ctx.respond(embed=embed)
            embed.set_image(url=download_url)
            await ctx.respond(embed=embed)


    @commands.command(name= "mchead",help="Gets a skin of a minecraft player")
    async def mchead(self, ctx, *, player: str):
        async with ctx.typing():
            resp = await self.ses.get(f"https://api.mojang.com/users/profiles/minecraft/{player}")
            jj = await resp.json()
            uuid = jj.get("id")
            head_url = f"https://mc-heads.net/avatar/{uuid}" 
            side_head_url = f"https://mc-heads.net/head/{uuid}"
            embed = discord.Embed(color=discord.Color.green())
            embed.set_image(url=head_url)
            await ctx.send(embed=embed)
            embed.set_image(url=side_head_url)
            await ctx.send(embed=embed)


    @commands.slash_command(name= "mchead",description="Gets a skin of a minecraft player")
    async def mchead_(self, ctx, *, player: str):
        async with ctx.typing():
            resp = await self.ses.get(f"https://api.mojang.com/users/profiles/minecraft/{player}")
            jj = await resp.json()
            uuid = jj.get("id")
            head_url = f"https://mc-heads.net/avatar/{uuid}" 
            side_head_url = f"https://mc-heads.net/head/{uuid}"
            embed = discord.Embed(color=discord.Color.green())
            embed.set_image(url=head_url)
            await ctx.respond(embed=embed)
            embed.set_image(url=side_head_url)
            await ctx.respond(embed=embed)

            
def setup(bot):
    bot.add_cog(Minecraft(bot))