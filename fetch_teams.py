import json
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.static import teams as static_teams

SEASON = "2026-27"
EAST = {"BOS","BKN","NYK","PHI","TOR","CHI","CLE","DET","IND","MIL","ATL","CHA","MIA","ORL","WAS"}
abbr = {t["id"]: t["abbreviation"] for t in static_teams.get_teams()}

df = leaguedashteamstats.LeagueDashTeamStats(
    season=SEASON,
    measure_type_detailed_defense="Advanced",
    per_mode_detailed="PerGame",
    timeout=60,
).get_data_frames()[0]

pct = lambda v: round(v * 100, 1) if v < 1 else round(v, 1)

out = []
for _, r in df.iterrows():
    a = abbr[r["TEAM_ID"]]
    out.append({
        "a": a, "n": r["TEAM_NAME"], "c": "E" if a in EAST else "W",
        "w": int(r["W"]), "l": int(r["L"]),
        "pace": round(r["PACE"], 1), "off": round(r["OFF_RATING"], 1),
        "def": round(r["DEF_RATING"], 1), "net": round(r["NET_RATING"], 1),
        "efg": pct(r["EFG_PCT"]), "tov": pct(r["TM_TOV_PCT"]), "reb": pct(r["REB_PCT"]),
    })

json.dump(out, open("teams.json", "w"), indent=2)
print(f"OK: {len(out)} equipos guardados en teams.json")