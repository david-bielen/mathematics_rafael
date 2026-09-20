# /// script
# dependencies = ['pydantic', 'pytz']
# ///
import random

from questions import GENERATORS, Question, is_correct
from stats import record_correct

MAX_ATTEMPTS = 3
PROGRESS_EVERY = 5


def handle_correct_answer() -> None:
    count = record_correct()
    if count % PROGRESS_EVERY:
        print("Rätt! Nästa fråga.\n")
        return
    print(f"\nDu har svarat rätt på {count} frågor i dag. Bra jobbat!\n")


def ask(question: Question) -> bool:
    for _ in range(MAX_ATTEMPTS):
        if is_correct(question, input(question.prompt)):
            return True
        print("Fel. Försök igen.")
    print(f"Rätt svar: {' '.join(question.answer)}\n")
    return False


def play() -> None:
    while True:
        if ask(random.choice(GENERATORS)()):
            handle_correct_answer()


if __name__ == "__main__":
    try:
        play()
    except (EOFError, KeyboardInterrupt):
        print("\nHej då!")
