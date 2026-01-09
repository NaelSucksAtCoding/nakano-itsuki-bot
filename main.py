import discord
import os
import random
import asyncio
import database
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

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

@bot.tree.error
async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.TransformerError):
        await interaction.response.send_message(
            f"❌ **Error:** User gak ketemu bro. Pastikan lu pilih user dari list yang muncul, jangan ketik manual doang.", 
            ephemeral=True
        )
    else:
        print(f"⚠️ Error lain: {error}")

# --- DATA (DARI KODE PERTAMA - TIDAK DIUBAH) ---
ROAST_LIST = [
    "Muka lu kayak gorengan dingin, berminyak tapi gak ada yang mau.",
    "Lu tuh beban keluarga apa beban server sih?",
    "Belajar sana! Jangan main Discord mulu, nilai lu ancur kan?",
    "Dih, bau bawang. Mandi sana woi!",
    "Otak lu loadingnya lebih lama dari Internet Explorer ya?",
    "Gua laper, dan liat lu bikin gua makin emosi.",
    "Ngaku programmer, tapi kalo AI down langsung bingung mau ngetik apa.",
    "Coding sekarang skill utamanya bukan logika, tapi nanya prompt yang bener.",
    "Error dikit langsung ke AI, mikir sendiri? Nanti aja.",
    "AI lu mati, confidence ikut mati.",
    "Katanya belajar ngoding, tapi yang hafal malah prompt AI.",
    "Merantau katanya biar mandiri, nyatanya mandiri cuma pas nangis sendirian.",
    "Datang jauh-jauh buat masa depan, tapi masa depan gak keliatan, Indomie keliatan terus.",
    "Merantau demi mimpi, tapi mimpi kalah sama cicilan dan uang kos.",
    "Di chat keluarga bilang aman, padahal lagi mikir besok makan apa.",
    "Hidup jauh dari orang tua bikin kuat, tapi bikin mental babak belur juga.",
]

GIFS = {
    "slap": [
        "https://media.tenor.com/XiYuU9h44-AAAAAC/anime-slap-mad.gif",
        "https://i.pinimg.com/originals/b6/d8/a8/b6d8a83eb652a30b95e87cf96a21e007.gif",
        "https://i.pinimg.com/originals/71/a5/1c/71a51cd5b7a3e372522b5011bdf40102.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjI5cmR4NDV0bnl1MW83Y3Roamk2cWxuYjZkanJ2cTE0ZWp4YzlreiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4R6EMXhNPz5WsJFEta/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExeWNmdHd1OTE4NTNmNG0wbHdrMDlqaGhlNnI2ZWF4ajMxNnlwdzY2aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZkiIapyGO0u6Q/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbTJ3bWplYTd4NWhlcGM4dzFyenNqeHB1ODRlZ3pwbnBuMTVoNGwzcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xUNd9HZq1itMkiK652/giphy.gif",
        "https://i.giphy.com/ylqr4JvFaZqnK.webp",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTNpa2xqZzBmZHA0a3FiNnY0d2Y4MHgxZGZsNDEwb3pma2hyYTRqaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/OzNvVsI8RMRuGqNYs1/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXA3dWxybTU5YWFlNnB3MTUzd200endtYjZmMWo4ajVmcmRtOWQyNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KHUKLyPtuteJWPJreE/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOG5hMmtzbHZnMGl5Yno3cTNyYmxjZW1rYjVuN2M4eWU1NzI1M3ZlZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/viFrrkC1qSY5fJhFn6/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTRiNmRjZGlwYWRwYzN3Z29ra3hzbWZqNmgwbzNkcnB5ZmlzcWM0cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZH3GaEibzDntlcq3mA/giphy.gif",
        "https://i.imgur.com/RFWNaoF.gif"
    ],
    "hug": [
        "https://media.tenor.com/kCZjTqCKIGAAAAAC/hug-anime.gif",
        "https://media.tenor.com/X5nBjx9G_HsAAAAC/anime-hug.gif",
        "https://media.tenor.com/J7eGDvGeP9IAAAAC/hug-cuddle.gif"
    ],
    "pat": [
        "https://media.tenor.com/E6fMkQRZBdIAAAAC/k-on-azu-nyan.gif",
        "https://media.tenor.com/Y7B6npa9mXcAAAAC/pat-head.gif"
    ],
    "scold": [
        "https://media.tenor.com/bK-Dy-sHkC8AAAAC/anime-scold.gif"
    ],
    "angry": [
        "https://media.tenor.com/j0URHc6S_PYAAAAM/i-dont-like-him-the-quintessential-quintuplets.gif"
    ]
}

