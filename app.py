import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Premier League Dashboard", layout="wide")
st.title("🏆 Premier League Stats Dashboard")
st.sidebar.title("Navigation")

if "show_players" not in st.session_state:
    st.session_state.show_players = False
if "show_teams" not in st.session_state:
    st.session_state.show_teams = False

if st.sidebar.button("🧍 Players"):
    st.session_state.show_players = not st.session_state.show_players
    st.session_state.show_teams = False

if st.sidebar.button("🛡️ Teams"):
    st.session_state.show_teams = not st.session_state.show_teams
    st.session_state.show_players = False

# PLAYER SECTION
if st.session_state.show_players:
    player_option = st.sidebar.radio("Player Options", [
        "Player Stats", "Top Scorers", "Top Assists", "Head-to-Head"
    ])

    if player_option == "Player Stats":
        st.header("🧍 Explore Players by Team")

        conn = sqlite3.connect("premier_league.db")
        df = pd.read_sql_query("SELECT * FROM players", conn)
        teams = sorted(df["team"].unique())
        selected_team = st.selectbox("Select a team", teams)
        team_players = df[df["team"] == selected_team]
        selected_player = st.selectbox("Select a player", team_players["name"].tolist())
        player_profile = team_players[team_players["name"] == selected_player].iloc[0]
        st.subheader(f"📄 Profile: {player_profile['name']}")
        st.markdown(f"""
        **Team:** {player_profile['team']}  
        **Position:** {player_profile['position']}  
        **Goals:** {player_profile['goals']}  
        **Assists:** {player_profile['assists']}  
        **Matches Played:** {player_profile['matches_played']}  
        **Minutes Played:** {player_profile.get('minutes_played', 'N/A')}
        """)
        conn.close()

    elif player_option == "Top Scorers":
        st.header("🥇 Top Goal Scorers")

        conn = sqlite3.connect("premier_league.db")
        df_top = pd.read_sql_query("SELECT name, team, goals FROM players ORDER BY goals DESC LIMIT 5", conn)
        st.subheader("📋 Top 5 Scorers Table")
        st.dataframe(df_top.reset_index(drop=True), use_container_width=True, height=330)

        st.markdown("---")
        st.subheader("⚡ Most Efficient Scorers (Goals per 90 Minutes)")
        df_full = pd.read_sql_query("SELECT name, team, goals, minutes_played FROM players WHERE minutes_played > 0", conn)
        conn.close()
        df_full["goals_per_90"] = (df_full["goals"] / df_full["minutes_played"]) * 90
        df_eff = df_full.sort_values(by="goals_per_90", ascending=False).head(5)
        df_eff["goals_per_90"] = df_eff["goals_per_90"].round(2)
        st.dataframe(
            df_eff[["name", "team", "goals", "minutes_played", "goals_per_90"]].reset_index(drop=True),
            use_container_width=True,
            height=330
        )

        st.markdown("---")
        st.subheader("📊 Bar Chart – Top 5 Goal Scorers")
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.barh(df_top["name"], df_top["goals"], color="royalblue")
        ax.invert_yaxis()
        ax.set_xlabel("Goals")
        ax.set_title("Top 5 Goal Scorers")
        st.pyplot(fig)

    elif player_option == "Top Assists":
        st.header("🎯 Top Assist Providers")
        conn = sqlite3.connect("premier_league.db")
        df_top = pd.read_sql_query("SELECT name, team, assists FROM players ORDER BY assists DESC LIMIT 5", conn)
        st.subheader("📋 Top 5 Assist Providers")
        st.dataframe(df_top.reset_index(drop=True), use_container_width=True, height=330)

        st.markdown("---")
        st.subheader("⚡ Most Efficient Creators (Assists per 90 Minutes)")
        df_full = pd.read_sql_query("SELECT name, team, assists, minutes_played FROM players WHERE minutes_played > 0", conn)
        conn.close()
        df_full["assists_per_90"] = (df_full["assists"] / df_full["minutes_played"]) * 90
        df_eff = df_full.sort_values(by="assists_per_90", ascending=False).head(5)
        df_eff["assists_per_90"] = df_eff["assists_per_90"].round(2)
        st.dataframe(
            df_eff[["name", "team", "assists", "minutes_played", "assists_per_90"]].reset_index(drop=True),
            use_container_width=True,
            height=330
        )

        st.markdown("---")
        st.subheader("📊 Bar Chart – Top 5 Assist Providers")
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.barh(df_top["name"], df_top["assists"], color="seagreen")
        ax.invert_yaxis()
        ax.set_xlabel("Assists")
        ax.set_title("Top 5 Assist Providers")
        st.pyplot(fig)

    elif player_option == "Head-to-Head":
        st.header("⚔️ Head-to-Head Player Comparison")
        conn = sqlite3.connect("premier_league.db")
        df = pd.read_sql_query("SELECT * FROM players WHERE minutes_played > 0", conn)
        conn.close()
        players = sorted(df["name"].unique())
        col1, col2 = st.columns(2)
        with col1:
            player1 = st.selectbox("Select Player 1", players)
        with col2:
            player2 = st.selectbox("Select Player 2", players, index=1)

        p1 = df[df["name"] == player1].iloc[0]
        p2 = df[df["name"] == player2].iloc[0]

        def per90(val, minutes):
            return round((val / minutes) * 90, 2) if minutes else 0

        stats = pd.DataFrame({
            "Stat": ["Team", "Position", "Goals", "Assists", "Matches", "Minutes", "Goals per 90", "Assists per 90"],
            player1: [
                p1["team"], p1["position"], p1["goals"], p1["assists"], p1["matches_played"],
                p1["minutes_played"], per90(p1["goals"], p1["minutes_played"]), per90(p1["assists"], p1["minutes_played"])
            ],
            player2: [
                p2["team"], p2["position"], p2["goals"], p2["assists"], p2["matches_played"],
                p2["minutes_played"], per90(p2["goals"], p2["minutes_played"]), per90(p2["assists"], p2["minutes_played"])
            ]
        })
        st.dataframe(stats.set_index("Stat"), use_container_width=True)

