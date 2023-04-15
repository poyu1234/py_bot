import discord
from discord.ext import commands
import json
import os

# client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 處理json
with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# 調用 event 函式庫


@bot.event
# 當機器人完成啟動時
async def on_ready():
    print(f">> {bot.user} is online <<")


@bot.event
# 當有訊息時
async def on_message(message):
    # 排除自己的訊息，避免陷入無限循環
    if message.author == bot.user:
        return
    # 如果以「說」開頭
    if message.content.startswith('說'):
        # 分割訊息成兩份
        tmp = message.content.split(" ", 2)
        # 如果分割後串列長度只有1
        if len(tmp) == 1:
            await message.channel.send("你要我說什麼啦？")
        else:
            await message.channel.send(tmp[1])

    await bot.process_commands(message)  # 讓command順利運作


@bot.event
# 當有成員加入
async def on_member_join(member):
    channel = bot.get_channel(int(jdata["welcome_id"]))
    await channel.send(f'{member} join!')


@bot.event
# 當有成員離開
async def on_member_leave(member):
    channel = bot.get_channel(int(jdata["bye_id"]))
    await channel.send(f'{member} leave!')


@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}(ms)')


# # 引入cog
# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         bot.load_extension(f'cogs.{filename[:-3]}')
#         print(f'cogs.{filename[:-3]}').

if __name__ == "__main__":
    bot.run(jdata["TOKEN"])
