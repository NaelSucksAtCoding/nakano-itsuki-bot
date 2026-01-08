import sqlite3
import random

DB_NAME = "itsuki_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Bikin tabel reputasi kalau belum ada
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_status (
            user_id INTEGER PRIMARY KEY,
            reputation INTEGER DEFAULT 0,
            title TEXT DEFAULT 'NPC Biasa'
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database Reputation siap!")

def get_user_data(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT reputation, title FROM user_status WHERE user_id = ?", (user_id,))
    data = c.fetchone()
    conn.close()
    
    if data:
        return data # Balikin (reputation, title)
    else:
        # Kalau user baru, daftarin dulu
        register_user(user_id)
        return (0, "NPC Biasa")

def register_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Judul awal random
    titles = ["NPC Biasa", "Warga Baru", "Kang Pantau", "Fans Itsuki"]
    initial_title = random.choice(titles)
    
    try:
        c.execute("INSERT INTO user_status (user_id, reputation, title) VALUES (?, 0, ?)", (user_id, initial_title))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Udah terdaftar
    conn.close()

def change_reputation(user_id, amount):
    # Update reputasi (bisa nambah atau kurang)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Pastikan user ada dulu
    get_user_data(user_id) 
    
    c.execute("UPDATE user_status SET reputation = reputation + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    
    # Cek level buat update Title otomatis
    c.execute("SELECT reputation FROM user_status WHERE user_id = ?", (user_id,))
    new_rep = c.fetchone()[0]
    
    new_title = None
    if new_rep <= -10: new_title = "Beban Server 🤡"
    elif new_rep >= 10 and new_rep < 50: new_title = "Warga Teladan 😇"
    elif new_rep >= 50: new_title = "Sepuh Server 👑"
    
    if new_title:
        c.execute("UPDATE user_status SET title = ? WHERE user_id = ?", (new_title, user_id))
        conn.commit()
        
    conn.close()
    return new_rep