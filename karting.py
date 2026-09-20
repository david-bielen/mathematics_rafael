import datetime
import json
import subprocess
import sys
from pathlib import Path

import pytz

REQUIRED_CORRECT_ANSWERS = 10
GAME_DIR = Path("/home/rafael/Downloads/SuperTuxKart-1.4-linux-x86_64")
helsinki_tz = pytz.timezone("Europe/Helsinki")
stats = json.loads(Path("stats.json").read_text())
today = datetime.datetime.now(tz=helsinki_tz).strftime("%Y-%m-%d")
if stats.get(today, 0) < REQUIRED_CORRECT_ANSWERS:
    print(
        "You have not answered enough questions today. You need to answer "
        f"{REQUIRED_CORRECT_ANSWERS - stats.get(today, 0)} "
        "more question(s) before you can play Karting.\n",
    )
    sys.exit()

subprocess.run(  # noqa: S603
    [GAME_DIR / "run_game.sh"],
    cwd=GAME_DIR,
    check=False,
)
