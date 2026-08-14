import discord
from discord.ext import commands
import datetime

from config.config import MESG_CHANNEL

class VC_Notice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        mesg_channel = self.bot.get_channel(MESG_CHANNEL)

        # 入退室以外はreturn.
        if before.channel == after.channel:
            return

        embed = discord.Embed()

        if before.channel is None: #VCへの入室.
            embed.description = f'{member.display_name} joined voice channel {after.channel.name}.'
        elif after.channel is None: #VCからの退出.
            embed.description = f'{member.display_name} left voice channel {before.channel.name}.'
        else: #VC間の移動.
            embed.description = f'{member.display_name} moved from {before.channel.name} to {after.channel.name}.'

        embed.add_field(name = '', value = datetime.datetime.now().strftime('%Y/%m/%d %H:%M'))
    
        await mesg_channel.send(embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(VC_Notice(bot))