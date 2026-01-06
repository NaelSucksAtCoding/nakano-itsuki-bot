import discord
from discord.ext import commands

# Settingan dasar
intents = discord.Intents.default()
intents.message_content = True # Wajib biar bisa baca chat

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Hoi! {bot.user} (Nakano Itsuki) udah bangun dan siap makan!')
    # Ganti status bot jadi "Watching..."
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Menu Makanan"))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! Makan bang? 🍔')

# JANGAN UPLOAD TOKEN KE GITHUB (Nanti gua ajarin cara amaninnya)
# Sementara tempel token lu di sini buat ngetes doang:
bot.run('TOKEN DIHAPUS DULU')