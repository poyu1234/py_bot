import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
import json
import aiohttp

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class aclient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            application_id=jdata["application_id"]
        )
        self.synced = False  # make sure only sync once
        self.initial_extensions = jdata["initial_cogs"]

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        # load cogs
        for file in self.initial_extensions:
            await self.load_extension(file)
        # sync tree
        if not self.synced:
            synced = await self.tree.sync(guild=discord.Object(id=int(jdata["PY_guild_id"])))
            print(f"synced {len(synced)} slash commands")
            self.synced = True

    async def on_command_error(self, ctx, error) -> None:
        await ctx.reply(error, ephemeral=True)

    async def on_ready(self):
        print(f">> {client.user} is online <<")


client = aclient()


@ client.hybrid_command(name="load", with_app_command=True)
@app_commands.guilds(discord.Object(id=int(jdata["PY_guild_id"])))
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    await ctx.reply(f"Loaded {extension} done.")


@ client.hybrid_command(name="unload", with_app_command=True)
@app_commands.guilds(discord.Object(id=int(jdata["PY_guild_id"])))
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await ctx.reply(f'unloaded {extension} done.')


@ client.hybrid_command(name="reload", with_app_command=True)
@app_commands.guilds(discord.Object(id=int(jdata["PY_guild_id"])))
async def reload(ctx, extension):
    await client.reload_extension(f'cogs.{extension}')
    await ctx.reply(f'reloaded {extension} done.')


async def main():
    async with client:
        await client.start(jdata["TOKEN"])

asyncio.run(main())
