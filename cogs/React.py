import discord
from discord.ext import commands
from core.classes import Cog_Extension


class React(Cog_Extension):

    @commands.Cog.listener()
    async def on_ready(self):
        print("React is ready")

    # @commands.Cog.listener()
    # # 當有訊息時
    # async def on_message(self, message):
    #     # 排除自己的訊息，避免陷入無限循環
    #     if message.author == self.client.user:
    #         return
    #     # 如果以「說」開頭
    #     if message.content.startswith('說'):
    #         # 分割訊息成兩份
    #         tmp = message.content.split(" ", 2)
    #         # 如果分割後串列長度只有1
    #         if len(tmp) == 1:
    #             await message.channel.send("你要我說什麼啦？")
    #         else:
    #             await message.channel.send(tmp[1])

    #     await self.client.process_commands(message)  # 讓command順利運作

    @commands.command()
    async def greet(self, ctx):
        await ctx.send(f"hi! <@{ctx.author.id}>")


async def setup(client):
    await client.add_cog(React(client))
