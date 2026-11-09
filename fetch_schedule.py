import json
import requests
from datetime import datetime, timedelta, timezone

URL = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


def bajar():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("cdn.nba.com falló:", e, "- probando con nba_api...")
        from nba_api.stats.endpoints import scheduleleaguev2
        return scheduleleaguev2.ScheduleLeagueV2(season="2026-27", timeout=60).get_dict()


data = bajar()
ls = data.get("leagueSchedule", data)

ahora = datetime.now(timezone.utc)
ini = ahora - timedelta(days=1)
fin = ahora + timedelta(days=14)

games = []
for d in ls["gameDates"]:
    for g in d["games"]:
        home = g["homeTeam"].get("teamTricode")
        away = g["awayTeam"].get("teamTricode")
        if not home or not away:
            continue
        t = datetime.fromisoformat(g["gameDateTimeUTC"].replace("Z", "+00:00"))
        if ini <= t <= fin:
            games.append({"utc": g["gameDateTimeUTC"], "home": home, "away": away})

games.sort(key=lambda g: g["utc"])
json.dump({"games": games}, open("schedule.json", "w"))
print(f"OK: {len(games)} partidos en los próximos 14 días")