import discord
from discord.ext import commands
from utils.database import create_tables, sqlite
import random
import asyncio
import re


tables = create_tables.creation(debug=True)
if not tables:
    sys.exit(1)

class Bakery(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()
    self.username_regex = r"^[^@]*$"

  def check_existing_profile(self, user_id):
   data = self.db.fetchrow("SELECT * FROM Accounts WHERE user_id=?", (user_id,))
   if data:
     return data["bakery_name"]
   return None


  @commands.command(
   name="start")
  async def start_(self, ctx):
   """ Create a bakery! """
   bakery_exists = self.check_existing_profile(ctx.author.id)
   if bakery_exists:
     return await ctx.send(f":x: You've already created a bakery!")

   start_content = await ctx.send(f"Hello {ctx.author.mention}! Please choose a name for your bakery!")
   confirm = random.randint(10000, 99999)

   def check_name(m):
            if (m.author == ctx.author and m.channel == ctx.channel):
                if re.compile(self.username_regex).search(m.content):
                    return True
            return False


   def check_confirm(m):
     if (m.author == ctx.author and m.channel == ctx.channel):
       if (m.content.startswith(str(confirm))):
           return True
       return False

   try:
         user = await self.bot.wait_for('message', timeout=30.0, check=check_name)
   except asyncio.TimeoutError:
         return await start_content.edit(
            content=f"~~{start_content.clean_content}~~\n\n:x: Bakery creation failed!")

   


   setname = user.content

   confirm_msg = await ctx.send(f"Okay {ctx.author.mention}, are you sure you want to set your Bakery's Name to **`{setname}`**? Please type `{confirm}` if you're sure!")

   try:
       user = await self.bot.wait_for('message', timeout=30.0, check=check_confirm)
   except asyncio.TimeoutError:
         return await confirm_msg.edit(
            content=f"~~{confirm_msg.clean_content}~~\n\n:x: Bakery creation process stopped...")

   
   
   self.db.execute("INSERT INTO Accounts VALUES (?, ?)", (ctx.author.id, setname))
   await ctx.send(f"✅ Your Bakery has been created!")


  @commands.command(name="bakery")
  async def profile_(self, ctx):
    db_bakeryname = self.check_existing_profile(ctx.author.id)
    embed = discord.Embed(
      title=f"{ctx.author}'s' Bakery",
      description=f"**Name:** {db_bakeryname}\n**Bake Bucks:** 0 \n**Level:** 0/100\n**Items Baked:** 0",
      color = discord.Colour.blurple())

    embed.set_footer(text="BakeryBot - v0.1")
    await ctx.reply(embed=embed)



def setup(bot):
  bot.add_cog(Bakery(bot))