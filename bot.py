import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Événement quand le bot est prêt
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} !")

# Commande simple
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Lancer le bot
bot.run("MTMwOTUwNjUxNDQ1Njk0MDU5NQ.GgwhYm.RWukH2pqgMLi2F-SPHuE798HEnSQCnUIW2Ba2w")
