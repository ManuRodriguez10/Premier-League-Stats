import sqlite3

conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    season TEXT NOT NULL,
    goals_scored INTEGER DEFAULT 0,
    goals_conceded INTEGER DEFAULT 0,
    position INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("✅ 'teams' table created.")
