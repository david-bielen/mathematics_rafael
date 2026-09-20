import subprocess
import sys

from stats import locked_message, missing_answers

REQUIRED_CORRECT_ANSWERS = 10

remaining = missing_answers(REQUIRED_CORRECT_ANSWERS)
if remaining:
    print(locked_message(remaining, "Mario"))
    sys.exit()

subprocess.run(["mari0"], check=False)  # noqa: S603, S607
