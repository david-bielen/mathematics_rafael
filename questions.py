from __future__ import annotations

import random
from itertools import pairwise
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from collections.abc import Callable

MIN_TWO_DIGIT = 10
MIN_THREE_DIGIT = 100
MAX_NUMBER = 1000

SEPARATORS = str.maketrans({",": " ", "€": " ", "+": " ", "=": " = "})

CHAIN_TERMS = (3, 4)

PICTURE_LETTERS = ("x", "y", "z", "a", "b", "c")
MIN_PICTURE_LETTERS = 3
MAX_PICTURE_LETTERS = 4
MAX_PICTURE_VALUE = 100

# A near neighbour forces place-value thinking; the two zeros make "=" common.
NEIGHBOUR_OFFSETS = (-100, -10, -1, 0, 0, 1, 10, 100)
DECOMPOSE_CHANCE = 0.5

SEQUENCE_STEPS = (2, 3, 4, 5, 6, 7, 10)
SEQUENCE_SHOWN = 4
SEQUENCE_ASKED = 3
SEQUENCE_MAX_START = 700
SEQUENCE_MIN_START = 200

MISSING_TERM_FORMS = (
    ("{a} + □ = {c}", "b"),
    ("□ + {b} = {c}", "a"),
    ("{c} - {b} = □", "a"),
    ("{c} - □ = {a}", "b"),
    ("□ - {b} = {a}", "c"),
)

ORDER_COUNT = 6

COUNT_WORDS = ("en", "två", "tre", "fyra", "fem", "sex", "sju", "åtta", "nio")
MIN_NOTE_COUNT = 2
MAX_NOTE_COUNT = 9
NOTES = ((100, "100-eurossedlar"), (10, "10-eurossedlar"), (1, "1-euromynt"))
WALLETS = ("En plånbok", "En börs", "Kassan i en affär", "En spargris")

NAMES = (
    ("Emma", "Hon"),
    ("Måns", "Han"),
    ("Ella", "Hon"),
    ("Atte", "Han"),
    ("Hanna", "Hon"),
    ("Sandor", "Han"),
    ("Venla", "Hon"),
    ("Niko", "Han"),
    ("Arthur", "Han"),
    ("Aurora", "Hon"),
    ("Kerstin", "Hon"),
    ("Viktor", "Han"),
    ("Rafael", "Han"),
)

WORD_PROBLEMS = (
    (
        "{name} har {a} euro i sin plånbok. {pronoun} köper en jacka som "
        "kostar {b} euro. Hur mycket pengar har {name} kvar?",
        "-",
    ),
    (
        "{name} har sparat {a} euro. {pronoun} köper en cykel som kostar "
        "{b} euro. Hur mycket pengar har {name} kvar?",
        "-",
    ),
    (
        "Läraren har {a} blyertspennor. Läraren delar ut {b} av pennorna "
        "till eleverna. Hur många pennor har läraren kvar?",
        "-",
    ),
    (
        "I skolans förråd finns {a} skolböcker. {b} av dem delas ut till "
        "eleverna. Hur många skolböcker blir kvar i förrådet?",
        "-",
    ),
    (
        "Skolan har {a} elever. {b} av eleverna är på rast. Hur många "
        "elever har lektion?",
        "-",
    ),
    (
        "{name} köper två böcker. Den ena boken kostar {a} euro och den "
        "andra {b} euro. Hur mycket kostar böckerna sammanlagt?",
        "+",
    ),
    (
        "I {name}s skola går det {a} elever och i grannskolan {b} elever. "
        "Hur många elever går det sammanlagt i de två skolorna?",
        "+",
    ),
    (
        "{name} sparar först {a} euro och sedan {b} euro till. Hur mycket "
        "pengar har {name} sparat sammanlagt?",
        "+",
    ),
    (
        "Biografen har {a} besökare på fredagen och {b} besökare på "
        "lördagen. Hur många besökare har biografen sammanlagt?",
        "+",
    ),
)


class Question(BaseModel):
    prompt: str
    answer: tuple[str, ...]


def normalize(text: str) -> tuple[str, ...]:
    """Compare answers as tokens: '500+40+8' equals '500, 40, 8'."""
    return tuple(text.lower().translate(SEPARATORS).split())


def _make(prompt: str, answer: str) -> Question:
    return Question(prompt=prompt, answer=normalize(answer))


def is_correct(question: Question, user_input: str) -> bool:
    return normalize(user_input) == question.answer


def generate_addition() -> Question:
    total = random.randint(MIN_THREE_DIGIT, MAX_NUMBER)
    first = random.randint(MIN_TWO_DIGIT, total - MIN_TWO_DIGIT)
    return _make(f"Vad är {first} + {total - first}? ", str(total))


def generate_subtraction() -> Question:
    minuend = random.randint(MIN_THREE_DIGIT, MAX_NUMBER)
    subtrahend = random.randint(MIN_TWO_DIGIT, minuend - MIN_TWO_DIGIT)
    prompt = f"Vad är {minuend} - {subtrahend}? "
    return _make(prompt, str(minuend - subtrahend))


