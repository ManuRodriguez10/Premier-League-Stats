import sqlite3

# Sample player data
players = [
    # Man City
    ("Erling Haaland", "Manchester City", "Forward", 36, 8, 35),
    ("Kevin De Bruyne", "Manchester City", "Midfielder", 10, 18, 30),

    # Arsenal
    ("Bukayo Saka", "Arsenal", "Forward", 14, 11, 38),
    ("Martin Ødegaard", "Arsenal", "Midfielder", 12, 8, 37),

    # Liverpool
    ("Mohamed Salah", "Liverpool", "Forward", 19, 9, 36),
    ("Trent Alexander-Arnold", "Liverpool", "Defender", 2, 10, 35),

    # Manchester United
    ("Marcus Rashford", "Manchester United", "Forward", 17, 7, 36),
    ("Bruno Fernandes", "Manchester United", "Midfielder", 8, 10, 37),

    # Tottenham
    ("Heung-min Son", "Tottenham", "Forward", 13, 6, 35),
    ("James Maddison", "Tottenham", "Midfielder", 7, 8, 30),

    # Chelsea
    ("Raheem Sterling", "Chelsea", "Forward", 9, 5, 33),
    ("Enzo Fernández", "Chelsea", "Midfielder", 2, 4, 32),

    # Newcastle
    ("Alexander Isak", "Newcastle", "Forward", 18, 3, 34),
    ("Bruno Guimarães", "Newcastle", "Midfielder", 5, 6, 35),

    # Aston Villa
    ("Ollie Watkins", "Aston Villa", "Forward", 15, 9, 37)
]

# Connect to the DB
conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()

# Insert players into the DB
cursor.executemany("""
    INSERT INTO players (name, team, position, goals, assists, matches_played)
    VALUES (?, ?, ?, ?, ?, ?)
""", players)

# Save and close
conn.commit()
conn.close()

print("Sample players added successfully.")
