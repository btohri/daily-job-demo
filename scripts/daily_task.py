# scripts/daily_task.py
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode
import json, csv
from datetime import datetime
from zoneinfo import ZoneInfo

# 屏東（約略座標）
LAT, LON = 22.68, 120.48
TZ = "Asia/Taipei"

params = {
    "latitude": LAT,
    "longitude": LON,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": TZ,
}
url = "https://api.open-meteo.com/v1/forecast?" + urlencode(params)

# 取得資料
with urlopen(url, timeout=30) as r:
    data = json.load(r)

daily = data["daily"]
dates = daily["time"]
tmax = daily["temperature_2m_max"]
tmin = daily["temperature_2m_min"]
prcp = daily["precipitation_sum"]

# 只寫入「今天」這一筆（以台北時區判定）
today = datetime.now(ZoneInfo(TZ)).date().isoformat()
rows = []
for d, mx, mn, p in zip(dates, tmax, tmin, prcp):
    if d == today:
        rows.append({"date": d, "tmax": mx, "tmin": mn, "precip_mm": p})

# 輸出到 CSV
Path("data").mkdir(parents=True, exist_ok=True)
csv_path = Path("data/weather_pingtung.csv")
write_header = not csv_path.exists()
with csv_path.open("a", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["date", "tmax", "tmin", "precip_mm"])
    if write_header:
        w.writeheader()
    for row in rows:
        w.writerow(row)

print(f"OK: wrote {len(rows)} row(s) to {csv_path}")
