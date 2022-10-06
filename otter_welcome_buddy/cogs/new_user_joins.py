"""
When a user joins, sends reactionable message
"""
from discord.ext import commands


class Greetings(commands.Cog):
    """Custom message"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Ready Event"""
        print("We have logged in ")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send Welcome message to new member"""
        print("User Joined")
        await member.send("Welcome To Project Nutria")


async def setup(bot):
    """Required setup method"""
    await bot.add_cog(Greetings(bot=bot))
