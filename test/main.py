import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from helper import *
import socket
load_dotenv()

SERVER_ID = int(os.getenv('SERVER_ID')) # type: ignore
SERVER_COUNT = int(os.getenv('SERVER_COUNT')) # type: ignore
UPSTREAM_DNS_COUNT=int(os.getenv('UPSTREAM_DNS_COUNT')) # type: ignore

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    hostname = socket.gethostname()
    # Background tasks START

    # Background tasks END
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=hostname), status=discord.Status.online)
    await bot.tree.sync(guild=discord.Object(id=SERVER_ID))
    print(f"Bot: Logged in.")

bot.run(os.getenv('TEST_BOT_TOKEN')) # type: ignore