import discord
from discord.ext import commands
from utils.database import create_tables, sqlite

tables = create_tables.creation(debug=True)
if not tables:
    sys.exit(1)

class Profile(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = sqlite.Database()
    self.username_regex = r"^\w+"

 def check_existing_profile(self, user_id):
   data = self.db.fetchrow("SELECT * FROM profile_name WHERE user_id=?", (user_id,))
   if data:
       return data["profile_name"]
    else:
       return None


 @commands.command(
   name="start"
 )
 async def start_(self, ctx):
   """ Create a profile! """
   profile_exists = self.check_existing_profile(ctx.author.id)
   if profile_exists:
            return await ctx.send(
                f":x: You've created created a profile!"
            )

   start_msg = await ctx.send(f"Hello {ctx.author.mention}! Please choose a username for your profile!")
        confirm = random.randint(10000, 99999)


        def check_confirm(m):
            if (m.author == ctx.author and m.channel == ctx.channel):
                if (m.content.startswith(str(confirm))):
                    return True
            return False

    setname = user.content.split(" ")[0]


    confirm_msg = await ctx.send(
            f"Alright **{ctx.author.name}**, do you confirm that your username is {setname}?\nType `{confirmcode}` to confirm this choice\n"
        )

        try:
            user = await self.bot.wait_for('message', timeout=30.0, check=check_confirm)
        except asyncio.TimeoutError:
            return await confirm_msg.edit(
                content=f"~~{confirm_msg.clean_content}~~\n\nStopped process..."
            )

        self.db.execute("INSERT INTO profile_name VALUES (?, ?)", (ctx.author.id, setname))
        await ctx.send(f":checkmark: Your username is now set in my database!")