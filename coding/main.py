import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents = intents)

XP_FILE = "xp_data.json"

if os.path.exists(XP_FILE):
    with open(XP_FILE, "r") as f:
        xp_data = json.load(f)
    
else:
    xp_data = {}

#   ຕັ້ງບົດບາດບ່ອນີ້

LEVEL_ROLE = {
    1 : 1362824931124969472 , # Role ID ສຳລັບເວລ 1
    15 : 1362826484154106209 , # Role ID ສຳລັບເວລ 15
    20 : 1362826576345174036 , # Role ID ສຳລັບເວລ 20
    40 : 1362826944411861002 , # Role ID ສຳລັບເວລ 40
    50 : 1362827025361928282 , # Role ID ສຳລັບເວລ 50
}

def save_xp():
    with open(XP_FILE, "w") as f :
        json.dump(xp_data, f)

def get_level(xp):
    return xp // 100        #   100 xp = 1 level


@bot.event
async def on_ready():
    print(f'bot is online')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    target_channel_id = 1362848549326553229
    target_channel = bot.get_channel(target_channel_id)

    if not target_channel:
        print("not target")
        return

    if message.channel.id != target_channel_id:
        return
    messageInput = message.content.lower()

    if "hello" in messageInput:
        await target_channel.send(f"hi it'me {bot.user.name}")

    elif "bye" in messageInput:
        await target_channel.send("see you agian")

    else:
        await target_channel.send("i don't know")

    await bot.process_commands(message)
    print(messageInput)




bot.run(TOKEN)