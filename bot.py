import disnake
from disnake.ext import commands

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all())

temp_voice_channels = set()


@bot.command()
@commands.is_owner()
async def load(ctx, extension) -> None:
    bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def unload(ctx, extension) -> None:
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def reload(ctx, extension) -> None:
    bot.reload_extension(f'cogs.{extension}')


for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(BOT_TOKEN)