# ==========================================
# 🔘 KELAS BUTTON (FITUR BARU)
# ==========================================

# 1. VIEW UNTUK ROASTING
class RoastView(View):
    def __init__(self, target_user):
        super().__init__(timeout=60) # Tombol mati setelah 60 detik
        self.target_user = target_user
        self.click_counts = {}
    
    # Fungsi pengecekan limit klik (Maksimal 6x)
    async def check_limit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        current_clicks = self.click_counts.get(user_id, 0)
        
        if current_clicks >= 6:
            await interaction.response.send_message("Woi udah! Jari lu gak capek apa?", ephemeral=True)
            return False # Stop, gak boleh lanjut
        
        self.click_counts[user_id] = current_clicks + 1
        return True # Lanjut

    @discord.ui.button(label="Roast Lagi 🔥", style=discord.ButtonStyle.danger)
    async def roast_again(self, interaction: discord.Interaction, button: Button):
        if not await self.check_limit(interaction): return

        hinaan = random.choice(ROAST_LIST)
        await interaction.response.send_message(f"{self.target_user.mention}, belum puas? **{hinaan}**")

    @discord.ui.button(label="Baper 😭", style=discord.ButtonStyle.secondary)
    async def cry(self, interaction: discord.Interaction, button: Button):
        if not await self.check_limit(interaction): return

        # Update: Tambah 5 kalimat baru
        responses = [
            f"Dih, {interaction.user.name} cengeng banget. Gitu doang nangis.",
            "Yah, mental kerupuk. Baru gitu aja udah mewek.",
            "Tisu mana tisu? Banjir nih server gara-gara lu.",
            "Cup cup cup... Kasian banget sih, mau dipanggilin mama?",
            "Udah gede jangan baperan gitu dong.",
            "Halah drama. Paling besok juga lupa."
        ]
        await interaction.response.send_message(random.choice(responses), ephemeral=True)

    @discord.ui.button(label="Balas 💢", style=discord.ButtonStyle.primary)
    async def counter(self, interaction: discord.Interaction, button: Button):
        if not await self.check_limit(interaction): return

        replies = [
            "Berani juga lu jawab ya?!",
            "Halah, berisik lu. Awas ya nanti!",
            "Waduh, si beban mulai ngelawan gaes.",
            "Nyali lu gede juga ye.",
            "Bodo amat, gak denger. Wleee 😜"
        ]
        # Update: Hapus prefix "Itsuki:" biar langsung teks aja
        await interaction.response.send_message(random.choice(replies))

