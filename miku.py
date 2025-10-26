import os
from dotenv import load_dotenv
import discord
from discord import app_commands  
from discord.ext import commands 
from datetime import datetime, timedelta
import asyncio
import threading
load_dotenv() 

MIKUTOKEN = os.getenv("MIKUTOKEN")

intents = discord.Intents.default()  # 使用默認的 intents
intents.messages = True  # 許可機器人讀取訊息
intents.message_content = True
intents.guilds = True
intents.members = True

san_days_ago = datetime.utcnow() - timedelta(days=3)
GUILD_ID = 1346245323789438988
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="del", description="刪除特定使用者三天內的所有訊息(快速)")
@app_commands.describe(text="刪除目標的ID")
@app_commands.checks.has_permissions(administrator=True)
async def delmsg(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"已收到指令，執行中…")
    deleted_count = 0
    target_name = "User"
    for channel in interaction.guild.text_channels:
        try:
            async for msg in channel.history(limit=None, after=san_days_ago):
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
                        await asyncio.sleep(0.05)  # 控制刪除速率
                    except discord.Forbidden:
                        pass
        except discord.Forbidden:
            continue
    print(f"已刪除 {target_name} 的訊息，共 {deleted_count} 則。")
    if deleted_count == 0:
        await interaction.followup.send("查無此ID的訊息", ephemeral=True)
    else:
        await interaction.followup.send(f"已刪除 {deleted_count} 則訊息", ephemeral=True)
@delmsg.error
async def delmsg_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(f"需要管理者權限使用這個指令。", ephemeral=True)


        
        

@bot.tree.command(name="delall", description="刪除特定使用者的所有訊息")
@app_commands.describe(text="刪除目標的ID")
@app_commands.checks.has_permissions(administrator=True)
async def delmsg(interaction: discord.Interaction, text: str):
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
                        await asyncio.sleep(0.05)  # 控制刪除速率
                    except discord.Forbidden:
                        pass
        except discord.Forbidden:
            continue
    print(f"已刪除 {target_name} 的訊息，共 {deleted_count} 則。")
    if deleted_count == 0:
        await interaction.followup.send("查無此ID的訊息", ephemeral=True)
    else:
        await interaction.followup.send(f"已刪除 {deleted_count} 則訊息", ephemeral=True)
        
@delmsg.error
async def delmsg_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(f"需要管理者權限使用這個指令。", ephemeral=True)



@bot.event
async def on_ready():
    print(f'{bot.user} 已上線')
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild) 

bot.run(MIKUTOKEN)  
