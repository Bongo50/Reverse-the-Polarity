# invite: https://discord.com/api/oauth2/authorize?client_id=866403823010840588&permissions=67628096&scope=bot

import discord
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

goodbyeWords = ['i\'m leaving', 'i\'m going', 'gtg', 'got to go', 'i have to go', 'i must go', 'i must depart', 'i\'m going', 'i\im leaving', 'bye for now']

def url_ready(text):
    newText = ""
    for char in text:
        if char != " ":
            newText += char
        elif char == " ":
            newText += "_"
    return(newText)

def tardis_get_random():
    response = requests.get("https://tardis.fandom.com/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json")
    page_json = response.json()
    print("Random page requested:")
    print(page_json)
    page_name = page_json["query"]["random"][0]["title"]
    page_url = "https://www.tardis.fandom.com/wiki/" + page_name
    page = url_ready(page_url)
    return(page)

def tardis_get_page_contents(page):
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

def doctorwhumour_top():
    response = requests.get("https://www.reddit.com/r/DoctorWhumour/top.json?limit=1&t=hour", headers = {'User-agent': 'Reverse the Polarity!'})
    meme_json = response.json()
    print(meme_json)
    meme_title = meme_json["data"]["children"][0]["data"]["title"]
    meme_image = meme_json["data"]["children"][0]["data"]["thumbnail"]
    meme_image = meme_image.split("?", 1)[0]
    meme = "**" + meme_title + "**: " + meme_image
    return(meme)

def rtpotnf_search(query):
    response = requests.get("https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=UCH50geW3LYlhBt8PVN0UHng&q="+query+"&key="+os.getenv('GOOGLE_TOKEN'))
    results_json = response.json()
    result_id = results_json["items"][0]["id"]["videoId"]
    result_url = "https://www.youtube.com/watch?v="+result_id
    return(result_url)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="?help for help"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    #test command
    if msg.startswith('?test'):
        await message.reply('I\'m working')

    #invite
    if msg.startswith('?invite'):
        await message.reply("https://discord.com/api/oauth2/authorize?client_id=866403823010840588&permissions=67628096&scope=bot")

    #help
    if msg.startswith('?help'):
        await message.reply('''**==Help Message==**
`?help` - this message
`?test` - check if I'm working
`?invite` - get an invite link
`?goodnight` or `?gn` - send the goodnight image
`?goodbye` or `?gb` - send the goodbye video
`?rtpotnfsearch <search query>` - search YouTube for a video by Reverse the Polarity of the Neutron Flow
`?tardisrandom` or `?tr` - get a random page from Tardis Data Core
`?tardispagecontents <page name>` or `?tpc <page name>` - get the first 2000 characters of a Tardis Data Core Page (**Warning: this is very buggy!**)
`?doctorwhumor` or `?dwmeme` - get the hottest meme from the last hour from r/DoctorWhumor
`?freeaudio` or `?fa` - get a link to my website with a list of legally free Doctor Who audio dramas''')

    #random Tardis page
    if msg.startswith('?tardisrandom') or msg.startswith('?tr'):
        page = tardis_get_random()
        await message.reply(page)

    #get contents of Tardis page
    if msg.startswith('?tardispagecontents'):
        page = msg.split("?tardispagecontents ",1)[1]
        contents = tardis_get_page_contents(page)
        await message.reply(contents)
    if msg.startswith('?tpc'):
        page = msg.split("?tpc ",1)[1]
        contents = tardis_get_page_contents(page)
        await message.reply(contents)

    #get top meme from last hour on r/DoctorWhumor
    if msg.startswith('?doctorwhumor') or msg.startswith('?dwmeme'):
        post = doctorwhumour_top()
        await message.reply(post)

    #search for a video from Reverse the Polarity of the Neutron Flow
    if msg.startswith('?rtpotnfsearch'):
        searchQuery = url_ready(msg.split("?rtpotnfsearch ",1)[1])
        result = rtpotnf_search(searchQuery)
        await message.reply(result)

    #goodnight image
    if msg.startswith('?goodnight') or msg.startswith('?gn'):
        await message.reply(file=discord.File('goodnight.jpg'))

    #goodbye video
    if msg.startswith('?goodbye') or msg.startswith('?gb'):
        await message.reply(file=discord.File('goodbye.mp4'))

    #free audios
    if msg.startswith('?freeaduio') or msg.startswith('?fa'):
        await message.reply('https://www.bongo50.ga/Doctor-Who/get-started-with-audio.html#free')

    #goodbye video
    for i in goodbyeWords:
        if i in msg.lower():
            await message.reply(file=discord.File('goodbye.mp4'))
            break

client.run(os.getenv('DISCORD_TOKEN'))