# TEAM SECTION
if st.session_state.show_teams:
    team_option = st.sidebar.radio("Team Options", [
        "Team Stats", "Top Scoring Teams", "Best Defenses", "League Standings"
    ])

    if team_option == "Team Stats":
        st.header("🛡️ Team Stats")
        conn = sqlite3.connect("premier_league.db")
        df = pd.read_sql_query("SELECT * FROM players", conn)
        team_stats = df.groupby("team").agg({
            "goals": "sum",
            "assists": "sum",
            "matches_played": "sum"
        }).reset_index()
        team_stats.columns = ["Team", "Total Goals", "Total Assists", "Total Matches Played"]
        st.dataframe(team_stats, use_container_width=True)
        conn.close()

    elif team_option == "Top Scoring Teams":
        st.header("⚽ Teams with Most Goals Scored")
        conn = sqlite3.connect("premier_league.db")
        df = pd.read_sql_query("""
            SELECT name as team, season, goals_scored 
            FROM teams 
            ORDER BY goals_scored DESC
        """, conn)
        conn.close()
        st.dataframe(df.reset_index(drop=True), use_container_width=True, height=500)

    elif team_option == "Best Defenses":
        st.header("🛡️ Teams with Fewest Goals Conceded")
        conn = sqlite3.connect("premier_league.db")
        df = pd.read_sql_query("""
            SELECT name as team, season, goals_conceded 
            FROM teams 
            ORDER BY goals_conceded ASC
        """, conn)
        conn.close()
        st.dataframe(df.reset_index(drop=True), use_container_width=True, height=500)

    elif team_option == "League Standings":
        st.header("📈 League Standings")
        conn = sqlite3.connect("premier_league.db")
        df = pd.read_sql_query("SELECT name, season, position FROM teams", conn)
        conn.close()
        df = df.sort_values(by=["season", "position"])
        st.dataframe(df.reset_index(drop=True), use_container_width=True, height=500)

# Landing Page
if not st.session_state.show_players and not st.session_state.show_teams:
    st.markdown("### ⚽ Project Overview")
    st.markdown("""
The Premier League is the top professional football (soccer) league in England. It consists of 20 teams and typically runs from August to May with each team playing 38 matches.  
It is considered by many as one of the most competitive and entertaining leagues in the world.  

You can:
- View individual player profiles by team  
- Analyze top scorers and assist providers  
- See efficiency metrics like **Goals and Assists per 90 Minutes**  
- Compare players head-to-head  
- Track team league standings  
- Switch between players and teams using the sidebar  
    """)
