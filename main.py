#invite: https://discord.com/api/oauth2/authorize?client_id=867699991245619231&permissions=2148002880&scope=bot

import discord
from discord.ext import commands
from discord_slash import SlashCommand
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='t?')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="t?help for help"))
        
@bot.command()
async def ping(ctx):
    await ctx.reply('pong')

@bot.command()
async def help(ctx):
    await ctx.reply('''test''')
    
bot.run(os.getenv('DISCORD_TOKEN'))
