import discord
from discord import app_commands
from discord.ext import commands

import random
import json

class Weapon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='weapon', description='ブキをランダムに抽選.')
    async def weapon(self, interaction: discord.Interaction):
        print(f"{interaction.user}:/weapon")
        
        with open("weapons.json", "r", encoding="utf-8") as f:
            weapons = json.load(f)
        
        weapon = random.choice(weapons)
        
        print(f"【{interaction.user.display_name}】 抽選結果 : {weapon['name']['ja_JP']}")
        
        embed = discord.Embed()
        embed.description = f"【{interaction.user.display_name}】 抽選結果 : {weapon['name']['ja_JP']}"
        await interaction.response.send_message(embed = embed)

    @app_commands.command(name='weapon_all', description='指定したチャンネルのメンバー全員のブキをランダムに抽選.')
    async def weapon_all(self, interaction: discord.Interaction):
        print(f"{interaction.user}:/weapon_all")
        
        # VCにいない場合
        if interaction.user.voice is None:
            await interaction.response.send_message(
                "ボイスチャンネルに入ってから実行してください。",
                ephemeral=True
            )
            return
        
        with open("weapons.json", "r", encoding="utf-8") as f:
            weapons = json.load(f)
        
        # コマンドを実行したユーザーがいるVCを取得
        voice_channel = interaction.user.voice.channel
        # VCにいるユーザー全員を取得
        members = voice_channel.members
        
        # 結果を作成
        results = []
        for member in members:
            weapon = random.choice(weapons)
        
            results.append(
                f"【{member.display_name}】 {weapon['name']['ja_JP']}"
            )

        # 結果送信.
        embed = discord.Embed(
            title="ブキ抽選結果",
            description="\n".join(results)
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Weapon(bot))