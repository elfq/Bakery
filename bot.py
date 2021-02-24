from templatebot import Bot
from discord import AllowedMentions, Activity, Game
from os import environ as env
from dotenv import load_dotenv
import discord
from discord.ext import fancyhelp

bot = Bot(
    name="BakeryBot",
    command_prefix="b!",
    allowed_mentions=AllowedMentions(
        everyone=False, roles=False, users=True),
    help_command=fancyhelp.EmbeddedHelpCommand(color=0x4e5d94),
    activity=Game("with cakes 🍰"),
)

bot.VERSION = "1.0.0"

bot.load_initial_cogs(
    "cogs.bakery", "cogs.bake", "cogs.shop"
)

@bot.event
async def on_command_error(ctx, error):
 await ctx.send(f"💥 {error}")

bot.run(env.get("TOKEN", None))