# 2. VIEW UNTUK SHIP CHAOS
class ShipView(View):
    def __init__(self, score): # Kita butuh data Score di sini
        super().__init__(timeout=60)
        self.score = score
        self.click_counts = {}

    async def check_limit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        current_clicks = self.click_counts.get(user_id, 0)
        if current_clicks >= 6:
            await interaction.response.send_message("Buset, tombolnya mau dijebolin? Udah woi, max 6x!", ephemeral=True)
            return False
        self.click_counts[user_id] = current_clicks + 1
        return True

    # Helper untuk milih respon berdasarkan rasio score (4 roast : 1 beneran, dst)
    def get_weighted_response(self, roast_pool, real_pool):
        # Tentukan bobot (weights) berdasarkan range score
        if self.score <= 25:
            # 0-25: 4 Roast, 1 Beneran (80% Roast)
            population = [roast_pool, real_pool]
            weights = [80, 20]
        elif self.score <= 50:
            # 26-50: 3 Roast, 2 Beneran (60% Roast)
            population = [roast_pool, real_pool]
            weights = [60, 40]
        elif self.score <= 75:
            # 51-75: 2 Roast, 3 Beneran (40% Roast)
            population = [roast_pool, real_pool]
            weights = [40, 60]
        else:
            # 76-100: 1 Roast, 4 Beneran (20% Roast)
            population = [roast_pool, real_pool]
            weights = [20, 80]
            
        # Pilih pool mana yang dipake
        selected_pool = random.choices(population, weights=weights, k=1)[0]
        return random.choice(selected_pool)

    @discord.ui.button(label="Nikahin 💍", style=discord.ButtonStyle.success)
    async def marry(self, interaction: discord.Interaction, button: Button):
        if not await self.check_limit(interaction): return

        roast_responses = [
            "Yakin nikah? Mending pikir-pikir lagi deh, suram kayaknya.",
            "Hah? Nikah? Sama dia? Mata lu sehat kan?",
            "Jangan deh, kasian keturunan lu nanti.",
            "Dih, selera lu rendah banget asli.",
            "Red flag berjalan gitu mau dinikahin? Gws deh."
        ]
        real_responses = [
            "Gas! Gue tunggu undangannya ya!",
            "Cocok banget emang, semoga samawa ya!",
            "Setuju! Pasangan ter-uwu satu server.",
            "Langsung KUA aja bro, kelamaan pacaran."
        ]
        
        reply = self.get_weighted_response(roast_responses, real_responses)
        await interaction.response.send_message(reply)

    @discord.ui.button(label="Putusin 💔", style=discord.ButtonStyle.danger)
    async def breakup(self, interaction: discord.Interaction, button: Button):
        if not await self.check_limit(interaction): return

        # Kalau putusin: Roast = Nyela keputusan putus (Sarkas/Jahat), Real = Mendukung putus
        roast_responses = [
            "Dih, mutusin anak orang sembarangan. Karma is real loh.",
            "Sok laku banget lu minta putus.",
            "Halah, paling besok juga ngemis balikan.",
            "Drama banget hidup lu, dikit-dikit putus.",
            "Lu nya aja yang baperan, padahal dia oke lho."
        ]
        real_responses = [
            "Bagus! Keputusan tepat, cari yang lebih cakep.",
            "Nah gitu dong, lu berhak bahagia tanpa dia.",
            "Setuju, mending jomblo daripada makan hati.",
            "Udah kuduga bakal putus, emang gak cocok dari awal."
        ]

        reply = self.get_weighted_response(roast_responses, real_responses)
        await interaction.response.send_message(reply)

    @discord.ui.button(label="Reroll (Cek Ulang) 🔄", style=discord.ButtonStyle.secondary)
    async def reroll(self, interaction: discord.Interaction, button: Button):
        if not await self.check_limit(interaction): return
        # Reroll ga perlu logic berat, just fun
        new_score = random.randint(0, 100)
        await interaction.response.send_message(f"Dih ngeyel. Oke gue cek lagi... Hasilnya: **{new_score}%**.", ephemeral=True)

# ==========================================
# 🤖 EVENT & COMMANDS
# ==========================================

