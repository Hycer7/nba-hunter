import json
from nba_api.stats.endpoints import leaguedashplayerstats, playerindex

SEASON = "2026-27"
EAST = {"BOS","BKN","NYK","PHI","TOR","CHI","CLE","DET","IND","MIL","ATL","CHA","MIA","ORL","WAS"}

adv = leaguedashplayerstats.LeagueDashPlayerStats(
    season=SEASON, measure_type_detailed_defense="Advanced",
    per_mode_detailed="PerGame", timeout=60).get_data_frames()[0]

base = leaguedashplayerstats.LeagueDashPlayerStats(
    season=SEASON, measure_type_detailed_defense="Base",
    per_mode_detailed="Per100Possessions", timeout=60).get_data_frames()[0].set_index("PLAYER_ID")

idx = playerindex.PlayerIndex(season=SEASON, timeout=60).get_data_frames()[0]
pos = dict(zip(idx["PERSON_ID"], idx["POSITION"]))

out = []
for _, r in adv.iterrows():
    if r["GP"] < 5 or r["MIN"] < 15:
        continue
    b = base.loc[r["PLAYER_ID"]]
    t = r["TEAM_ABBREVIATION"]
    out.append({
        "n": r["PLAYER_NAME"],
        "id": int(r["PLAYER_ID"]),
        "t": t,
        "c": "E" if t in EAST else "W",
        "p": (pos.get(r["PLAYER_ID"]) or "F")[0],
        "mpg": round(r["MIN"], 1),
        "pts": round(b["PTS"], 1),
        "reb": round(b["REB"], 1),
        "ast100": round(b["AST"], 1),
        "usg": round(r["USG_PCT"] * 100, 1),
        "ast": round(r["AST_PCT"] * 100, 1),
        "ts": round(r["TS_PCT"] * 100, 1),
        "pie": round(r["PIE"] * 100, 1),
        "per": None,
        "ws": None,
    })

json.dump(out, open("players.json", "w"), indent=2)
print(f"OK: {len(out)} jugadores guardados en players.json")