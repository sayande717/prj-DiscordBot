from common import *
from discord.ext import commands
import discord
import os

# Import Bot Token
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv('bot_token')

# Bot Intents
intent = discord.Intents.default()
intent.message_content = True

# Bot Command prefix
bot = commands.Bot(intents=intent, command_prefix='$')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening,name='$info'))

# Scope: Information / Help
@bot.command()
async def info(ctx):
    channelID = ctx.channel.id
    try:
        await ctx.channel.send(
            f"\< **Information/Help** /> \
            \n> Channel: **#{bot.get_channel(channelID)}** \
            \n> Scope: {getString(channelID,'scope')} \
            \n> Description: {getString(channelID,'description')} \
            \n \
            \nEnjoy! :innocent:"
            )
    except KeyError:
        await ctx.channel.send(getString(0, 'mistake'))

@bot.command()
async def calc(ctx, expression1='', expression2=''):
    if ctx.channel.id == 999999999999999999: # Calculations
        result = getCalcResult(expression1, expression2)
        resultPrefix = f'Answer ='
        if result == False:
            await ctx.channel.send(getString(0,'mistake'))
        else:
            await ctx.channel.send(f'{resultPrefix} **{result}**')
            
@bot.command()
async def gen(ctx,noOfDigits=4):
    if ctx.channel.id == 999999999999999999: # Random number generator
        strOut = getRandomNumber(noOfDigits)
        if len(strOut) == 0:
            strOut = getString(0,'mistake')
        await ctx.channel.send(strOut)

bot.run(bot_token)