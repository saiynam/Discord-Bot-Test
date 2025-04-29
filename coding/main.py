import discord
from discord.ext import commands
import os
import json
import random
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
    level = int((xp / 42) ** 0.55)
    return level        #   100 xp = 1 level


@bot.event
async def on_ready():
    print(f'bot is online')

@bot.event
async def on_message(message):
    if not message.guild:
        return

    if message.author.bot :
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

    user_id = str(message.author.id)
    user_data = xp_data.get(user_id, {"xp": 0})
    user_data["xp"] += 10
    xp_data[user_id] = user_data

    new_xp = xp_data[user_id]["xp"]
    new_level = get_level(new_xp)

    guild = message.guild
    member = message.author

    #   ຕວດສອບວ່າ user ຄວນໄດ້ຮັບ Role ໃຫມ່ຫຼືບໍ່

    if new_level in LEVEL_ROLE:
        new_role_id = LEVEL_ROLE[new_level]
        new_role = guild.get_role(new_role_id)

        if new_role not in member.roles :

            #   ບ່ອນນີ້ແລ ລົບ ເກົ່າທັ້ງໝົດທີ່ໄດ້ຈາກ LEVEL_ROLE
            for lvl, rid in LEVEL_ROLE.items():
                role = guild.get_role(rid)

                if role in member.roles:
                    await member.remove_roles(role)

            #   ບ່ອນນີ້ມອບ Role ໃໝ່
            await member.add_roles(new_role)
            await message.channel.send(f"{member.mention} ขึ้นเลเวล {new_level} แล้ว! ได้รับการเลื่อนตำแหน่งเป็น {new_role.name}" )
    save_xp()
    await bot.process_commands(message)


@bot.command()
async def top(ctx) :
    sorted_users = sorted(xp_data.items(), key=lambda x: x[1]['xp'], reverse=True)  
    top_n = 5
    
    embed = discord.Embed(
        title = "🏆 อันดับ XP สูงสุด",
        description = "ใครจะเป็นสุดยอด พนักงาน กันนะ",
        color = discord.Color.gold()
    )

    medals = ["🥇", "🥈", "🥉"]
    for idx, (user_id, user_info) in enumerate(sorted_users[:top_n], start = 1):
        member = ctx.guild.get_member(int(user_id))
        name = member.display_name if member else "ไม่พบพนักงาน"
        xp = user_info["xp"]

        if idx <= 3:
            rank = medals[idx - 1]
        else:
            rank = f"{idx}."
        
        embed.add_field(
            name = f"{rank} {name}",
            value = f"{xp} XP",
            inline = False
        )
    embed.set_footer(text = f"จัดอันดับโดย{bot.user.name}", icon_url = bot.user.display_avatar.url)
    await ctx.send(embed = embed)

@bot.command()
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    user_id = str(member.id)
    user_data = xp_data.get(user_id, {"xp": 0})
    xp = user_data["xp"]
    level = get_level(xp)

    if level >= 50:
        color = discord.Color.dark_purple()
        job_class = "เทพนักรบมังกร"
        rank_emoji = "🐉"
    elif level >= 30:
        color = discord.Color.gold()
        job_class = "จอมเวทย์"
        rank_emoji = "🪄"
    elif level >= 15:
        color = discord.Color.green()
        job_class = "นักธนู"
        rank_emoji = "🏹"
    else:
        color = discord.Color.blue()
        job_class = "นักผจญภัยฝึกหัด"
        rank_emoji = "⚔️"

    embed = discord.Embed(
        title=f"{rank_emoji} โปรไฟล์ของ {member.display_name}",
        description=(
            f"**เลเวล:** {level}\n"
            f"**XP:** {xp}\n"
            f"**คลาส:** `{job_class}`\n"
        ),
        color=color
    )

    roles = [role for role in member.roles if role.name != "@everyone"]
    if roles:
        embed.add_field(name="บทบาทในบริษัท", value=roles[-1].name, inline=True)

    weapon_list = ["ปีน", "ธนู", "หอก", "จี่หนัง", "คัมภีร์ปกหนังหมา"]
    embed.add_field(name="อาวุธหลัก", value=random.choice(weapon_list), inline=True)

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"นักผจญภัยโดย {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)


bot.run(TOKEN)