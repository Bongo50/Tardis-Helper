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

def url_ready(text):
    newText = ""
    for char in text:
        if char != " ":
            newText += char
        elif char == " ":
            newText += "_"
    return(newText)

def get_random():
    response = requests.get("https://tardis.fandom.com/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json")
    page_json = response.json()
    print("Random page requested:")
    print(page_json)
    page_name = page_json["query"]["random"][0]["title"]
    page_url = "https://www.tardis.fandom.com/wiki/" + page_name
    page = url_ready(page_url)
    return(page)

def get_page_contents(page):
    page = url_ready(page)
    response = requests.get("https://tardis.fandom.com/api.php?action=parse&page="+page+"&prop=text&formatversion=2&format=json")
    page_json = response.json()
    page_html = page_json["parse"]["text"]
    page_part_html = page_html
    page_part_html = page_part_html.replace("<b>", "**")
    page_part_html = page_part_html.replace("</b>", "**")
    page_part_html = page_part_html.replace("<i>", "*")
    page_part_html = page_part_html.replace("</i>", "*")
    page_soup = BeautifulSoup(page_part_html, 'html.parser')
    page_text = page_soup.get_text()
    page_url = "https://tardis.fandom.com/wiki/"+page
    page_trunctuated = page_text[:2000-(len(page_url)+3)]
    message = page_trunctuated+'''
<'''+page_url+'>'
    return message

def search_pages(term, count):
    term = url_ready(term)
    response = requests.get("https://tardis.fandom.com/api.php?action=query&list=search&srsearch="+term+"&srlimit="+count+"&format=json")
    results_json = response.json()
    results = ""
    for n in range(0,int(count)):
        page = results_json["query"]["search"][n]["title"]
        results += "**"+str(n+1)+".** - "+page+": https://www.tardis.fandom.com/wiki/"+url_ready(page)+'''
'''
    return(results)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="t?help for help"))
        
@bot.command()
async def ping(ctx):
    await ctx.reply('pong')
    
@bot.command()
async def help(ctx):
    await ctx.reply('''**== Help Message ==**
`t?help` - this message
`t?ping` - ping the bot (to see if I'm working
`t?random` - get a random page from the (main) namespace
`t?contents <page>` - get the contents of any Tardis page - **note: this does not yet work fully**
`t?search <search query> <number of results>` - search Tardis Data Core. To use a multi-word search query, suround it in `"`''')

@bot.command()
async def random(ctx):
    await ctx.reply(get_random())

@bot.command()
async def contents(ctx, page):
    await ctx.reply(get_page_contents(page))

@bot.command()
async def search(ctx, term, count):
    await ctx.reply(search_pages(term, count))
    
bot.run(os.getenv('DISCORD_TOKEN'))
