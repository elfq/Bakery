import discord
from discord.ext import commands
from utils.database import create_tables, sqlite
import random
import asyncio
import re


tables = create_tables.creation(debug=True)
if not tables:
    sys.exit(1)

class Profile(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()
    self.username_regex = r"^[^@]*$"

  def check_existing_profile(self, user_id):
   data = self.db.fetchrow("SELECT * FROM Accounts WHERE user_id=?", (user_id,))
   if data:
     return data["profile_name"]
   return None


  @commands.command(
   name="start")
  async def start_(self, ctx):
   """ Create a profile! """
   profile_exists = self.check_existing_profile(ctx.author.id)
   if profile_exists:
     return await ctx.send(f":x: You've already created a profile!")

   start_content = await ctx.send(f"Hello {ctx.author.mention}! Please choose a username for your profile!")
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
            content=f"~~{start_content.clean_content}~~\n\n:x: Account creation failed!")

   


   setname = user.content

   confirm_msg = await ctx.send(f"Okay {ctx.author.mention}, are you sure you want to set your username to **`{setname}`**? Please type `{confirm}` if you're sure!")

   try:
       user = await self.bot.wait_for('message', timeout=30.0, check=check_confirm)
   except asyncio.TimeoutError:
         return await confirm_msg.edit(
            content=f"~~{confirm_msg.clean_content}~~\n\n:x: Account creation process stopped...")

   
   
   self.db.execute("INSERT INTO Accounts VALUES (?, ?)", (ctx.author.id, setname))
   await ctx.send(f"✅ Your profile is now saved in my database!")


  @commands.command(name="profile")
  async def profile_(self, ctx):
    embed = discord.Embed(
      title="Your Profile",
      description=f"**Name:** {self.check_profile(ctx.author.id)}",
      color = discord.Colour.red())

    await ctx.reply(embed=embed)



def setup(bot):
  bot.add_cog(Profile(bot))