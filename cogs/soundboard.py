
import discord
from discord.ext import commands 
from discord.commands import slash_command



class soundboard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sounds = {
            "airhorn": "airhorn.mp3",
            "sad_trombone": "sad_trombone.mp3"
        }


    #slash command with options
    @slash_command(name="soundboard", description="Play a sound from the soundboard")
    async def soundboard(self, ctx, *, sound: discord.Option(str, "The sound to play", required=True, choices=["airhorn", "sad_trombone"])):
        if ctx.author.voice is None:
            await ctx.respond("You are not in a voice channel")
            return
        else:
            vc = await ctx.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(f"soundboard/{self.sounds[sound]}"))
            while vc.is_playing():
                pass
            await vc.disconnect()
            



        
def setup(client):
    client.add_cog(soundboard(client))