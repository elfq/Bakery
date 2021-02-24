import discord
from discord.ext import commands
from utils.database import create_tables, sqlite

class Bake(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()

  def bakery_name(self, user_id):
   data = self.db.fetchrow("SELECT * FROM Bakery WHERE user_id=?", (user_id,))
   if data:
     return data["bakery_name"]
   else:
     return None

  def bakery_level(self, user_id):
   data = self.db.fetchrow("SELECT * FROM Bakery WHERE user_id=?", (user_id,))
   if data:
     return data["level"]
   else:
     return 0

  def bakery_bucks(self, user_id):
   data = self.db.fetchrow("SELECT * FROM Bakery WHERE user_id=?", (user_id,))
   if data:
     return data["bakebucks"]
   else:
     return 0

  def baked_cakes(self, user_id):
   data = self.db.fetchrow("SELECT * FROM Baked WHERE user_id=?", (user_id,))
   if data:
     return data["cakes"]
   else:
     return 0

  @commands.group(invoke_without_command=True)
  async def bake(self, ctx):
    embed = discord.Embed(
      title="Baking!",
      description="You can bake an item by running `b!bake (item name)`, be aware that there is a cooldown for baking each item!",
      color=discord.Colour.blurple()
    )
    embed.add_field(name="Sections", value="`Cake`", inline=True)

    embed.set_thumbnail(url=self.bot.user.avatar_url)
    embed.set_footer(text="BakeryBot")
    await ctx.send(embed=embed)

  @bake.command(name="cake", aliases=["cakes"])
  async def BakeCake(self, ctx):
    self.db.execute("UPDATE Baked SET cakes=? WHERE user_id=?", (self.baked_cakes(ctx.author.id) + 1, ctx.author.id))
    embed = discord.Embed(
      title = "🍰",
      description = f"You've just baked **1** cake, you now have *{self.baked_cakes(ctx.author.id)} cakes!*",
      color = discord.Colour.blurple()
    )
    await ctx.reply(embed=embed)

  

def setup(bot):
  bot.add_cog(Bake(bot))
