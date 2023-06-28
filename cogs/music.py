import discord
from discord.ext import commands
import youtube_dl

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.queue = []

    def cog_unload(self):
        if self.voice and self.voice.is_connected():
            self.queue.clear()
            self.voice.stop()
            self.voice.disconnect()

    @commands.command()
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        if self.voice and self.voice.is_connected():
            await self.voice.move_to(ctx.message.author.voice.channel)
        else:
            self.voice = await ctx.message.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if self.voice and self.voice.is_connected():
            self.queue.clear()
            await self.voice.stop()
            await self.voice.disconnect()
        else:
            await ctx.send("I am not connected to a voice channel.")

    @commands.command()
    async def play(self, ctx, url):
        if not self.voice or not self.voice.is_connected():
            await ctx.send("I am not connected to a voice channel. Use the `join` command first.")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            self.queue.append(url2)

        if not self.voice.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if not self.queue:
            return

        url = self.queue.pop(0)
        self.voice.play(discord.FFmpegPCMAudio(url), after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))

    @commands.command()
    async def pause(self, ctx):
        if self.voice and self.voice.is_playing():
            self.voice.pause()

    @commands.command()
    async def resume(self, ctx):
        if self.voice and self.voice.is_paused():
            self.voice.resume()

    @commands.command()
    async def skip(self, ctx):
        if self.voice and self.voice.is_playing():
            self.voice.stop()
            await self.play_next(ctx)

    @commands.command()
    async def clear(self, ctx):
        self.queue.clear()

def setup(bot):
    bot.add_cog(Music(bot))
