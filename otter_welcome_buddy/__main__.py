"""
Principal function to be called by Docker
"""

import asyncio
import os

from common.constants import COMMAND_PREFIX
from discord.ext.commands import Bot
from startup import intents

# @client.event
# async def on_ready():
# say_hi()
# print(f"We have logged in as {client.user}")


# @client.event
# async def on_member_join(member):
# print("Someone joined")
# await member.send("Welcome To The Discord")


# @client.event
# async def on_message(message):
# if message.author == client.user:
# return

# print(message.author.id)
# if message.content.startswith("$hello"):
# await message.author.send("test")


async def main() -> None:
    """Orchestration function"""
    # intents: discord.Intents = discord.Intents.default()
    # intents.message_content = True
    # intents.members = True
    bot: Bot = Bot(
        command_prefix=COMMAND_PREFIX, intents=intents.get_registered_intents()
    )

    async with bot:
        await bot.load_extension("otter_welcome_buddy.cogs.new_user_joins")
        await bot.start(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
