import sqlite3
import pandas as pd

# Load the dataset
df = pd.read_csv("premier-player-23-24.csv")
print(f"✅ Loaded CSV with {df.shape[1]} columns.")

# Normalize team names
def clean_team_name(name):
    name = str(name).strip().lower()
    name = name.replace(" fc", "")
    return name.title()

df["team"] = df["Team"].apply(clean_team_name)

# Rename columns to standard ones used in the app
df = df.rename(columns={
    "Player": "name",
    "Pos": "position",
    "Gls": "goals",
    "Ast": "assists",
    "Min": "minutes_played"
})

# Drop rows with missing values in any required column
df = df[["name", "team", "position", "goals", "assists", "minutes_played"]].dropna()

# Convert numeric fields
df["goals"] = pd.to_numeric(df["goals"], errors="coerce").fillna(0).astype(int)
df["assists"] = pd.to_numeric(df["assists"], errors="coerce").fillna(0).astype(int)
df["minutes_played"] = pd.to_numeric(df["minutes_played"], errors="coerce").fillna(0).astype(int)

# Add a dummy column for matches played (assume each player played some matches)
df["matches_played"] = (df["minutes_played"] / 90).round().astype(int)

# Connect to database
conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()

# Create players table
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    team TEXT,
    position TEXT,
    goals INTEGER,
    assists INTEGER,
    minutes_played INTEGER,
    matches_played INTEGER
)
""")

# Clear old data
cursor.execute("DELETE FROM players")

# Insert clean data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO players (name, team, position, goals, assists, minutes_played, matches_played)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        row["name"], row["team"], row["position"],
        row["goals"], row["assists"], row["minutes_played"], row["matches_played"]
    ))

conn.commit()
conn.close()
print("✅ Players seeded successfully.")
