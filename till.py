
# This file is made by REI otherwise known as KeiNeroKami in Github
# ====================<REIME>====================
# This are snippets for making a bot/App in Discord
# Made: 11, 21, 25
# ===============================================

import code
from multiprocessing import process
from pydoc import text
from tkinter import font
from xmlrpc import client
from click import command
from flask import ctx
import nextcord
from nextcord.ext import commands
import textwrap
from nextcord import File
from nextcord import ButtonStyle, Embed, Color
from nextcord.ui import Button, View
import random
from random import choice
from nextcord.utils import get
import json, datetime, asyncio
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
import os
from dotenv import load_dotenv

# ----------------------------------

load_dotenv()
TOKEN = os.getenv("TOKEN")


#Reminder: Please install package DotEnv and use that to store your token as it is important to keep your bot token a secret. I'll tell you about that later for now play around these snippets

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)

# Bonus tip for making slash commands

# ---------- Auto-sync Slash Commands ----------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        status=nextcord.Status.online, # Options: online, idle, dnd, invisible
        activity=nextcord.Activity(
            name="🍃 scars remember everything",
            type=nextcord.ActivityType.playing, # Options: playing, streaming, listening, watching, competing
        )
    )
    print("Presence set!")
    await bot.sync_all_application_commands()
    print("synced!")

# ----------------------------------

# global variables

# ----------------------------------
#autoresponse deleting user trigger

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "*ivantill" in message.content.lower():
        await message.delete()

    await bot.process_commands(message)

    if "gnarly" in message.content.lower():
        await message.channel.send("BOBA TEA 🗣️ (GNARLY)")
        await asyncio.sleep(2)
        await message.channel.send("TESLA 🗣️ (GNARLY)")
        await asyncio.sleep(2)
        await message.channel.send("FRIED CHICKEN 🗣️ (GNARLY)")
        await asyncio.sleep(2)
        await message.channel.send("PARTYIN' IN THE HOLLYWOOD HILLS 🗣️ (UH-UH)")
        await asyncio.sleep(2)
        await message.channel.send("THIS SONG 🗣️ (GNARLY, UH)")
        await asyncio.sleep(2)
        await message.channel.send("OH MY GOD, THAT NEW BEAT 🗣️ (GNARLY; FUCKING GNARLY)")
        await asyncio.sleep(2)
        await message.channel.send("OH MY GOD, IS THIS REAL? 🗣️ (GNARLY)")
        await asyncio.sleep(2)  
        await message.channel.send("EVERYTHING'S GNARLY!!! 👽💚")

# ----------------------------------

@bot.command()
async def ping(ctx):
    embed = nextcord.Embed(title="POONGGG!", description=f"I'm fast and active as ever!, my ping is {round(bot.latency * 1000)}ms!! Have fun with my commands!", color=0x00ff00)
    embed.set_image(url="https://files.catbox.moe/0oftm1.gif")
    await ctx.send(embed=embed)

@bot.slash_command(name="ping", description="Ping the bot")
async def ping_slash(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="POONGGG!", description=f"I'm fast and active as ever!, my ping is {round(bot.latency * 1000)}ms!! Have fun with my commands!", color=0x00ff00)
    embed.set_image(url="https://files.catbox.moe/0oftm1.gif")
    await interaction.response.send_message(embed=embed)

# ----------------------------------

random_gifs = [
    'https://files.catbox.moe/xsmk6l.gif',
    'https://files.catbox.moe/rla8j9.gif',
    'https://files.catbox.moe/7ks45x.gif',
    'https://files.catbox.moe/nxfyu0.gif',
    'https://files.catbox.moe/41q0xa.gif',
    'https://files.catbox.moe/pnxbgj.gif'
]

@bot.command()
async def randomgif(ctx):
    await ctx.send(random.choice(random_gifs))

@bot.slash_command(name="randomgif", description="Random gif setup")
async def randomgif_slash(interaction: nextcord.Interaction):
    await interaction.response.send_message(random.choice(random_gifs))

# ----------------------------------
# bot says hi using user's nickname

@bot.command()
async def hi(ctx):
    nickname = ctx.author.display_name
    await ctx.send(f"Hi {nickname}!")

@bot.slash_command(name="hi", description="Bot says hi")
async def hi_slash(interaction: nextcord.Interaction):
    nickname = interaction.user.display_name
    await interaction.response.send_message(f"Hi {nickname}!")

# ----------------------------------

# store usage counts here  {user_id: count}

