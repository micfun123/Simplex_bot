import discord
from discord.ext import commands
import aiohttp
import aiofiles
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# --- A Note on APIs ---
# The original script used two APIs:
# 1. https://some-random-api.com/ - This API is currently active.
# 2. https://michaelapi.herokuapp.com/ - This API is currently offline and has been for some time.
#
# All commands relying on the defunct 'michaelapi' have been removed from this rewritten script
# to ensure functionality. These included 'wanted', 'trash', and 'ghost'.

class Filter(commands.Cog):
    """
    Applies fun image filter and overlay effects to user profile pictures.
    """
    def __init__(self, client: commands.Bot):
        self.client = client
        self.session = aiohttp.ClientSession()
        self.temp_storage_path = "./tempstorage"
        # Ensure the temporary storage directory exists
        if not os.path.exists(self.temp_storage_path):
            os.makedirs(self.temp_storage_path)

    def cog_unload(self):
        # Gracefully close the aiohttp session when the cog is unloaded.
        self.client.loop.create_task(self.session.close())

    async def _create_image(self, ctx: commands.Context, endpoint: str, member: discord.Member):
        """
        A generalized function to handle API requests, file creation, and sending.

        Args:
            ctx: The command context.
            endpoint: The specific API endpoint for the desired filter (e.g., 'jail', 'glass').
            member: The Discord member whose avatar will be used.
        """
        if member is None:
            member = ctx.author

        # Use display_avatar to get server-specific avatars if they exist
        avatar_url = str(member.display_avatar.url)
        api_url = f"https://some-random-api.com/canvas/{endpoint}"
        params = {'avatar': avatar_url}
        temp_file_path = os.path.join(self.temp_storage_path, f"overlay_{ctx.author.id}_{ctx.command.name}.png")

        try:
            async with self.session.get(api_url, params=params) as resp:
                if resp.status != 200:
                    logging.error(f"API Error: {endpoint} endpoint returned status {resp.status}")
                    await ctx.send(f"😥 The image API isn't working right now. Please try again later. (Status: {resp.status})")
                    return

                # Read the image data
                data = await resp.read()

                # Write data to a temporary file asynchronously
                async with aiofiles.open(temp_file_path, mode="wb") as f:
                    await f.write(data)

            # Send the file to Discord
            await ctx.send(file=discord.File(temp_file_path))

        except aiohttp.ClientError as e:
            logging.error(f"Network error during API call: {e}")
            await ctx.send("Network error. Could not connect to the image API.")
        except IOError as e:
            logging.error(f"File write error: {e}")
            await ctx.send("Error: Could not save the image file on the server.")
        finally:
            # IMPORTANT: Ensure the temporary file is always deleted
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


    # --- Overlay Commands ---

    @commands.command(help="Puts a jail overlay on an avatar.", usage="[@member]")
    async def jail(self, ctx, member: discord.Member = None):
        await self._create_image(ctx, "jail", member)

    @commands.command(help="Puts a 'comrade' overlay on an avatar.", usage="[@member]")
    async def comrade(self, ctx, member: discord.Member = None):
        await self._create_image(ctx, "comrade", member)

    @commands.command(help="Puts a 'wasted' (GTA) overlay on an avatar.", usage="[@member]")
    async def wasted(self, ctx, member: discord.Member = None):
        await self._create_image(ctx, "wasted", member)

    @commands.command(help="Puts a 'passed' (GTA) overlay on an avatar.", usage="[@member]")
    async def passed(self, ctx, member: discord.Member = None):
        await self._create_image(ctx, "passed", member)

    @commands.command(help="Creates a 'triggered' GIF from an avatar.", usage="[@member]")
    async def triggered(self, ctx, member: discord.Member = None):
        # Note: 'triggered' endpoint creates a GIF, so we adjust the file path
        await self._create_image(ctx, "triggered", member)


    # --- Filter Commands ---

    @commands.command(name="greyscale", help="Applies a greyscale filter to an avatar.", usage="[@member]")
    async def greyscale_cmd(self, ctx, member: discord.Member = None):
        await self._create_image(ctx, "greyscale", member)

    @commands.command(help="Applies a sepia filter to an avatar.", usage="[@member]")
    async def sepia(self, ctx, member: discord.Member = None):
        await self._create_image(ctx, "sepia", member)

    @commands.command(name="blurple", help="Applies a blurple filter to an avatar.", usage="[@member]")
    async def blurple_cmd(self, ctx, member: discord.Member = None):
        await self._create_image(ctx, "blurple2", member) # 'blurple2' is the new version

    @commands.command(name="blurpleold", help="Applies the old blurple filter to an avatar.", usage="[@member]")
    async def blurpleold_cmd(self, ctx, member: discord.Member = None):
        await self._create_image(ctx, "blurple", member) # 'blurple' is the old version

    @commands.command(help="Pixelates an avatar.", usage="[@member]")
    async def pixelate(self, ctx, member: discord.Member = None):
        await self._create_image(ctx, "pixelate", member)


def setup(client: commands.Bot):
    """The setup function to add the cog to the bot."""
    client.add_cog(Filter(client))