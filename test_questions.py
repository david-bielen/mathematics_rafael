import random

import pytest

import questions
from questions import GENERATORS, MAX_NUMBER, Question, is_correct, normalize

RUNS = 300


def build(generator, seed: int) -> Question:
    random.seed(seed)
    return generator()


@pytest.mark.parametrize("generator", GENERATORS, ids=lambda g: g.__name__)
def test_answer_round_trips(generator) -> None:
    for seed in range(RUNS):
        question = build(generator, seed)
        assert question.prompt.strip()
        assert "None" not in question.prompt
        assert question.answer
        assert is_correct(question, " ".join(question.answer))


NUMERIC = (
    questions.generate_addition,
    questions.generate_subtraction,
    questions.generate_term_chain,
    questions.generate_missing_term,
    questions.generate_place_value_join,
    questions.generate_wallet_money,
    questions.generate_word_problem,
)


@pytest.mark.parametrize("generator", NUMERIC, ids=lambda g: g.__name__)
def test_numeric_answers_stay_in_range(generator) -> None:
    for seed in range(RUNS):
        (answer,) = build(generator, seed).answer
        assert 0 <= int(answer) <= MAX_NUMBER


def test_sequence_asks_for_three_terms() -> None:
    for seed in range(RUNS):
        answer = build(questions.generate_number_sequence, seed).answer
        terms = [int(term) for term in answer]
        steps = {b - a for a, b in zip(terms, terms[1:], strict=False)}
        assert len(terms) == questions.SEQUENCE_ASKED
        assert len(steps) == 1
        assert all(term >= 0 for term in terms)


def test_comparison_answers_a_sign() -> None:
    signs = {
        build(questions.generate_comparison, seed).answer[0]
        for seed in range(RUNS)
    }
    assert signs == {"<", "=", ">"}


def test_place_value_split_adds_up() -> None:
    for seed in range(RUNS):
        question = build(questions.generate_place_value_split, seed)
        parts = [int(token) for token in question.answer if token != "+"]
        assert sum(parts) == int(question.prompt.split()[-2])


def test_order_numbers_is_sorted() -> None:
    for seed in range(RUNS):
        question = build(questions.generate_order_numbers, seed)
        numbers = [int(token) for token in question.answer]
        upward = "minsta till" in question.prompt
        assert numbers == sorted(numbers, reverse=not upward)


def test_normalize_accepts_loose_formatting() -> None:
    assert normalize("500+40+8") == normalize("500, 40, 8")
    assert normalize(" 92 € ") == normalize("92")
