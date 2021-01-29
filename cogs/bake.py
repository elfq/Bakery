import discord
from discord.ext import commands
from utils.database import create_tables, sqlite

class Bake(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()

  @commands.group(invoke_without_command=True)
  async def bake(self, ctx):
    embed = discord.Embed(
      title="Baking!",
      description="You can bake an item by running `b!bake (item name)`, be aware that there is a cooldown for baking each item!",
      color=discord.Colour.blurple()
    )
    embed.add_field(name="Sections", value="`Cake`", inline=True)

    embed.set_thumbnail(url=self.bot.user.avatar_url)
    embed.set_footer(text="BakeryBot - b!")
    await ctx.send(embed=embed)

  @bake.command()
  async def cake(self, ctx):
    cake_count = 1 
    await ctx.send(cake_count)

def setup(bot):
  bot.add_cog(Bake(bot))