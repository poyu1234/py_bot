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


@client.command()
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


@client.command()
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'unloaded {extension} done.')


@client.command()
async def reload(ctx, extension):
    await client.reload_extension(f'cogs.{extension}')
    await ctx.send(f'reloaded {extension} done.')


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load()
        await client.start(jdata["TOKEN"])

asyncio.run(main())