usage_count_hug = {}
usage_count_yawn = {}

#random gif list

random_gifs_hugs = [
    'https://files.catbox.moe/8db5n7.gif',
    'https://files.catbox.moe/m9u33i.gif',
    'https://files.catbox.moe/98ml3v.gif',
    'https://files.catbox.moe/v0esu2.gif'
]

random_gifs_yawn = [
    'https://files.catbox.moe/kguxqs.gif',
    'https://files.catbox.moe/nqjtqw.gif',
    'https://files.catbox.moe/wk497f.gif',
    'https://files.catbox.moe/tw1qfu.gif'
    ]


@bot.command()
async def hug(ctx, member: nextcord.Member = None):
    membername = member.display_name if member else "themselves"
    user_id = ctx.author.id

    # increase count for this user
    usage_count_hug[user_id] = usage_count_hug.get(user_id, 0) + 1

    count = usage_count_hug[user_id]

    # default target is self
    if member is None:
        member = ctx.author

    #button logic

    hugback = Button(label="click", style=ButtonStyle.primary)
    embedback = Embed(title=f"{membername} hugged back! {ctx.author.display_name}",color=Color.teal())
    embedback.set_image(random.choice(random_gifs_hugs))

    async def hugback_callback(interaction):
        await interaction.response.send_message(embed=embedback)

    hugback.callback = hugback_callback

    myview = View(timeout=180)
    myview.add_item(hugback)
    
    #hug logic here

    embed = Embed(title=f"{ctx.author.display_name} hugs {membername}!", description=f"{ctx.author.mention} has hugged {count} times", color=Color.teal())
    embed.set_image(random.choice(random_gifs_hugs))
    
    await ctx.send(embed=embed, view=myview)

@bot.slash_command(name="hug", description="Hug someone!")
async def hug(interaction: nextcord.Interaction, member: nextcord.Member = None):
    membername = member.display_name if member else "themselves"
    user_id = interaction.user.id

    # increase count for this user
    usage_count_hug[user_id] = usage_count_hug.get(user_id, 0) + 1
    count = usage_count_hug[user_id]

    # default target
    if member is None:
        member = interaction.user

    # button logic

    hugback = Button(label="click", style=ButtonStyle.primary)
    embedback = Embed(title=f"{membername} hugged back {interaction.user.display_name}!",color=Color.teal())
    embedback.set_image(random.choice(random_gifs_hugs))

    async def hugback_callback(interaction):
        await interaction.response.send_message(embed=embedback)

    hugback.callback = hugback_callback

    myview = View(timeout=180)
    myview.add_item(hugback)

    #hug logic here

    embed = Embed(title=f"{interaction.user.display_name} hugs {membername}!", description=f"{interaction.user.mention} has hugged {count} times", color=Color.teal())
    embed.set_image(random.choice(random_gifs_hugs))

    await interaction.response.send_message(embed=embed, view=myview)

# ----------------------------------

@bot.command()
async def yawn(ctx):

    user_id = ctx.author.id
    # increase count for this user
    usage_count_yawn[user_id] = usage_count_yawn.get(user_id, 0) + 1

    count = usage_count_yawn[user_id]

    # default target is self

    #yawn logic here

    embed = Embed(title=f"{ctx.author.display_name} yawned!", description=f"{ctx.author.mention} has yawned {count} times", color=Color.teal())
    embed.set_image(random.choice(random_gifs_yawn))
    
    await ctx.send(embed=embed)

@bot.slash_command(name="yawn", description="Yawn!")
async def yawn(interaction: nextcord.Interaction):
    user_id = interaction.user.id

    # increase count for this user
    usage_count_yawn[user_id] = usage_count_yawn.get(user_id, 0) + 1
    count = usage_count_yawn[user_id]

    embed = Embed(title=f"{interaction.user.display_name} yawned!", description=f"{interaction.user.mention} has yawned {count} times", color=Color.teal())
    embed.set_image(random.choice(random_gifs_yawn))

    await interaction.response.send_message(embed=embed)

# ----------------------------------

@bot.command()
async def pentake(ctx):
    await ctx.send("HEY! JS TAKE THE PEN BRO")
    await ctx.send("https://i.postimg.cc/PqScSdgm/169-sin-titulo.jpg")

@bot.slash_command(name="pentake", description="till gives u a pen")
async def pentake_slash(interaction: nextcord.Interaction):
    await interaction.response.send_message("HEY! JS TAKE THE PEN BRO") 
    await interaction.followup.send("https://i.postimg.cc/PqScSdgm/169-sin-titulo.jpg")

