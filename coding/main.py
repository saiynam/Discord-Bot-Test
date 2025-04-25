import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents = intents)

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