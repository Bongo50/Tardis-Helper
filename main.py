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
    page_url = "https://tardis.fandom.com/wiki/" + page_name
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
        results += "**"+str(n+1)+".** - "+page+": <https://tardis.fandom.com/wiki/"+url_ready(page)+'''>
'''
    return(results)



@bot.command()
async def ping(ctx):
    await ctx.reply('pong')

@bot.command()
async def invite(ctx):
    await ctx.reply('https://discord.com/api/oauth2/authorize?client_id=867699991245619231&permissions=2148002880&scope=bot')

@bot.command()
async def servercount(ctx):
    await ctx.reply("I am a member of "+str(len(bot.guilds))+" servers.")

@bot.command()
async def info(ctx):
    await ctx.reply('''**== Info Message ==**
<@867699991245619231> is a bot designed to intergrate some functions of Tardis Data Core, the Doctor Who Wiki, into Discord.
I was created by <@409330514693193728> (and yes, he gets pinged every time this command is run).
My prefix is `t?`.
For help, run `t?help`.
To invite me, run `t?invite`.

My profile picture is taken from <https://tardis.fandom.com/wiki/File:Favicon.ico>
Tardis Data Core can be visited at <https://tardis.fandom.com/>.

GitHub: <https://github.com/Bongo50/Tardis-Helper>
Bongo50's Website: <https://www.bongo50.ga/>

Tardis Helper is in no way officially affiliated with Tardis Data Core. Bongo50, however, does edit there frequently as [[User:Bongolium500]].''')
    
@bot.command()
async def help(ctx):
    await ctx.reply('''**== Help Message ==**
**=== Commands ===**
`t?help` - this message
`t?info` - get some information about me
`t?ping` - ping the bot (to see if I'm working
`t?servercount` - count the number of servers I'm in
`t?invite` - get an invite link
`t?random` - get a random page from the (main) namespace
`t?contents <page>` - get the contents of any Tardis page - **note: this does not yet work fully**
`t?search <search query> <number of results>` - search Tardis Data Core. To use a multi-word search query, suround it in `"`

**=== Other ===**
Messages containg links marked as [[link text]] or templates marked as {{template name}} will be replied to with links to the pages in question.''')

@bot.command()
async def random(ctx):
    await ctx.reply(get_random())

@bot.command()
async def contents(ctx, page):
    await ctx.reply(get_page_contents(page))

@bot.command()
async def search(ctx, term, count):
    await ctx.reply(search_pages(term, count))



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="t?help for help"))

@bot.event
async def on_message(message):
    #check for uses of [[ and link accordingly
    if message.author == bot.user:
        return
    
    if "[[" in message.content:
        message_list = message.content.split('[[')
        links=[]
        for n in range(1,len(message_list)):
            link_list = message_list[n].split(']]')
            links.append(url_ready(link_list[0]))
        urls = ""
        for link in links:
            urls += "<https://tardis.fandom.com/wiki/"+link+'''>
'''
        await message.reply(urls)

    #check for uses of {{ and link accordingly
    if "{{" in message.content:
        message_list = message.content.split('{{')
        links=[]
        for n in range(1,len(message_list)):
            link_list = message_list[n].split('}}')
            links.append(url_ready(link_list[0]))
        urls = ""
        for link in links:
            urls += "<https://tardis.fandom.com/wiki/Template:"+link+'''>
'''
        await message.reply(urls)
    await bot.process_commands(message)
    
bot.run(os.getenv('DISCORD_TOKEN'))
