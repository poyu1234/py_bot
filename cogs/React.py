import discord
from discord.ext import commands
from discord import app_commands
from core.classes import Cog_Extension
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class React(Cog_Extension):

    @commands.Cog.listener()
    async def on_ready(self):
        print("React is ready")

    @commands.Cog.listener()
    # 當有訊息時
    async def on_message(self, message):
        # 排除自己的訊息，避免陷入無限循環
        if message.author == self.client.user:
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

        if message.content.startswith('云琦😢'):
            pic = discord.File(jdata['wake_up'])
            await message.channel.send(f'<@{message.author.id}>', file=pic)

    @commands.hybrid_command()
    @app_commands.guilds(discord.Object(id=int(jdata["PY_guild_id"])))
    async def greet(self, ctx):
        await ctx.send(f"hi! <@{ctx.author.id}>")


async def setup(client):
    await client.add_cog(React(client), guilds=[discord.Object(id=int(jdata["PY_guild_id"]))])
