import sqlite3
import pandas as pd

# Load dataset with proper delimiter handling
df = pd.read_csv("england-premier-league-teams-2018-to-2019-stats.csv")

# Check actual column names to avoid header mismatch
print("✅ Loaded CSV with", len(df.columns), "columns.")

# Normalize team names
def clean_team_name(name):
    name = str(name).strip().lower().replace(" fc", "")
    return name.title()

df["team"] = df["team_name"].apply(clean_team_name)
df["season"] = df["season"]
df["goals_scored"] = pd.to_numeric(df["goals_scored"], errors='coerce')
df["goals_conceded"] = pd.to_numeric(df["goals_conceded"], errors='coerce')
df["position"] = pd.to_numeric(df["league_position"], errors='coerce')

# Drop rows with missing values in critical columns
df = df[["team", "season", "goals_scored", "goals_conceded", "position"]].dropna()

# Connect to SQLite database
conn = sqlite3.connect("premier_league.db")
cursor = conn.cursor()

# Create teams table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    season TEXT,
    goals_scored INTEGER,
    goals_conceded INTEGER,
    position INTEGER
)
""")

# Clear existing data to avoid duplicates
cursor.execute("DELETE FROM teams")

# Insert clean data into table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO teams (name, season, goals_scored, goals_conceded, position)
        VALUES (?, ?, ?, ?, ?)
    """, (row["team"], row["season"], int(row["goals_scored"]), int(row["goals_conceded"]), int(row["position"])))

conn.commit()
conn.close()

print("✅ Teams seeded successfully.")
