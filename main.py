import discord
import os  
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import random
import datetime

load_dotenv()

# --- SETUP BOT ---
class ItsukiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash commands (/) berhasil di-sync!")

bot = ItsukiBot()

# --- DATA ---
ROAST_LIST = [
    "Muka lu kayak gorengan dingin, berminyak tapi gak ada yang mau.",
    "Lu tuh beban keluarga apa beban server sih?",
    "Belajar sana! Jangan main Discord mulu, nilai lu ancur kan?",
    "Dih, bau bawang. Mandi sana woi!",
    "Otak lu loadingnya lebih lama dari internet Explorer ya?",
    "Gua laper, dan liat lu bikin gua makin emosi.",
]

GIFS = {
    "slap": "https://media.tenor.com/XiYuU9h44-AAAAAC/anime-slap-mad.gif",
    "hug": "https://media.tenor.com/kCZjTqCKIGAAAAAC/hug-anime.gif",
    "pat": "https://media.tenor.com/E6fMkQRZBdIAAAAC/k-on-azu-nyan.gif",
    "scold": "https://media.tenor.com/bK-Dy-sHkC8AAAAC/anime-scold.gif",
    "angry": "https://media.tenor.com/pG0y1uKjQPAAAAAC/itsuki-nakano-pout.gif"
}

# --- EVENT ---
@bot.event
async def on_ready():
    print(f'🤖 {bot.user} (Nakano Itsuki) Online!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Kamu Makan"))

# ==========================================
# 🔥 TEKNIK ANTI-TIMEOUT (DEFER + FOLLOWUP)
# ==========================================

# --- 1. ROAST ME ---
@bot.tree.command(name="roast", description="Minta di-roast sama Itsuki")
async def roast(interaction: discord.Interaction, user: discord.Member = None):
    # STEP 1: Minta waktu (biar ga timeout 3 detik)
    await interaction.response.defer() 
    
    target = user if user else interaction.user
    hinaan = random.choice(ROAST_LIST)
    
    embed = discord.Embed(title="🔥 ROASTED!", description=f"{target.mention}, {hinaan}", color=discord.Color.red())
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.set_footer(text="Jangan baper ya, cuma bot kok.")
    
    # STEP 2: Pakai 'followup.send' (bukan response.send_message lagi)
    await interaction.followup.send(embed=embed)

# --- 2. SHIP ---
@bot.tree.command(name="ship", description="Cek kecocokan cinta")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    await interaction.response.defer() # <--- PENTING

    score = random.randint(0, 100)
    
    if score < 20:
        status = "💔 Gak banget. Mending jauhan."
        color = discord.Color.dark_gray()
    elif score < 50:
        status = "😐 Yah... temenan aja deh."
        color = discord.Color.orange()
    elif score < 80:
        status = "❤️ Lumayan cocok! Gasss!"
        color = discord.Color.pink()
    else:
        status = "💍 DEFINISI JODOH! NIKAH KAPAN?!"
        color = discord.Color.fuchsia()

    bar_full = int(score / 10)
    progress_bar = "[" + ("█" * bar_full) + ("-" * (10 - bar_full)) + "]"

    embed = discord.Embed(title="💘 Love Calculator", color=color)
    embed.add_field(name="Pasangan", value=f"{user1.mention} x {user2.mention}", inline=False)
    embed.add_field(name="Score", value=f"**{score}%** {progress_bar}", inline=False)
    embed.add_field(name="Komentar Itsuki", value=status, inline=False)
    
    await interaction.followup.send(embed=embed) # <--- FOLLOWUP

# --- 3. ACTION (Hug, Slap, dll) ---
async def send_action(interaction, target, text_template, gif_key):
    # Kita defer di dalam helper function ini
    await interaction.response.defer()

    embed = discord.Embed(description=text_template.format(user=interaction.user.mention, target=target.mention), color=discord.Color.blue())
    embed.set_image(url=GIFS[gif_key])
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="hug", description="Peluk seseorang")
async def hug(interaction: discord.Interaction, user: discord.Member):
    await send_action(interaction, user, "{user} memeluk {target} dengan erat! 🤗", "hug")

@bot.tree.command(name="slap", description="Gampar seseorang")
async def slap(interaction: discord.Interaction, user: discord.Member):
    await send_action(interaction, user, "{user} menampar {target}! PLAK! 👋", "slap")

@bot.tree.command(name="pat", description="Elus kepala seseorang")
async def pat(interaction: discord.Interaction, user: discord.Member):
    await send_action(interaction, user, "{user} mengelus kepala {target}. Good boy/girl. 😺", "pat")

@bot.tree.command(name="scold", description="Marahin seseorang")
async def scold(interaction: discord.Interaction, user: discord.Member):
    await send_action(interaction, user, "{user} memarahi {target}! Jangan nakal dong! 💢", "scold")

# --- 4. MOOD ---
@bot.tree.command(name="mood", description="Cek mood Itsuki hari ini")
async def mood(interaction: discord.Interaction):
    await interaction.response.defer() # <--- PENTING

    moods = [
        ("Laper banget 🍔", "Bagi duit dong buat beli meatbun.", discord.Color.orange()),
        ("Seneng 😊", "Nilai ujianku bagus hari ini!", discord.Color.green()),
        ("Marah 😡", "Siapa yang ngabisin pudding di kulkas?!", discord.Color.red()),
        ("Ngantuk 😴", "Jangan ganggu, mau bobo.", discord.Color.blue()),
    ]
    current_mood = random.choice(moods)
    
    embed = discord.Embed(title=f"Mood Itsuki: {current_mood[0]}", description=current_mood[1], color=current_mood[2])
    if "Marah" in current_mood[0]:
        embed.set_image(url=GIFS["angry"])
        
    await interaction.followup.send(embed=embed)

bot.run(os.getenv('DISCORD_TOKEN'))