import discord
from discord.ext import commands
import os
import asyncio
import json

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


@client.event
async def on_ready():
    print(f">> {client.user} is online <<")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load()
        await client.start(jdata["TOKEN"])

asyncio.run(main())
