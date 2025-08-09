from datetime import datetime, timezone
from pathlib import Path

Path("data").mkdir(parents=True, exist_ok=True)
with open("data/daily.txt", "a", encoding="utf-8") as f:
    f.write(f"Daily run at {datetime.now(timezone.utc).isoformat()}\n")
print("OK")
