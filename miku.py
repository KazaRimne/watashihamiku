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
    await interaction.response.send_message(f"已收到指令，執行中…")
    deleted_count = 0
    target_name = "User"

    for channel in interaction.guild.text_channels:
        try:
            async for msg in channel.history(limit=None):
                match = False
                # 判斷 text 是否匹配 ID、username 或暱稱（忽略大小寫）
                if text.isdigit() and str(msg.author.id) == text:
                    match = True
                elif msg.author.name.lower() == text.lower():
                    match = True
                elif msg.author.display_name.lower() == text.lower():
                    match = True

                if match:
                    try:
                        await msg.delete()
                        deleted_count += 1
                        if target_name == "User":
                            target_name = msg.author.display_name
                        await asyncio.sleep(0.25)  # 控制刪除速率
                    except discord.Forbidden:
                        pass
        except discord.Forbidden:
            continue
    print(f"已刪除 {target_name} 的訊息，共 {deleted_count} 則。")
@bot.event
async def on_ready():
    print(f'{bot.user} 已上線')
    guild = discord.Object(id=GUILD_ID)

bot.run(MIKUTOKEN)  
