import aiofiles
import discord
from discord.ext import commands
import aiohttp
import os


class filter(commands.Cog):
    def __init__(self, client): 
        self.client = client 

    
    @commands.command(help="This will put a jail effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def jail(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/jail/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    @commands.command(help="This will put a glass effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def glass(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/glass/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    @commands.command(help="This will put a comrade effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def comrade(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/comrade/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    @commands.command(help="This will put a wasted effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def wasted(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/wasted/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    @commands.command(help="This will put a passed effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def passed(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/passed/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    @commands.command(help="This will put a triggered effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def triggered(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/triggered/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    @commands.command(help="This will put a Greyscale effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def Greyscale(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/greyscale"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    
    @commands.command(help="This will put a sepia effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def sepia(self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/sepia"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    
    
    @commands.command(help="This will put a Blurple  effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def Blurple (self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/blurple2"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    
    
    @commands.command(help="This will put a Blurple old effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def Blurpleold (self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/blurple"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")


    @commands.command(help="This will put a Wanted old effect over the profile", description="Image overlays for you discord profile pic")
    async def wanted (self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        url = f"https://michaelapi.herokuapp.com/filters/wanted?image_url={member.avatar.url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()

        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    @commands.slash_command(help="This will put a Wanted old effect over the profile", description="Image overlays for you discord profile pic")
    async def wanted (self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        url = f"https://michaelapi.herokuapp.com/filters/wanted?image_url={member.avatar.url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()

        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.respond(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")
    

        
    @commands.command(help="This will put a pixelate effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def pixelate (self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/pixelate"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")


    @commands.command(help="This will put a Trash old effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def Trash (self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        url = f"https://michaelapi.herokuapp.com/filters/trash?image_url={member.avatar.url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()

        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    @commands.command(name = "ghost" ,help="This will put a Trash old effect over the profile", extras={"category":"Search"}, usage="[@member]", description="Image overlays for you discord profile pic")
    async def ghost__command (self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        url = f"https://michaelapi.herokuapp.com/filters/ghost?url={member.avatar.url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()

        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")

    @commands.slash_command(name = "ghost", description="This will put a Trash old effect over the profile")
    async def ghost__slash (self, ctx, member: discord.Member=None):

        if member is None:
            member = ctx.author
            
        url = f"https://michaelapi.herokuapp.com/filters/ghost?url={member.avatar.url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                    f = await aiofiles.open(f'./tempstorage/overlay{ctx.author.id}.png', mode='wb')
                    await f.write(await resp.read())
                    await f.close()

        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.respond(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")



def setup(client):
    client.add_cog(filter(client))
    
