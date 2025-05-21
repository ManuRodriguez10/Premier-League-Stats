import sqlite3

conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()

# Check if minutes_played already exists
cursor.execute("PRAGMA table_info(players)")
columns = [col[1] for col in cursor.fetchall()]

if "minutes_played" not in columns:
    cursor.execute("ALTER TABLE players ADD COLUMN minutes_played INTEGER DEFAULT 0")
    print("✅ Column 'minutes_played' added.")
else:
    print("⚠️ Column 'minutes_played' already exists.")

conn.commit()
conn.close()
