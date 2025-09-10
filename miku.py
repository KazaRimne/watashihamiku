import os
from dotenv import load_dotenv
import discord
from discord import app_commands  
from discord.ext import commands 
import asyncio
import threading
load_dotenv() 

MIKUTOKEN = os.getenv("MIKUTOKEN")

intents = discord.Intents.default()  # 使用默認的 intents
intents.messages = True  # 許可機器人讀取訊息
intents.message_content = True
intents.guilds = True
intents.members = True
CHANNEL_ID = 1347197528264675348 
GUILD_ID = 1346245323789438988
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="del", description=".")
@app_commands.describe(text="ID")
async def delmsg(interaction: discord.Interaction, text: str):
    # 限制只能在指定頻道使用
    if interaction.channel.id != CHANNEL_ID:
        return
    # 嘗試取得目標用戶
    deleted_count = 0
    target_name = "User"

    for channel in interaction.guild.text_channels:
        try:
            async for msg in channel.history(limit=None):
                if str(msg.author.id) == text:
                    try:
                        deleted_count += 1
                        await msg.delete()
                        if target_name == "User":
                            target_name = msg.author.display_name
                    except discord.Forbidden:
                        pass
        except discord.Forbidden:
            continue

@bot.event
async def on_ready():
    print(f'{bot.user} 已上線')
    guild = discord.Object(id=GUILD_ID)

    synced = await bot.tree.sync(guild=guild)
    print(f"已同步 {len(synced)} 個指令到伺服器 {GUILD_ID}")

bot.run(MIKUTOKEN)  
