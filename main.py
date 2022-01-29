import os

from discord.ext import commands
from dotenv import load_dotenv

# TODO: Write error handler

if __name__ == '__main__':
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    bot = commands.Bot(command_prefix="!")

    bot.load_extension("LoLBot")

    bot.run(DISCORD_TOKEN)