@bot.event
async def on_ready():
    database.init_db()
    print(f'🤖 {bot.user} (Nakano Itsuki) Online!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ketik /mood untuk cek mood gue!"))

# --- FITUR MENTION REACTION (FITUR BARU) ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Kalau bot di-mention (ping)
    if bot.user.mentioned_in(message):
        content = message.content.lower()
        
        # Logika Tsundere
        if "makan" in content:
            await message.reply("Mana? Mana makanannya?! 🍔")
        else:
            pings = [
                "Apa sih ping-ping mulu? Ganggu orang makan aja.",
                "Hadir. Kenapa? Kangen?",
                "Berisik woi.",
                "Jangan spam atau Gue makan nih!"
            ]
            await message.channel.send(random.choice(pings))

    # PENTING: Biar command lain tetep jalan
    await bot.process_commands(message)

    msg = message.content.lower()

    # ========================================================
    # 1. WIBU & JEPANG (DIPINDAH KE ATAS BIAR GA BENTROK SAMA "AI")
    # ========================================================
    if "kawaii" in msg or "kawai" in msg or "gemoy" in msg:
        if random.randint(1, 100) <= 100:
             await message.reply("Be-berisik! (˶˃⤙˂˶)")

    elif "okaeri" in msg or "okairi" in msg:
        if random.randint(1, 100) <= 100:
             await message.reply("Tadaima... eh, ini server Discord woi, bukan rumah!")

    elif "master" in msg:
        if random.randint(1, 100) <= 100:
             await message.reply("Gue bukan maid ya! Jangan panggil master!")

    elif "omoshiroi" in msg:
        if random.randint(1, 100) <= 100:
             await message.reply("Nani yang omoshiroi? Wibu terdeteksi.")

    elif any(x in msg for x in ["anime", "manga", "waifu"]):
        if random.randint(1, 100) <= 100:
             await message.reply("Wibu bau bawang. Mandi sana! Waifu lu gepeng.")

    elif "isekai" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Mending lu isekai beneran sana biar ga balik.", "Kebanyakan nonton anime lu, sadar woi."]
            await message.reply(random.choice(replies))

    # ========================================================
    # 2. GENERAL CHAT (SEPI, LAPER, DLL)
    # ========================================================
    elif "sepi" in msg:
        if random.randint(1, 100) <= 100: 
            await message.reply("Kuburan kali ah sepi. Ramein dong!")
            
    elif "laper" in msg or "lapar" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Sama... bagi duit dong buat beli meatbun 🤤")
            
    elif "wkwk" in msg or "haha" in msg:
        if random.randint(1, 100) <= 100: 
            await message.reply("Ketawa lu jelek.")

    elif "pagi" in msg:
         if random.randint(1, 100) <= 100:
             await message.reply("Pagi juga. Jangan lupa sarapan.")

    # ========================================================
    # 3. KATA-KATA TAMBAHAN (REQUEST BARU)
    # ========================================================
    elif "sok asik" in msg or "so asik" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Kalo itu menurut lu sok asik, ya urusan lu.", "Gue gak minta perhatian siapa-siapa.", "Santai aja. Gue gak ada niat sok akrab."]
            await message.reply(random.choice(replies))

    elif "norak" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Gue gak peduli keliatan gimana di mata lu.", "Norak atau enggak, bukan urusan lu."]
            await message.reply(random.choice(replies))

    elif "cringe" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Lu gampang banget ngerasa cringe ya.", "Gue gak minta reaksi lebay dari lu."]
            await message.reply(random.choice(replies))

    elif "berisik" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Lu yang berisik! Ganggu orang makan aja.", "Santai, ini bukan ruang sunyi."]
            await message.reply(random.choice(replies))

    elif "ganggu" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Kalo keganggu, ya jangan nimbrung.", "Pergi sana, hush hush!"]
            await message.reply(random.choice(replies))

    elif "bacot" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Mulut lu tuh dijaga, bau tau.", "Berisik banget, kayak kaleng rombeng."]
            await message.reply(random.choice(replies))

    elif "diem" in msg or "diam" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Lu aja yang diem, bawel amat.", "Gak mau wleee 😜"]
            await message.reply(random.choice(replies))

    elif "rese" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Bodo amat, emang gue pikirin?", "Dih, sensian amat sih lu."]
            await message.reply(random.choice(replies))

    elif "nyebelin" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Makasih pujiannya.", "Emang tugas gue bikin lu kesel."]
            await message.reply(random.choice(replies))

    elif "copas" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Kreatif dikit napa, modal copas doang bangga.", "PLAGIAT TEROSS."]
            await message.reply(random.choice(replies))

    elif "error" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Bukan error, itu fitur rahasia.", "Jalan kok di gue."]
            await message.reply(random.choice(replies))

    elif "ngoding" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Ngoding terus, mandi kapan?", "Awas tipes bang, istirahat napa."]
            await message.reply(random.choice(replies))

    elif "deadline" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Mampus, siapa suruh nunda-nunda.", "Semangat ngerjainnya, jangan nangis ya."]
            await message.reply(random.choice(replies))

    elif "tugas" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Tugas mulu, kapan mainnya?", "Kerjain woi, jangan main Discord terus."]
            await message.reply(random.choice(replies))

    elif "revisi" in msg:
        if random.randint(1, 100) <= 100:
            replies = ["Turut berduka cita ya...", "Mampus, revisi lagi revisi lagi."]
            await message.reply(random.choice(replies))

    # ========================================================
    # 4. AI & CODING (DITARUH DISINI BIAR 'KAWAII' GA KEDETECT 'AI')
    # ========================================================
    elif "ai" in msg or "prompt" in msg:
        if random.randint(1, 100) <= 100: 
            roasts = [
                "AI mulu, otak dipake gak?",
                "Halah, paling copas prompt doang bangga.",
                "Ya kali coding cuma nyuruh-nyuruh AI doang… dipikirin dikit kek.",
                "Skill lu cuma sebatas prompt engineer ya?"
            ]
            await message.reply(random.choice(roasts))

    # ========================================================
    # 5. KATA GAUL & SINGKATAN (PRIORITAS TERAKHIR)
    # ========================================================
    elif any(x in msg for x in ["bro", "cuy", "coy", "gan"]):
        if random.randint(1, 100) <= 100:
            await message.reply("Apa sih manggil-manggil gitu… berisik tau")

    elif "lah" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Lah terus kenapa? Masalah?")

    elif "blom" in msg or "belom" in msg or "blum" in msg or "belum" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Lama banget sih. Keburu lumutan nih.")

    elif "bsk" in msg or "besok" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Besok makan apa ya... eh, maksudnya besok ngapain?")

    elif "td" in msg or "tadi" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Masa lalu ga usah dibahas.")

    elif "gokil" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("B aja sih menurut gue.")
    
    elif "wtf" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Heh! Mulutnya dijaga ya!")

    elif ":v" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Garing lu, muka pacman.")

    elif "gas" in msg or "lanjut" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Gas kemana? Kalo makan gue ikut.")

    elif "aman" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Yakin aman? Tugas lu udah kelar emang?")

    elif "nunggu" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Nunggu kepastian itu sakit kawan. Mending makan.")

    elif "tanya" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Bayar dulu kalo mau nanya.")

    elif "coba" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Gamau ah, mager.")

    elif "lomba" in msg or "panitia" in msg:
        if random.randint(1, 100) <= 100:
            await message.reply("Ada konsumsinya gak? Kalo snack-nya enak gue mau join dong.")

    # PENTING:
    await bot.process_commands(message)

# --- COMMANDS ---

# 1. ROAST (UPDATED DENGAN TOMBOL)
@bot.tree.command(name="roast", description="Roast user dengan tombol interaktif")
async def roast(interaction: discord.Interaction, user: discord.Member = None):
    await interaction.response.defer()
    target = user if user else interaction.user
    
    # Tetap pakai ROAST_LIST yang lu punya
    hinaan = random.choice(ROAST_LIST)
    embed = discord.Embed(title="🔥 ROASTED!", description=f"{target.mention}, {hinaan}", color=discord.Color.red())
    embed.set_thumbnail(url=target.display_avatar.url)
    
    # Attach View (Tombol)
    view = RoastView(target_user=target)
    await interaction.followup.send(embed=embed, view=view)

# 2. SHIP (UPDATED DENGAN TOMBOL)
@bot.tree.command(name="ship", description="Love calculator chaos mode")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    await interaction.response.defer()
    score = random.randint(0, 100)
    
    # Logic Status 4 Tingkatan
    if score <= 25:
        color = discord.Color.dark_gray()
        status = "💀 Suram. Mending anggep aja gak kenal."
    elif score <= 50:
        color = discord.Color.orange()
        status = "😐 Yah... sebatas 'kenal' doang sih oke."
    elif score <= 75:
        color = discord.Color.gold()
        status = "❤️ Lumayan lah, ada potensi jadi sesuatu."
    else:
        color = discord.Color.pink()
        status = "💍 DEFINISI JODOH! NIKAH KAPAN?!"

    bar_full = int(score / 10)
    progress_bar = "[" + ("█" * bar_full) + ("-" * (10 - bar_full)) + "]"

    embed = discord.Embed(title="💘 Love Calculator", color=color)
    embed.add_field(name="Pasangan", value=f"{user1.mention} x {user2.mention}", inline=False)
    embed.add_field(name="Score", value=f"**{score}%** {progress_bar}", inline=False)
    embed.add_field(name="Komentar Itsuki", value=status, inline=False)
    
    # PENTING: Masukkan variable 'score' ke dalam ShipView()
    view = ShipView(score=score) 
    await interaction.followup.send(embed=embed, view=view)

# 3. HELPER ACTION (TETAP ADA)
async def send_action(interaction, target, text_template, gif_key):
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        print("⚠️ Telat respon (Timeout), tapi gpp lanjut aja.")
    except Exception as e:
        print(f"⚠️ Error pas defer: {e}")

    list_gambar = GIFS.get(gif_key, [])
    
    if list_gambar:
        gambar_terpilih = random.choice(list_gambar)
        print(f"DEBUG: {gif_key} -> {gambar_terpilih}") 
    else:
        gambar_terpilih = None

    embed = discord.Embed(
        description=text_template.format(user=interaction.user.mention, target=target.mention), 
        color=discord.Color.blue()
    )
    
    if gambar_terpilih:
        embed.set_image(url=gambar_terpilih)

    await interaction.followup.send(embed=embed)

# 4. ACTION COMMANDS (TETAP ADA LENGKAP)
@bot.tree.command(name="hug", description="Peluk seseorang")
async def hug(interaction: discord.Interaction, user: discord.Member):
    await send_action(interaction, user, "{user} memeluk {target} dengan erat! 🤗", "hug")

@bot.tree.command(name="slap", description="Gampar seseorang")
async def slap(interaction: discord.Interaction, user: discord.Member):
    await send_action(interaction, user, "{user} menampar {target}! PLAK! 👋", "slap")

@bot.tree.command(name="pat", description="Elus kepala seseorang")
async def pat(interaction: discord.Interaction, user: discord.Member):
    await send_action(interaction, user, "{user} mengelus kepala {target}. Anak baik. 😺", "pat")

@bot.tree.command(name="scold", description="Marahin seseorang")
async def scold(interaction: discord.Interaction, user: discord.Member):
    await send_action(interaction, user, "{user} memarahi {target}! Jangan nakal dong! 💢", "scold")

# 5. MOOD (TETAP ADA)
@bot.tree.command(name="mood", description="Cek mood Itsuki hari ini")
async def mood(interaction: discord.Interaction):
    await interaction.response.defer()

    moods = [
    ("Lapar parah 🍔", "Asli, jangan singgung soal makanan dulu ya, gue belum makan dari pagi soalnya.", discord.Color.orange()),
    ("Serius & Fokus 📚", "Gue nggak telat, nggak cabut, terus tugas gue juga rapi. Ya emang udah harusnya gitu kan? Standar lah.", discord.Color.green()),
    ("Kesal 😡", "Woi, siapa yang main sikat aja makanan di kulkas nggak bilang-bilang? Mending ngaku deh sekarang!", discord.Color.red()),
    ("Gelisah 😣", "Santai, gue fine-fine aja kok. Udah nggak usah nanya lagi lo.", discord.Color.dark_teal()),
    ("Capek tapi Tahan 😴", "Gue cuma agak capek aja sih. Masih kuat kok... dikit lagi juga kelar.", discord.Color.blue()),
    ]
    current_mood = random.choice(moods)
    
    embed = discord.Embed(title=f"Mood Itsuki: {current_mood[0]}", description=current_mood[1], color=current_mood[2])
    
    if "Kesal" in current_mood[0]:
        list_angry = GIFS.get("angry")
        if list_angry:
            embed.set_image(url=random.choice(list_angry))
        
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="status", description="Cek status sosial dan reputasi kamu")
async def status(interaction: discord.Interaction, user: discord.Member = None):
    await interaction.response.defer()
    target = user if user else interaction.user
    
    # Ambil data dari database
    rep, title = database.get_user_data(target.id)
    
    # Tentukan warna embed berdasarkan reputasi
    if rep < 0: color = discord.Color.red()
    elif rep > 20: color = discord.Color.gold()
    else: color = discord.Color.blue()
    
    embed = discord.Embed(title=f"📜 Status: {target.name}", color=color)
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="Gelar", value=f"**{title}**", inline=False)
    embed.add_field(name="Reputasi", value=f"{rep} Poin", inline=False)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="puji", description="Puji orang (Nambah Reputasi)")
