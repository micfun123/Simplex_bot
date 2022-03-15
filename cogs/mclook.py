import aiohttp
import asyncio
import concurrent.futures
import socket
from functools import partial
from mcstatus import MinecraftServer
from pyraklib.protocol.UNCONNECTED_PING import UNCONNECTED_PING
from pyraklib.protocol.UNCONNECTED_PONG import UNCONNECTED_PONG
import discord
from discord.ext import commands
from time import sleep




class Minecraft(commands.Cog):
    """All the info needed on a Minecraft server"""
    def __init__(self, bot):
        
        self.bot = bot
        self.ses = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.ses.close())

    def vanilla_pe_ping(self, ip, port):
        ping = UNCONNECTED_PING()
        ping.pingID = 4201
        ping.encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(0)
        try:
            s.sendto(ping.buffer, (socket.gethostbyname(ip), port))
            sleep(1.5)
            recv_data = s.recvfrom(2048)
        except BlockingIOError:
            return False, 0
        except socket.gaierror:
            return False, 0
        pong = UNCONNECTED_PONG()
        pong.buffer = recv_data[0]
        pong.decode()
        s_info = str(pong.serverName)[2:-2].split(";")
        p_count = s_info[4]
        return True, p_count

    def standard_je_ping(self, combined_server):
        try:
            status = MinecraftServer.lookup(combined_server).status()
        except Exception:
            return False, 0, None

        return True, status.players.online, status.latency

    async def unified_mc_ping(self, server_str, _port=None, _ver=None):
        if ":" in server_str and _port is None:
            split = server_str.split(":")
            ip = split[0]
            port = int(split[1])
        else:
            ip = server_str
            port = _port

        if port is None:
            str_port = ""
        else:
            str_port = f":{port}"

        if _ver == "je":
            # ONLY JE servers
            standard_je_ping_partial = partial(self.standard_je_ping, f"{ip}{str_port}")
            with concurrent.futures.ThreadPoolExecutor() as pool:
                s_je_online, s_je_player_count, s_je_latency = await self.bot.loop.run_in_executor(pool,
                                                                                              standard_je_ping_partial)
            if s_je_online:
                ps_online = (await self.unified_mc_ping(ip, port, "api")).get("players")
                return {"online": True, "player_count": s_je_player_count, "players": ps_online, "ping": s_je_latency, "version": "Java Edition"}

            return {"online": False, "player_count": 0, "players": None, "ping": None, "version": None}
        elif _ver == "api":
            # JE & PocketMine
            resp = await self.ses.get(f"https://api.mcsrvstat.us/2/{ip}{str_port}")
            jj = await resp.json()
            if jj.get("online"):
                return {"online": True, "player_count": jj.get("players", {}).get("online", 0), "players": jj.get("players", {}).get("list"), "ping": None,
                        "version": jj.get("software")}
            return {"online": False, "player_count": 0, "players": None, "ping": None, "version": None}
        elif _ver == "be":
            # Vanilla MCPE / Bedrock Edition (USES RAKNET)
            vanilla_pe_ping_partial = partial(self.vanilla_pe_ping, ip, (19132 if port is None else port))
            with concurrent.futures.ThreadPoolExecutor() as pool:
                pe_online, pe_p_count = await self.bot.loop.run_in_executor(pool, vanilla_pe_ping_partial)
            if pe_online:
                return {"online": True, "player_count": pe_p_count, "players": None, "ping": None, "version": "Vanilla Bedrock Edition"}
            return {"online": False, "player_count": 0, "players": None, "ping": None, "version": None}
        else:
            tasks = [
                self.bot.loop.create_task(self.unified_mc_ping(ip, port, "je")),
                self.bot.loop.create_task(self.unified_mc_ping(ip, port, "api")),
                self.bot.loop.create_task(self.unified_mc_ping(ip, port, "be"))
            ]

            done = 0

            while done < 3:
                for task in tasks:
                    if task.done():
                        result = task.result()

                        if result.get("online") is True:
                            return result

                        done += 1

                await asyncio.sleep(.05)

            return {"online": False, "player_count": 0, "players": None, "ping": None, "version": None}

    @commands.command(name="mcping", aliases=["mcstatus"], help= "Gets the status of a Minecraft server, Ping and player count")
    @commands.guild_only()
    async def mc_ping(self, ctx, server: str, port: int = None):
        async with ctx.typing():
            status = await self.unified_mc_ping(server, port)

        title = f"<:a:730460448339525744> {server}{(':' + str(port)) if port is not None else ''} is online."

        if status.get("online") is False:
            embed = discord.Embed(color=discord.Color.green(),
                                  title=f"<:b:730460448197050489> {server}{(':' + str(port)) if port is not None else ''} is offline.")
            await ctx.send(embed=embed)
            return

        ps_list = status.get("players")

        embed = discord.Embed(color=discord.Color.green(), title=title)

        ping = status.get("ping", "Not Available")

        if ps_list is None:
            embed.add_field(name="Players Online", value=status.get("player_count"))
            embed.add_field(name="Latency/Ping", value=ping if ping != "None" and ping is not None else "Not Available")
            embed.add_field(name="Version", value=status.get('version'), inline=False)
        else:
            embed.add_field(name="Latency/Ping", value=ping if ping != "None" and ping is not None else "Not Available")
            embed.add_field(name="Version", value=status.get('version'))
            ps_list_cut = ps_list[:20]
            if len(ps_list_cut) == 0:
                ps_list_cut.append("No players online.")

            if len(ps_list_cut) < len(ps_list):
                ps_list_cut.append(f"and {len(ps_list)-len(ps_list_cut)} others...")

            embed.add_field(name=f"Players Online ({len(ps_list)} Total)",
                            value=discord.utils.escape_markdown(', '.join(ps_list_cut)),
                            inline=False)

        await ctx.send(embed=embed)

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


    @commands.command(help="Gets a skin of a minecraft player")
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

            
def setup(bot):
    bot.add_cog(Minecraft(bot))