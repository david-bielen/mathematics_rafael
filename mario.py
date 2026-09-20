import datetime
import json
import subprocess
import sys
from pathlib import Path

import pytz

REQUIRED_CORRECT_ANSWERS = 10
helsinki_tz = pytz.timezone("Europe/Helsinki")
stats_file = Path("stats.json")
# A fresh clone has no stats yet: treat that as "nothing answered today".
stats = json.loads(stats_file.read_text()) if stats_file.is_file() else {}
today = datetime.datetime.now(tz=helsinki_tz).strftime("%Y-%m-%d")
if stats.get(today, 0) < REQUIRED_CORRECT_ANSWERS:
    print(
        "You have not answered enough questions today. You need to answer "
        f"{REQUIRED_CORRECT_ANSWERS - stats.get(today, 0)} "
        "more question(s) before you can play Mario.\n",
    )
    sys.exit()

subprocess.run(["mari0"], check=False)  # noqa: S603, S607