async def puji(interaction: discord.Interaction, user: discord.Member):
    if user.id == interaction.user.id:
        await interaction.response.send_message("Dih gila hormat, muji diri sendiri.", ephemeral=True)
        return
        
    await interaction.response.defer()
    
    # Tambah reputasi target +1
    new_rep = database.change_reputation(user.id, 1)
    
    pujian_list = [
        "Keren banget bang!", "Panutan server nih.", 
        "Ganteng/Cantik banget hari ini.", "Pro player lewat gaes."
    ]
    
    await interaction.followup.send(f"{interaction.user.mention} memuji {user.mention}: *\"{random.choice(pujian_list)}\"* \n(Reputasi {user.name} naik jadi {new_rep})")

@bot.tree.command(name="hina", description="Hina orang (Kurangi Reputasi)")
async def hina(interaction: discord.Interaction, user: discord.Member):
    if user.id == interaction.user.id:
        await interaction.response.send_message("Lagi cosplay jadi masokis?", ephemeral=True)
        return

    await interaction.response.defer()
    
    # Kurangi reputasi target -1
    new_rep = database.change_reputation(user.id, -1)
    
    hinaan_list = [
        "Bau bawang.", "Beban tim.", "Muka pas-pasan gaya selangit.", "NPC kocak."
    ]
    
    await interaction.followup.send(f"{interaction.user.mention} menghina {user.mention}: *\"{random.choice(hinaan_list)}\"* \n(Reputasi {user.name} turun jadi {new_rep})")

