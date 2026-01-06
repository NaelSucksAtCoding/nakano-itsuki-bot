import sqlite3
import database  # Import modul database biar bisa dipake di main.py

# Nama file database
DB_NAME = "itsuki.db"

def initialize_db():
    """Bikin tabel kalau belum ada."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 1. Bikin Tabel Users (Simpan Duit & XP)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            money INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0
        )
    ''')

    # 2. Bikin Tabel Inventory (Simpan Item Gacha)
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_name TEXT,
            rarity TEXT,
            amount INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Database {DB_NAME} siap digunakan!")

# --- FUNGSI BANTUAN BUAT EKONOMI ---

def register_user(user_id):
    """Daftarin user baru ke database kalau belum ada"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Cek dulu ada ga
    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if c.fetchone() is None:
        c.execute("INSERT INTO users (user_id, money, xp) VALUES (?, 100, 0)", (user_id,)) # Modal awal 100
        conn.commit()
        print(f"User {user_id} terdaftar.")
    conn.close()

def get_data(user_id):
    """Ambil data uang & xp user"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT money, xp FROM users WHERE user_id = ?", (user_id,))
    data = c.fetchone()
    conn.close()
    return data # Balikkin (money, xp) atau None

def update_money(user_id, amount):
    """Tambah atau kurang uang (pakai minus buat ngurangin)"""
    register_user(user_id) # Jaga-jaga kalau user belum terdaftar
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET money = money + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

# --- FUNGSI BANTUAN BUAT INVENTORY/GACHA ---

def add_item(user_id, item_name, rarity):
    """Masukin item ke inventory"""
    register_user(user_id)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Cek user udah punya item ini belum?
    c.execute("SELECT amount FROM inventory WHERE user_id = ? AND item_name = ?", (user_id, item_name))
    result = c.fetchone()
    
    if result:
        # Kalau udah punya, tambah jumlahnya
        c.execute("UPDATE inventory SET amount = amount + 1 WHERE user_id = ? AND item_name = ?", (user_id, item_name))
    else:
        # Kalau belum, bikin baris baru
        c.execute("INSERT INTO inventory (user_id, item_name, rarity, amount) VALUES (?, ?, ?, 1)", (user_id, item_name, rarity))
    
    conn.commit()
    conn.close()

# Biar bisa dites langsung (Optional)
if __name__ == "__main__":
    initialize_db()