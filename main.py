import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()

# Create a table for players
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    team TEXT NOT NULL,
    position TEXT NOT NULL,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    matches_played INTEGER DEFAULT 0
)
""")

# Optional: Insert a sample player
cursor.execute("""
INSERT INTO players (name, team, position, goals, assists, matches_played)
VALUES ('Erling Haaland', 'Manchester City', 'Forward', 36, 8, 35)
""")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database initialized and sample player added.")
