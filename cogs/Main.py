import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Main(Cog_Extension):

    @commands.Cog.listener()
    async def on_ready(self):
        print("Main is ready")

    @commands.command()
    async def ping(self, ctx):
        bot_latency = round(self.client.latency*1000)

        await ctx.send(f"Pong! {bot_latency} ms.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(int(jdata["welcome_id"]))
        await channel.send(f'{member} join!')

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        channel = self.client.get_channel(int(jdata["bye_id"]))
        await channel.send(f'{member} leave!')


async def setup(client):
    await client.add_cog(Main(client))
