import datetime
import json
import operator
import random
from abc import ABC, abstractmethod
from pathlib import Path

import pytz

helsinki_tz = pytz.timezone("Europe/Helsinki")


class Question(ABC):
    @abstractmethod
    def generate_question(self) -> None:
        pass

    @abstractmethod
    def ask_question(self) -> str:
        pass

    @abstractmethod
    def check_answer(self, user_input: str) -> bool:
        pass


class ArithmeticQuestion(Question):
    def __init__(self) -> None:
        self.num1 = None
        self.num2 = None
        self.op_symbol = None
        self.operation = None
        self.answer = None

    def generate_question(self) -> None:
        ops = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
        }
        self.op_symbol, self.operation = random.choice(list(ops.items()))
        self.num1, self.num2 = self.get_random_numbers()
        self.answer = self.operation(self.num1, self.num2)

    def get_random_numbers(self) -> tuple[int, int]:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        if self.operation == operator.sub:
            num2 = random.randint(1, num1)
        elif self.operation == operator.mul:
            num1 = random.randint(1, 5)
            num2 = random.randint(1, 5)
        return num1, num2

    def ask_question(self) -> str:
        return input(f"What is {self.num1} {self.op_symbol} {self.num2}? ")

    def check_answer(self, user_input: str) -> bool:
        try:
            user_answer = int(user_input)
            if user_answer == self.answer:
                return True
            print("Incorrect. Please try again.")
        except ValueError:
            print("Please enter a valid integer.")
        return False


class ComparisonQuestion(Question):
    def __init__(self) -> None:
        self.expr1 = None
        self.expr2 = None
        self.correct_answer = None

    def generate_question(self) -> None:
        self.expr1 = self.generate_expression()
        self.expr2 = self.generate_expression()
        val1 = self.evaluate_expression(self.expr1)
        val2 = self.evaluate_expression(self.expr2)
        if val1 < val2:
            self.correct_answer = "<"
        elif val1 > val2:
            self.correct_answer = ">"
        else:
            self.correct_answer = "="

    def generate_expression(self) -> str:
        ops = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
        }
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 10)
        op_symbol, operation = random.choice(list(ops.items()))
        if operation == operator.sub:
            num2 = random.randint(1, num1)
        elif operation == operator.mul:
            num1 = random.randint(1, 5)
            num2 = random.randint(1, 5)
        return f"{num1} {op_symbol} {num2}"

    def evaluate_expression(self, expression: str) -> int:
        return eval(expression)  # noqa: S307

    def ask_question(self) -> str:
        return input(
            (
                f"Which is correct? {self.expr1} .. {self.expr2} "
                f"(Enter '<', '=', '>'): "
            ),
        )

    def check_answer(self, user_input: str) -> bool:
        if user_input.strip() == self.correct_answer:
            return True
        print("Incorrect. Please try again.")
        return False


class StatsManager:
    def __init__(self, filename: str = "stats.json") -> None:
        self.filename = filename
        self.stats = self.load_stats()

    def load_stats(self) -> dict[str, int]:
        return (
            json.loads(Path(self.filename).read_text())
            if Path(self.filename).exists()
            else {}
        )

    def save_stats(self) -> None:
        with Path(self.filename).open("w") as file:
            json.dump(self.stats, file, indent=4)

    def increment_today(self) -> None:
        today = datetime.datetime.now(tz=helsinki_tz).strftime("%Y-%m-%d")
        self.stats[today] = self.stats.get(today, 0) + 1
        self.save_stats()

    def get_today_count(self) -> int:
        return self.stats.get(
            datetime.datetime.now(tz=helsinki_tz).strftime("%Y-%m-%d"),
            0,
        )


def play_game() -> None:
    stats_manager = StatsManager()
    question_types = [ArithmeticQuestion, ComparisonQuestion]
    while True:
        question = random.choice(question_types)()
        question.generate_question()
        while True:
            user_input = question.ask_question()
            if question.check_answer(user_input):
                stats_manager.increment_today()
                if stats_manager.get_today_count() % 5 == 0:
                    print(
                        "\nYou have answered "
                        f"{stats_manager.get_today_count()} "
                        "questions correctly today. Keep it up!\n",
                    )
                else:
                    print("Correct! Let's move to the next question.\n")
                break


if __name__ == "__main__":
    play_game()
