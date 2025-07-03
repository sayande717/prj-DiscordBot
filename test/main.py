import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from helper import *
import socket
load_dotenv()

SERVER_ID = int(os.getenv('SERVER_ID'))
SERVER_COUNT = 3

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    hostname = socket.gethostname()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=hostname), status=discord.Status.online)
    await bot.tree.sync(guild=discord.Object(id=SERVER_ID))
    print(f"Bot: Logged in.")

"""
Command: `/status_dns`
Utility: Checks the status of local/upstream DNS servers.
Input: Server Type:
    - "lan": Local DNS servers
    - "wan": Upstream DNS servers
Output:
    - "lan":
        ```
        ## Local DNS Status:
        Server-0: :green_circle:
        Server-1: :green_circle:
        Server-2: :red_circle:
        ```
    - "wan":
        ```
        ## Upstream DNS Status:
        Server-0: :green_circle:
        Server-1: :green_circle:
        ```
"""
@bot.tree.command(guild=discord.Object(id=SERVER_ID), name="status_dns", description="Check if the DNS servers are responding")
async def status_dns(interaction: discord.Interaction,
                     server_type: str = "lan"):
    await interaction.response.defer(thinking=True)
    output_list = helper_dns_status(server_type)
    if server_type == "lan":
        output_str = "## Local DNS Status:\n" + "\n".join(f"- {line}" for line in output_list)
    elif server_type == "wan":
        output_str = "## Upstream DNS Status:\n" + "\n".join(f"- {line}" for line in output_list)
    else:
        output_str = "-1"
    await interaction.followup.send(output_str)

bot.run(os.getenv('TEST_BOT_TOKEN'))