# ----------------------------------

@bot.command()
async def keybtake(ctx):
    await ctx.send("HEY! JS TAKE THE KEYBOARD BRO")
    await ctx.send("https://i.postimg.cc/rpfbfqBR/169-sin-titulo-1.jpg")

@bot.slash_command(name="keybtake", description="till gives u a keyboard")
async def keybtake_slash(interaction: nextcord.Interaction):
    await interaction.response.send_message("HEY! JS TAKE THE KEYBOARD BRO")
    await interaction.followup.send("https://i.postimg.cc/rpfbfqBR/169-sin-titulo-1.jpg")

# ----------------------------------
#stored embeds
custom_embeds = {}

#set retrievable embed
@bot.command()
async def setembed(ctx, name: str, title: str, description: str, color: int, image_url: str):

    embed = nextcord.Embed(title=title, description=description, color=color)
    embed.set_image(url=image_url)

    custom_embeds[name] = embed

    await ctx.send(embed=embed)
    await ctx.send(f"Embed saved as {name}! You can retrieve it later.")
    
# slash command version
@bot.slash_command(name="setembed", description="Set a retrievable embed")
async def setembed_slash(interaction: nextcord.Interaction, name: str, title: str, description: str, color: int, image_url: str):

    embed = nextcord.Embed(title=title, description=description, color=color)
    embed.set_image(url=image_url)

    custom_embeds[name] = embed

    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(f"Embed saved as {name}! You can retrieve it later.")

# ----------------------------------

#retrieve stored embed
@bot.command()
async def getembed(ctx, name: str):
    embed = custom_embeds.get(name)
    if embed:
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No embed found with the name '{name}'.")

@bot.slash_command(name="getembed", description="Get a stored embed")
async def getembed_slash(interaction: nextcord.Interaction, name: str):
    embed = custom_embeds.get(name)
    if embed:
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"No embed found with the name '{name}'.")

# ----------------------------------

@bot.command(name='takebutton')
async def takebutton(ctx):
    hi = Button(label="click", style=ButtonStyle.primary)

    async def hi_callback(interaction):
        await interaction.response.send_message("you clicked the siwwy button!")

    hi.callback = hi_callback

    myview = View(timeout=180)
    myview.add_item(hi)

    await ctx.send("Click the button!!!", view=myview)

@bot.slash_command(name="takebutton", description="button")
async def takebutton_slash(interaction: nextcord.Interaction):
    hi = Button(label="click", style=ButtonStyle.primary)

    async def hi_callback_slash(interaction):
        await interaction.response.send_message("you clicked the siwwy button!")

    hi.callback = hi_callback_slash

    myview = View(timeout=180)
    myview.add_item(hi)

    await interaction.response.send_message("hi", view=myview)

# ----------------------------------

@bot.command()
async def blorb(ctx):
    await ctx.send("blorb blorb 👽")

@bot.slash_command(name="blorb", description="blorb 👽")
async def blorb_slash(interaction: nextcord.Interaction):
    await interaction.response.send_message("blorb blorb 👽")

# ----------------------------------

@bot.command()
async def ivantill(ctx):
    embed = nextcord.Embed(title="<3", description="thank you for being the victim of my shallow emotions",color=0x000000).set_image(url="https://files.catbox.moe/fwu0ap.gif")
    await ctx.send(embed=embed)

@bot.slash_command(name="ivantill", description="basic ivti")
async def ivantill_slash(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="<3", description="thank you for being the victim of my shallow emotions",color=0x000000).set_image(url="https://files.catbox.moe/fwu0ap.gif")
    await interaction.response.send_message(embed=embed)

# ----------------------------------

#embed a video from computer files
@bot.command()
async def light(ctx):
    img = File(r"C:\Users\Usuario\Desktop\all\till\light.mp4")
    await ctx.send(file=img)

@bot.slash_command(name="light", description="light video")
async def light_slash(interaction: nextcord.Interaction):
    img = File(r"C:\Users\Usuario\Desktop\all\till\light.mp4")
    await interaction.response.send_message(file=img)

# -----------------------------------

@bot.command()
async def speed(ctx):
    await ctx.send("https://files.catbox.moe/an25jf.gif")

@bot.slash_command(name="speed", description="speed dont laugh")
async def speed_slash(interaction: nextcord.Interaction):
    await interaction.response.send_message("https://files.catbox.moe/an25jf.gif")

#------------------------------------

