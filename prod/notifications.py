import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from helper import *
import subprocess

load_dotenv()
BOT_TOKEN = os.getenv('NOTIFICATIONS_BOT_TOKEN')
SERVER_ID = int(os.getenv('SERVER_ID'))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

"""
Function: `on_ready()`
Utility: Called when the bot has successfully connected to Discord and is ready.
"""
@bot.event
async def on_ready():
    hostname = subprocess.check_output(["hostnamectl", "hostname"]).decode().strip()
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=hostname))
    await bot.tree.sync(guild=discord.Object(id=SERVER_ID))

    # Background tasks START
    wan_speed_periodic.start()
    # Background tasks END

    print(f"Notification Bot: Logged in")


"""
Function: `wan_speed_periodic()`
Interval: Every 3 hours 45 minutes (13500 seconds)
Utility: Periodically checks for new speed test results in a CSV file and sends updates to a Discord channel.
Input: Reads from "./helper/speedtest_results.csv"
Output: Sends formatted speed test results to the specified Discord channel
```
Date: DD.MM.YYYY | Time: HH:MM
Latency: **XX ms**
Upload: **XXX.XX Mbps**
Download: **XXX.XX Mbps**
```
"""
target_wan_speed_csv = "./helper/speedtest_periodic.csv"
last_seen_lines = helper_wan_speed_periodic(target_wan_speed_csv)

@tasks.loop(seconds=13500)
async def wan_speed_periodic():
    global last_seen_lines
    global target_wan_speed_csv
    with open(target_wan_speed_csv, "r") as f:
        lines = set(f.readlines())
    new_lines = lines - last_seen_lines
    if new_lines:
        channel = bot.get_channel(int(os.getenv('CHANNEL_ID_bot_notifications_v0-speedtest')))
        for line in new_lines:
            # Matches with format on CSV: date,time,latency,upload,download
            date, time, latency, upload, download = line.strip().split(",")
            output_str = (
                f"Date: {date} | Time: {time}\n"
                f"Latency: {latency} ms\n"
                f"Upload: {upload} Mbps\n"
                f"Download: {download} Mbps"
            )
            await channel.send(output_str)
        last_seen_lines = lines

bot.run(BOT_TOKEN)