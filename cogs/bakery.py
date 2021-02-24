import discord
import random
import asyncio
import re
from discord.ext import commands
from utils.database import create_tables, sqlite

tables = create_tables.creation(debug=True)
if not tables:
 sys.exit(1)

class Bakery(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()
    self.username_regex = r"^[^@]*$"

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
  async def bakery(self, ctx):
    embed = discord.Embed(
      title = "Bakery - Menu",
      description = "Commands that relate to **Bakery**, to use a command, type `b!bakery <section>`.",
      color = discord.Colour.blurple()
    )
    embed.set_thumbnail(url = self.bot.user.avatar_url)
    embed.add_field(name = "Sections", value = "**start**\n**view**")
    await ctx.reply(embed = embed)


  @bakery.command(name = "start")
  async def start_(self, ctx):
   if self.bakery_name(ctx.author.id):
     return await ctx.send(f":x: You've already created a bakery!")

   start_content = await ctx.send(f"Hello {ctx.author.mention}! Please choose a name for your bakery!")

   def check_name(m):
     if (m.author == ctx.author and m.channel == ctx.channel):
       if re.compile(self.username_regex).search(m.content):
         return True
     return False

   try:
     user = await self.bot.wait_for('message', timeout = 30.0, check = check_name)
   except asyncio.TimeoutError:
     return await start_content.edit(
       content = f"~~{start_content.clean_content}~~\n\n:x: Bakery creation failed!")

   bakery_name = user.content
   confirm_msg = await ctx.send(f"Okay {ctx.author.mention}, are you sure you want to set your Bakery's Name to **`{bakery_name}`**? Please react with ✅ if you're sure.")
   await confirm_msg.add_reaction("✅")

   def check(reaction, user):
     return user == ctx.author and str(reaction.emoji) in ['✅'] and user != self.bot.user

   try:
     reaction, user = await self.bot.wait_for('reaction_add', check = check, timeout=60)

   except asyncio.TimeoutError:
     await ctx.send(":x: Timeout error, be a little more faster next time, okay?")

   else:
     if str(reaction.emoji) == '✅':
       self.db.execute("INSERT INTO Bakery VALUES (?, ?, ?, ?)", (ctx.author.id, bakery_name, 100, 1))
       self.db.execute("INSERT INTO Baked VALUES (?, ?)", (ctx.author.id, 1))
       await ctx.reply(f"✅ Your Bakery has been created!")


  @bakery.command(name="view")
  async def view_(self, ctx):
   if self.bakery_name(ctx.author.id) == None:
     return await ctx.send(f":x: You need to create a bakery in order to use this command, use **`b!bakery start`** to create one.")

   embed = discord.Embed(
     title = f"{ctx.author}'s Bakery",
     color = discord.Colour.blurple()
   )
   embed.add_field(name = "Profile", value = f"**Bakery's name:** {self.bakery_name(ctx.author.id)}\n**Level:** {self.bakery_level(ctx.author.id)}\n**BakeBucks:** {self.bakery_bucks(ctx.author.id)}", inline=False)
   embed.add_field(name = "Baked Items", value = f"**Cakes:** {self.baked_cakes(ctx.author.id)}", inline=False)
   embed.set_thumbnail(url = ctx.author.avatar_url)
   await ctx.reply(embed = embed)



def setup(bot):
  bot.add_cog(Bakery(bot))