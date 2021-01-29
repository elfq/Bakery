import discord
from discord.ext import commands
from utils.shard import Bot
import os
from os import environ

bot = Bot(
    command_prefix=environ.get("DISCORD_PREFIX"), prefix=environ.get("DISCORD_PREFIX"),
    developer_ids=environ.get("DEVELOPERS"), command_attrs=dict(hidden=True), intents=discord.Intents(
        guilds=True, members=True, messages=True, reactions=True, presences=True
    )
)


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")


@bot.event 
async def on_ready():
  print("-----------")
  print(f"ID: {bot.user.id}")
  print(f"Username: {bot.user.name}")
  print("Activity: 🍰 Making Cakes")
  print("-----------")
  await bot.change_presence(activity=discord.Game(name="🍰 Making Cakes"))

bot.run(environ.get("DISCORD_TOKEN"))
