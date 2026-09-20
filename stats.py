import datetime
import json
from pathlib import Path
from typing import cast

import pytz

STATS_FILE = Path("stats.json")
TIMEZONE = pytz.timezone("Europe/Helsinki")


def _today() -> str:
    return datetime.datetime.now(tz=TIMEZONE).strftime("%Y-%m-%d")


def _load() -> dict[str, int]:
    # A fresh clone has no stats yet: treat that as "nothing answered today".
    if not STATS_FILE.is_file():
        return {}
    return cast("dict[str, int]", json.loads(STATS_FILE.read_text()))


def answers_today() -> int:
    return _load().get(_today(), 0)


def record_correct() -> int:
    today = _today()
    updated = _load() | {today: answers_today() + 1}
    STATS_FILE.write_text(json.dumps(updated, indent=4))
    return updated[today]


def missing_answers(required: int) -> int:
    return max(required - answers_today(), 0)


def locked_message(remaining: int, game: str) -> str:
    word = "fråga" if remaining == 1 else "frågor"
    return (
        "Du har inte svarat rätt på tillräckligt många frågor i dag. Du "
        f"behöver svara rätt på {remaining} {word} till innan du får spela "
        f"{game}.\n"
    )
