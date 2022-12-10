import discord
import datetime
from discord.ext import commands
def micsid(ctx):
    return ctx.author.id == 481377376475938826 or ctx.author.id == 624076054969188363

class DMReply(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dm_channel = 935891510367494154

    @commands.command(aliases=['dmr'])
    @commands.check(micsid)
    async def dmreply(self, ctx, *, msg=None):
        if ctx.message.reference is None:
          return
        else:
            await ctx.message.delete()
            id = ctx.message.reference.message_id
            id = await ctx.channel.fetch_message(id)
            await id.reply(msg)
            id = int(id.content)
        person = await self.client.fetch_user(id)

        if msg is None:
            pass
        else:
            await person.send(msg)

        if ctx.message.attachments is None:
            return
        else:
            for i in ctx.message.attachments:
                em = discord.Embed( color=ctx.author.color)
                em.timestamp = datetime.datetime.utcnow()
                em.set_image(url=i.url)
                await person.send(embed=em)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
        
            cha = await self.client.fetch_channel(self.dm_channel)
            em = discord.Embed(title="New DM", description=f"From {message.author.name}", color=message.author.color)
            em.timestamp = datetime.datetime.utcnow()

            if message.content != "":
                em.add_field(name="Content", value=f"{message.content}")
            await cha.send(content=f"{message.author.id}", embed=em)

            if message.attachments is not None:
                for attachment in message.attachments:
                    if "image/" not in str(attachment.content_type):
                        return await cha.send(attachment.url)
                    em = discord.Embed(title="** **", color=discord.Color.blue())
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_image(url=attachment.url)
                    await cha.send(embed=em)
        try:
            if message.channel.id == self.dm_channel and message.author.id == self.client.owner_id:
                if message.reference is None:
                    return
                else:
                    id = message.reference.message_id
                    id = await message.channel.fetch_message(id)
                    id = int(id.content)
                person = await self.client.fetch_user(id)

                if message.content is None:
                    pass
                else:
                    await person.send(message.content)
                    await message.react("✅")

                if message.attachments is None:
                    return
                else:
                    for i in message.attachments:
                        if "image/" not in str(i.content_type):
                            return await person.send(i.url)
                        em = discord.Embed(color=message.author.color)
                        em.timestamp = datetime.datetime.utcnow()
                        em.set_image(url=i.url)
                        await person.send(embed=em)
                        await message.react("✅")
        except Exception as e:
            print(e)
            await message.react("❌")

def setup(client):
    client.add_cog(DMReply(client))