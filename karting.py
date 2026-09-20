import subprocess
import sys
from pathlib import Path

from stats import locked_message, missing_answers

REQUIRED_CORRECT_ANSWERS = 10
GAME_DIR = Path("/home/rafael/Downloads/SuperTuxKart-1.4-linux-x86_64")

remaining = missing_answers(REQUIRED_CORRECT_ANSWERS)
if remaining:
    print(locked_message(remaining, "Karting"))
    sys.exit()

subprocess.run(  # noqa: S603
    [GAME_DIR / "run_game.sh"],
    cwd=GAME_DIR,
    check=False,
)