@bot.command()
async def reminder(ctx):
    await ctx.send(f"halo {ctx.author.mention}!! please remember to smile everyday and help other people smile too!")

@bot.slash_command(name="reminder", description="tiny reminder")
async def reminder_slash(interaction: nextcord.Interaction):
    await interaction.response.send_message(f"halo {interaction.user.mention}!! please remember to smile everyday and help other people smile too!")
# -----------------------------------

@bot.command()
async def love(ctx):
    embed = nextcord.Embed(title="yay! gracias", description=f"Yo también te amo mucho {ctx.author.display_name} <3", color=0x323337)
    embed.set_image(url="https://files.catbox.moe/rcz217.gif")
    await ctx.send(embed=embed)

@bot.slash_command(name="love", description="love hehe")
async def love_slash(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="yay! gracias", description=f"Yo también te amo mucho {interaction.user.display_name} <3", color=0x323337)
    embed.set_image(url="https://files.catbox.moe/rcz217.gif")
    await interaction.response.send_message(embed=embed)

# -----------------------------------

@bot.command()
async def alarm(ctx, minutes: int, hours: int, msg: str):
    now=datetime.datetime.now()
    then=now+timedelta(hours=hours, minutes=minutes)
    await ctx.send(f"Alarm set for {then.strftime('%H:%M')} with message: {msg}")
    await asyncio.sleep(hours * 3600 + minutes * 60)
    await ctx.send(f"{ctx.author.mention} Alarm ringing! It's {then.strftime('%H:%M')}, your message: {msg}")
    await ctx.send("https://files.catbox.moe/hjyi24.gif")

@bot.slash_command(name="alarm", description="set an alarm")
async def alarm_slash(interaction: nextcord.Interaction, minutes: int, hours: int, msg: str):
    now=datetime.datetime.now()
    then=now+timedelta(hours=hours, minutes=minutes)
    channel = interaction.channel
    await interaction.response.send_message(f"Alarm set for {then.strftime('%H:%M')} with message: {msg}")
    await asyncio.sleep(hours * 3600 + minutes * 60)
    await channel.send(f"{interaction.user.mention} Alarm ringing! It's {then.strftime('%H:%M')}, your message: {msg}")
    await channel.send("https://files.catbox.moe/hjyi24.gif")

# -----------------------------------

#till speak bubble with prompted text
@bot.command()
async def tillimgtxt(ctx, *args):
    text = ' '.join(args)
    font = ImageFont.truetype("arial.ttf", 30)
    img = Image.open(r"C:\Users\Usuario\Desktop\all\till\tillspeak.png")
    cx,  cy = (685, 120)
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    lines = textwrap.wrap(text, width=30)
    yoffset = (h * len(lines))/2
    ytext = cy-(h/2) - yoffset/2

    for line in lines:
        draw = ImageDraw.Draw(img)
        bboxl = font.getbbox(line)
        w = bboxl[2] - bboxl[0]
        h = bboxl[3] - bboxl[1]
        draw.text((cx - (w/ 2), ytext), line, (0, 0, 0), font=font)
        img.save(r"C:\Users\Usuario\Desktop\all\till\tillspoke.png")
        ytext += h

    with open(r"C:\Users\Usuario\Desktop\all\till\tillspoke.png", "rb") as f:
        img = File(f)
        await ctx.send(file=img)

@bot.slash_command(name="tillimgtxt", description="till speak bubble with text")
async def tillimgtxt_slash(interaction: nextcord.Interaction, text: str):
    font = ImageFont.truetype("arial.ttf", 30)
    img = Image.open(r"C:\Users\Usuario\Desktop\all\till\tillspeak.png")
    cx,  cy = (685, 120)
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    lines = textwrap.wrap(text, width=30)
    yoffset = (h * len(lines))/2
    ytext = cy-(h/2) - yoffset/2

    for line in lines:
        draw = ImageDraw.Draw(img)
        bboxl = font.getbbox(line)
        w = bboxl[2] - bboxl[0]
        h = bboxl[3] - bboxl[1]
        draw.text((cx - (w/ 2), ytext), line, (0, 0, 0), font=font)
        img.save(r"C:\Users\Usuario\Desktop\all\till\tillspoke.png")
        ytext += h

    with open(r"C:\Users\Usuario\Desktop\all\till\tillspoke.png", "rb") as f:
        img = File(f)
        await interaction.response.send_message(file=img)

# -----------------------------------

