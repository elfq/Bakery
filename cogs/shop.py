import discord
from discord.ext import commands
from utils.database import create_tables, sqlite


class Shop(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()

  def bakery_name(self, user_id):
   data = self.db.fetchrow("SELECT * FROM Bakery WHERE user_id=?", (user_id,))
   if data:
     return data["bakery_name"]
   else:
     return None

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

  @commands.group(invoke_without_command = True, case_insensitive = True, aliases = ["store"], help = "Buy new items!")
  async def shop(self, ctx: commands.Context):
    embed = discord.Embed(
      title = "Shop",
      description = "Use `b!buy <item>` to buy it.",
      color = 0x4e5d94
    )
    embed.add_field(name = "Items", value = None)
    await ctx.reply(embed = embed)

  @commands.group(invoke_without_command = True,case_insensitive = True, help = "Sell your inventory.")
  async def sell(self, ctx: commands.Context):
    embed = discord.Embed(
      title = "Store",
      description = "Use `b!sell <item> <amt>` to sell them, you'll get rewarded money based on the item, and how much you have of it.",
      color = 0x4e5d94
    )
    embed.add_field(name = "Inventory", value = f"`🍰 Cake` - `{self.baked_cakes(ctx.author.id)}`")
    await ctx.reply(embed = embed)

  @sell.command(case_insensitive = True, aliases = ["cakes"], help = "Sell cakes.")
  async def cake(self, ctx: commands.Context, amt = 0):
   if self.bakery_name(ctx.author.id) == None:
     await ctx.reply(":x: You need to create a bakery in order to use this command, use **`b!bakery start`** to create one.")
   
   amt = int(amt)

   if amt > self.baked_cakes(ctx.author.id):
     return await ctx.reply(":x: You don't own that much cakes.")
    
   if amt < 0:
     return await ctx.reply(":x: You can't sell negative cakes.")

   multiplied_amt = amt + 5
   
   self.db.execute("UPDATE Bakery SET bakebucks=? WHERE user_id=?", (self.baked_cakes(ctx.author.id) * multiplied_amt, ctx.author.id))
  
   self.db.execute("UPDATE Baked SET cakes=? WHERE user_id=?", (self.baked_cakes(ctx.author.id) - amt, ctx.author.id))
   
   await ctx.reply(f"✅ You've sold **{amt}** cakes, you now have `{self.bakery_bucks(ctx.author.id)}` BakeBucks, and `{self.baked_cakes(ctx.author.id)}` cakes.")

def setup(bot):
  bot.add_cog(Shop(bot))

   
   
   

  