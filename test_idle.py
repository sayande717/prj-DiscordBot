import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TEST_BOT_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle)
        print(f'Logged in')

intents = discord.Intents.default()
client = MyClient(intents=intents)
client.run(TOKEN)