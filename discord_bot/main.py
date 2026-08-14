import discord
from discord.ext import commands

import os

# トークン取得.
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

# サーバ情報.
from config.config import GUILDS

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self):
        await self.load_extension("cogs.vc_notice")
        await self.load_extension("cogs.weapon")

        print("登録されているコマンド:")
        for command in self.tree.get_commands():
            print(f"- /{command.name}")

        for guild in GUILDS:
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"Guild {guild.id}: Synced {len(synced)} commands")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)