def _chain_parts(count: int) -> list[int]:
    return [
        random.randint(MIN_TWO_DIGIT, MAX_NUMBER // count)
        for _ in range(count)
    ]


def generate_term_chain() -> Question:
    parts = _chain_parts(random.choice(CHAIN_TERMS))
    total = sum(parts)
    if random.choice((True, False)):
        shown = " + ".join(str(part) for part in parts)
        return _make(f"Vad är {shown}? ", str(total))
    shown = " - ".join(str(part) for part in parts[1:])
    return _make(f"Vad är {total} - {shown}? ", str(parts[0]))


def _picture_prompt(letters: list[str], values: list[int]) -> str:
    sums = [
        f"{index + 2}) {first} + {second} = "
        f"{values[index] + values[index + 1]}"
        for index, (first, second) in enumerate(pairwise(letters))
    ]
    return "\n".join(
        [
            "Varje bokstav motsvarar ett tal:",
            f"1) {letters[0]} = {values[0]}",
            *sums,
            f"Ange värdena i ordningen {', '.join(letters)}: ",
        ],
    )


def generate_picture_equation() -> Question:
    count = random.randint(MIN_PICTURE_LETTERS, MAX_PICTURE_LETTERS)
    letters = random.sample(PICTURE_LETTERS, k=count)
    values = [random.randint(1, MAX_PICTURE_VALUE) for _ in letters]
    answer = " ".join(str(value) for value in values)
    return _make(_picture_prompt(letters, values), answer)


def _as_parts(number: int) -> str:
    parts = (number // 100 * 100, number // 10 % 10 * 10, number % 10)
    return " + ".join(str(part) for part in parts if part)


def _sign(left: int, right: int) -> str:
    if left == right:
        return "="
    return "<" if left < right else ">"


def _neighbour(number: int) -> int:
    offset = random.choice(NEIGHBOUR_OFFSETS)
    return min(max(number + offset, 1), MAX_NUMBER)


def generate_comparison() -> Question:
    left = random.randint(MIN_THREE_DIGIT, MAX_NUMBER)
    right = _neighbour(left)
    decompose = random.random() < DECOMPOSE_CHANCE
    shown = _as_parts(right) if decompose else str(right)
    prompt = f"Välj rätt tecken (<, = eller >). {left} __ {shown} "
    return _make(prompt, _sign(left, right))


def generate_number_sequence() -> Question:
    step = random.choice(SEQUENCE_STEPS) * random.choice((1, -1))
    start = (
        random.randint(SEQUENCE_MIN_START, MAX_NUMBER)
        if step < 0
        else random.randint(0, SEQUENCE_MAX_START)
    )
    terms = [start + step * i for i in range(SEQUENCE_SHOWN + SEQUENCE_ASKED)]
    shown = ", ".join(str(term) for term in terms[:SEQUENCE_SHOWN])
    prompt = f"Fortsätt talföljden. Skriv de tre följande talen: {shown}, ... "
    return _make(prompt, " ".join(str(t) for t in terms[SEQUENCE_SHOWN:]))


def generate_missing_term() -> Question:
    total = random.randint(MIN_TWO_DIGIT, MAX_NUMBER)
    part = random.randint(1, total - 1)
    values = {"a": total - part, "b": part, "c": total}
    form, key = random.choice(MISSING_TERM_FORMS)
    puzzle = form.format(**values)
    return _make(f"Vilket tal fattas? {puzzle} ", str(values[key]))


def generate_place_value_split() -> Question:
    number = random.randint(MIN_THREE_DIGIT, MAX_NUMBER - 1)
    parts = (number // 100 * 100, number // 10 % 10 * 10, number % 10)
    prompt = (
        "Dela upp talet i talsorter (t.ex. 235 = 200 + 30 + 5). "
        f"{number} = "
    )
    return _make(prompt, " + ".join(str(part) for part in parts))


def generate_place_value_join() -> Question:
    hundreds = random.randint(1, 9)
    tens, ones = (random.randint(0, 9) for _ in range(2))
    prompt = (
        f"Talet har {hundreds} hundratal, {tens} tiotal och {ones} ental. "
        "Vilket tal är det? "
    )
    return _make(prompt, str(hundreds * 100 + tens * 10 + ones))


def generate_order_numbers() -> Question:
    numbers = random.sample(range(1, MAX_NUMBER + 1), ORDER_COUNT)
    ascending = random.choice((True, False))
    direction = (
        "minsta till det största" if ascending else "största till det minsta"
    )
    shown = ", ".join(str(number) for number in numbers)
    prompt = f"Ordna talen från det {direction}: {shown} "
    ordered = sorted(numbers, reverse=not ascending)
    return _make(prompt, " ".join(str(number) for number in ordered))


def generate_wallet_money() -> Question:
    counts = [random.randint(MIN_NOTE_COUNT, MAX_NOTE_COUNT) for _ in NOTES]
    items = [
        f"{COUNT_WORDS[count - 1]} {name}"
        for count, (_, name) in zip(counts, NOTES, strict=True)
    ]
    total = sum(
        count * value for count, (value, _) in zip(counts, NOTES, strict=True)
    )
    listed = f"{', '.join(items[:-1])} och {items[-1]}"
    prompt = (
        f"{random.choice(WALLETS)} innehåller {listed}. "
        "Hur mycket pengar är det sammanlagt? "
    )
    return _make(prompt, str(total))


def _problem_numbers(operator: str) -> tuple[int, int, int]:
    total = random.randint(MIN_THREE_DIGIT, MAX_NUMBER)
    part = random.randint(MIN_TWO_DIGIT, total - MIN_TWO_DIGIT)
    if operator == "-":
        return total, part, total - part
    return part, total - part, total


def generate_word_problem() -> Question:
    template, operator = random.choice(WORD_PROBLEMS)
    first, second, answer = _problem_numbers(operator)
    name, pronoun = random.choice(NAMES)
    text = template.format(name=name, pronoun=pronoun, a=first, b=second)
    return _make(f"{text}\nSvar (bara talet): ", str(answer))


GENERATORS: tuple[Callable[[], Question], ...] = (
    generate_addition,
    generate_subtraction,
    generate_term_chain,
    generate_picture_equation,
    generate_comparison,
    generate_number_sequence,
    generate_missing_term,
    generate_place_value_split,
    generate_place_value_join,
    generate_order_numbers,
    generate_wallet_money,
    generate_word_problem,
)
