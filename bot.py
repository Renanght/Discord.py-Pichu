import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "/")

# Configuration des intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(
        f"Logged in as {bot.user.name} (ID: {bot.user.id})\n"
        "--------\n"
        f"Current discord.py version: {discord.__version__}\n"
        "--------\n"
        f"Use this link to invite {bot.user.name}:\n"
        f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot\n"
        "--------"
    )
    print("Bot is ready!")

# Charger les extensions
async def load_extensions():
    initial_extensions = ["cogs.general", "cogs.administration"]
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded extension: {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

if __name__ == "__main__":
    asyncio.run(load_extensions())
    bot.run(TOKEN)