#bot quotes a replied existing text in till speak bubble 
@bot.command()
async def tillimgquote(ctx):
    if ctx.message.reference is None:
        await ctx.send("Please reply to a message to quote it.")
        return
    
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    text = message.content
    font = ImageFont.truetype("arial.ttf", 30)
    img = Image.open(r"C:\Users\Usuario\Desktop\all\till\tillspeak.png")
    cx,  cy = (685, 120)
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    lines = textwrap.wrap(text, width=30)
    yoffset = (h * len(lines))/2
    ytext = cy-(h/2) - yoffset/2

    for line in lines:
        draw = ImageDraw.Draw(img)
        bboxl = font.getbbox(line)
        w = bboxl[2] - bboxl[0]
        h = bboxl[3] - bboxl[1]
        draw.text((cx - (w/ 2), ytext), line, (0, 0, 0), font=font)
        img.save(r"C:\Users\Usuario\Desktop\all\till\tillspoke.png")
        ytext += h

    with open(r"C:\Users\Usuario\Desktop\all\till\tillspoke.png", "rb") as f:
        img = File(f)
        await ctx.send(file=img)


# -----------------------------------

lyrics = [
"""허락해줘 네 손 끝까지
허락해줘 네 발 끝까지
네 눈에 날 녹여주길
널 놓치고 싶지 않아
부디 내게 상처를 내줘
부디 날 아프게 해줘
내가 한 방울도 안 남을 때까지
너로 물들여""",
"""검붉은 공기는
우리를 감싸안고
맘을 일으키고
뜨거운 이 전율은
하늘 끝까지 퍼져나가""",
"""그날 쥐어준 칼끝에 빛은 올라타
발끝 새로 자란 풀들, 네 공기를 들이마셔 (Oh)
흩어질수록 차갑게 피는 rue
그래 난 너를 읽어본다""",
"""이게 아름다운 노래라는데
다들 팔 벌려 좋아하는데도
수많은 spotlight 보다 원해 너
내 빛은 너로부터 태어나"""
]

lyricstitle = ["CURE", "Blink Gone", "Scars", "Mi Vida Loca"]

lyricimages = [
    "https://i.postimg.cc/KzLK3sWX/ivantill-alien-stage.gif",
    "https://i.postimg.cc/nz8rxGhK/alien-stage-luka.gif",
    "https://i.postimg.cc/ZRq9hqBy/ivan-alien-stage-ivan.gif",
    "https://i.postimg.cc/526fBkYG/mi-vida-loca-alien-stage.gif"
]

@bot.command()
async def randomlyrics(ctx):
    choice = random.randint(0, len(lyrics)-1)
    embed = nextcord.Embed(title=f"Here's your lyrics! You got {lyricstitle[choice]}!!", description=lyrics[choice], color=0x131416)
    embed.set_image(url=lyricimages[choice])
    await ctx.send(embed=embed)    
    
@bot.slash_command(name="randomlyrics", description="random till lyrics")
async def randomlyrics_slash(interaction: nextcord.Interaction):
    choice = random.randint(0, len(lyrics)-1)
    embed = nextcord.Embed(title=f"Here's your lyrics! You got {lyricstitle[choice]}!!", description=lyrics[choice], color=0x131416)
    embed.set_image(url=lyricimages[choice])
    await interaction.response.send_message(embed=embed)


# -----------------------------------

#bot manda un mensaje a las 6am cada dia
async def daily_message():
    await bot.wait_until_ready()
    channel = bot.get_channel(1387258797701070918)  # replace with your channel ID
    while not bot.is_closed():
        now = datetime.datetime.now()
        target = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now > target:
            target += datetime.timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        await channel.send("Good morning! You guys should wake up already >:P!!!")

        #answers to message sent after daily message
        def check(msg):
            return msg.channel == channel and msg.author != bot.user and msg.content.lower() in ["good morning till", "gm till", "morning till", "gm"]
        try:
            msg = await bot.wait_for('message', check=check, timeout=3600) # wait for 1 hour
            await channel.send(f"Good morning {msg.author.mention}! Have a great day! 💚")
        except asyncio.TimeoutError:
            await channel.send("Looks like no one responded... Hope you all have a great day anyway! 💚")

            #meaning of content.lower() in check:
            #this checks if the message content is one of the specified greetings, ignoring case sensitivity.
            #meaning of in in check:
            #the in operator checks if the content of the message is present in the provided list of greetings.

bot.loop.create_task(daily_message())



# -----------------------------------

bot.run(TOKEN)
