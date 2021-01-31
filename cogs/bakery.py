import discord
from discord.ext import commands
from utils.database import create_tables, sqlite
from utils import default, checks
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

  def bakery_name_exists(self, user_id):
        data = self.db.fetchrow("SELECT * FROM Accounts WHERE user_id=?", (user_id,))
        if data:
            return data["bakery_name"]
        else:
            return None

  @commands.group(invoke_without_command=True)
  async def bakery(self, ctx):
    embed = discord.Embed(
      title = "Bakery - Menu",
      description = "Commands that relate to **Bakery**, to use a command, type `b!bakery <section>`.",
      color = discord.Colour.blurple()
    )

    embed.set_thumbnail(url=self.bot.user.avatar_url)
    embed.add_field(name="Sections", value="**start**\n**view**")
    await ctx.reply(embed=embed)


  @bakery.command(name="start")
  async def start_(self, ctx):
   """ Create a bakery! """
   bakery_exists = self.bakery_name_exists(ctx.author.id)
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

   
   channel = self.bot.get_channel(805210381466599424)
   self.db.execute("INSERT INTO Accounts VALUES (?, ?)", (ctx.author.id, setname))
   await ctx.send(f"✅ Your Bakery has been created!")
   embed = discord.Embed(
     title = "Bakery Creation!",
     description = f"**Bakery Name:** {setname}\n**Creator:** {ctx.author.id}\n**Creator's Name:** {ctx.author}",
     color = discord.Colour.blurple()
   )
   embed.set_thumbnail(url=ctx.author.avatar_url)
   await channel.send(embed=embed)


  @bakery.command(name="view")
  async def view_(self, ctx):
    """ View a bakery! """
    bakery_exists = self.bakery_name_exists(ctx.author.id)
    embed = discord.Embed(
      title=f"{ctx.author}'s' Bakery",
      description=f"**Name:** {bakery_exists}\n**Bake Bucks:** 0 \n**Level:** 0/100\n**Items Baked:** 0",
      color = discord.Colour.blurple())

    embed.set_footer(text="BakeryBot - v0.1")
    await ctx.reply(embed=embed)

  
  @commands.command()
  @commands.check(checks.is_moderator)
  async def delete(self, ctx, user: discord.Member,reason='None given.'):
   self.db.execute("DELETE FROM Accounts WHERE user_id=?", (user.id,))
   await ctx.send(f"✅ Successfully deleted {user}'s bakery for `{reason}`'")
   await user.send(f"Hello, your bakery has been deleted for violating the bot's rules, if you feel like this is false, then join https://discord.gg/sDaP9NU and send our moderators a message!\n\nAction by: {ctx.author.mention}\nDeletion Message: `{reason}`")


   




def setup(bot):
  bot.add_cog(Bakery(bot))
