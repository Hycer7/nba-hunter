import json
from nba_api.stats.endpoints import leaguegamelog

df = leaguegamelog.LeagueGameLog(
    season="2026-27", player_or_team_abbreviation="P", timeout=60
).get_data_frames()[0].sort_values("GAME_DATE", ascending=False)

out = {}
for _, r in df.iterrows():
    if not (r["MIN"] > 0):
        continue
    out.setdefault(r["PLAYER_NAME"], []).append({
        "d": r["GAME_DATE"], "o": r["MATCHUP"], "w": r["WL"] or "",
        "min": int(r["MIN"]), "pts": int(r["PTS"]), "reb": int(r["REB"]),
        "ast": int(r["AST"]), "tp": int(r["FG3M"]), "blk": int(r["BLK"]),
    })

json.dump(out, open("gamelog.json", "w"), ensure_ascii=False)
print(f"OK: {len(out)} jugadores con gamelog.json")