import asyncio
import re


from string import Template


def strfdelta(tdelta, fmt):
    """strftime but operated with :class:`datetime.timedelta` instead
    :param tdelta: timedelta object targeted
    :param fmt: format string
    :return: a formatted string
    """

    class DeltaTemplate(Template):
        delimiter = "%"

    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    return DeltaTemplate(fmt).substitute(**d)

from datetime import datetime, timedelta
from discord.ext.commands import (
    Bot,
    Cog,
    command,
    Context,
    RoleConverter,
    TextChannelConverter,
)
from discord import Message, TextChannel


class BumpReminder(Cog):
    def __init__(self, bot: Bot):
        self.loop = bot.loop  # event loop spawned by bot.run()

    @staticmethod
    def is_successful_bump(msg: Message):
        """Tell if a discord message is a successful DISBOARD bump."""

        successful_bump = r"""<@!?\d+>,\s*
        \s*Bump done :thumbsup:
        \s*Check it on DISBOARD: https://disboard\.org/"""

        if len(msg.embeds) != 1 or msg.author.id != 302050872383242240:
            return False
        elif re.match(successful_bump, msg.embeds[0].description) is None:
            return False
        else:
            return True

    def ping_target(self, channel: TextChannel):
        asyncio.ensure_future(
            channel.send(
                f"A bump is available %s!"
            ),
            loop=self.loop,
        )

    @Cog.listener()
    async def on_message(self, msg: Message):
        if msg.guild.id in self.bump_roles:
            if self.is_successful_bump(msg):
                self.loop.call_later(7200, self.ping_target, msg.channel)


def setup(client):
    client.add_cog(BumpReminder(client))