## COMPLAIN (Itsuki Ngeluh)
@bot.tree.command(name="complain", description="Itsuki lagi ngeluh. Jangan banyak tanya.")
async def complain(interaction: discord.Interaction):
    await interaction.response.defer()

    complains = [
        "Capek. Kalian ribut mulu dari tadi.",
        "Kenapa sih semua orang hari ini nyebelin?",
        "Laper… tapi males keluar.",
        "Gue pengen tenang sebentar. Bisa gak?",
        "Server rame tapi isinya bikin pusing.",
        "Bukan marah… cuma kesel aja.",
        "Hari ini gak ada yang beres.",
        "Gue butuh makan. Sekarang.",
        "Pengen meatbun, tapi duit abis.",
        "Jangan ganggu, lagi badmood."
    ]

    # Pake Embed biar rapi
    embed = discord.Embed(description=f"😒 **Itsuki:** {random.choice(complains)}", color=discord.Color.light_grey())
    await interaction.followup.send(embed=embed)

## CONFESS (Nembak Itsuki + GIF Blush)
@bot.tree.command(name="confess", description="Nyoba nembak Itsuki (resiko ditanggung sendiri)")
async def confess(interaction: discord.Interaction):
    await interaction.response.defer()

    responses = [
        "Hah?! Jangan ngaco!",
        "Ngapain sih tiba-tiba ngomong gitu!",
        "Gue gak bilang nolak… tapi juga gak nerima!",
        "Jangan GR dulu. Gue cuma kaget doang.",
        "B-bukan berarti gue seneng ya!",
        "Heh… ngomong gitu tuh bikin orang bingung tau.",
        "Lu tau gak sih timing?",
        "…… idiot."
    ]

    embed = discord.Embed(
        description=f"😳 **Itsuki:** {random.choice(responses)}", 
        color=discord.Color.brand_red()
    )
    
    # KITA SAMBUNG KE GIF BLUSH YANG UDAH ADA DI FITUR SEBELUMNYA
    if "blush" in GIFS:
        embed.set_image(url=random.choice(GIFS["blush"]))

    await interaction.followup.send(embed=embed)

## NICKNAME (Versi Simple)
@bot.tree.command(name="nickname", description="Itsuki ngasih julukan ke seseorang")
async def nickname(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()

    # Cek kalo narget diri sendiri
    if user.id == interaction.user.id:
        await interaction.followup.send("Ngasih julukan ke diri sendiri? Aneh lu.", ephemeral=True)
        return

    nicknames = [
        "Berisik",
        "Si Laper",
        "NPC Server",
        "Beban Ringan",
        "Anak Kos",
        "Paling Ribut",
        "Figuran",
        "Orang Aneh",
        "Kang Drama",
        "Si Paling Anime",
        "Badut",
        "Wibu Wangy"
    ]

    chosen = random.choice(nicknames)

    embed = discord.Embed(
        description=f"Mulai hari ini, gue panggil lu **{chosen}** ya, {user.mention}. Jangan protes.",
        color=discord.Color.blue()
    )
    await interaction.followup.send(embed=embed)

# RUN
bot.run(os.getenv('DISCORD_TOKEN'))