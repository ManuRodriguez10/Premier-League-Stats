import sqlite3

conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()

# Sample updates
updates = [
    ("Erling Haaland", 2800),
    ("Mohamed Salah", 2900),
    ("Marcus Rashford", 2700),
    ("Alexander Isak", 2500),
    ("Heung-min Son", 2600),
    ("Bukayo Saka", 3000),
    ("Ollie Watkins", 2900),
    ("Kevin De Bruyne", 1800),
    ("Bruno Fernandes", 3100),
    ("James Maddison", 2700),
]

for name, minutes in updates:
    cursor.execute("UPDATE players SET minutes_played = ? WHERE name = ?", (minutes, name))

conn.commit()
conn.close()

print("Minutes played updated.")
