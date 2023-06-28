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
            self.bot.loop.create_task(self.voice.disconnect())

    async def check_voice_channel(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return False

        return True

    async def join_voice_channel(self, ctx):
        if self.voice and self.voice.is_connected():
            await self.voice.move_to(ctx.message.author.voice.channel)
        else:
            self.voice = await ctx.message.author.voice.channel.connect()

    @commands.command()
    async def join(self, ctx):
        if not await self.check_voice_channel(ctx):
            return

        await self.join_voice_channel(ctx)
        await ctx.send("Joined the voice channel.")

    @commands.command()
    async def leave(self, ctx):
        if not self.voice or not self.voice.is_connected():
            await ctx.send("I am not connected to a voice channel.")
            return

        self.queue.clear()
        await self.voice.disconnect()
        self.voice = None
        await ctx.send("Left the voice channel.")

    @commands.command()
    async def play(self, ctx, url):
        if not await self.check_voice_channel(ctx):
            return

        if not self.voice or not self.voice.is_connected():
            await self.join_voice_channel(ctx)

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
            await ctx.send("Playback paused.")

    @commands.command()
    async def resume(self, ctx):
        if self.voice and self.voice.is_paused():
            self.voice.resume()
            await ctx.send("Playback resumed.")

    @commands.command()
    async def skip(self, ctx):
        if self.voice and self.voice.is_playing():
            self.voice.stop()
            await self.play_next(ctx)
            await ctx.send("Skipped to the next song.")

    @commands.command()
    async def clear(self, ctx):
        self.queue.clear()
        await ctx.send("Queue cleared.")

def setup(bot):
    bot.add_cog(Music(bot))
