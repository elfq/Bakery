import discord
import random
import asyncio
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

  @commands.group(invoke_without_command = True)
  async def bake(self, ctx: commands.Context):
    embed = discord.Embed(
      title = "Baking!",
      description = "You can bake an item by running `b!bake (item name)`, be aware that there is a cooldown for baking each item!",
      color = discord.Colour.blurple()
    )
    embed.add_field(name = "Sections", value = "`Cake`", inline = False)
    embed.set_thumbnail(url = self.bot.user.avatar_url)
    await ctx.reply(embed = embed)

  @bake.command(name="cake", aliases = ["cakes"])
  async def BakeCake(self, ctx: commands.Context):
    if self.bakery_name(ctx.author.id) == None:
     return await ctx.send(f":x: You need to create a bakery in order to use this command, use **`b!bakery start`** to create one.")
    cakes = random.randint(1, 5)
    self.db.execute("UPDATE Baked SET cakes=? WHERE user_id=?", (self.baked_cakes(ctx.author.id) + cakes, ctx.author.id))
    oven = await ctx.reply("🍳 Baking...")
    await asyncio.sleep(4)
    embed = discord.Embed(
      title = "🍰 Done!",
      description = f"You've baked **{cakes}** cake(s), you now have **{self.baked_cakes(ctx.author.id)}** cakes!",
      color = discord.Colour.blurple())
    await oven.edit(content = f"Hey {ctx.author.mention}, your cake has finished baking!", embed = embed)

  

def setup(bot):
  bot.add_cog(Bake(bot))
