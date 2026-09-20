# /// script
# dependencies = ['pytz']
# ///
import datetime
import json
import operator
import random
from abc import ABC, abstractmethod
from pathlib import Path

import pytz  # type: ignore


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


class SequenceArithmeticQuestion(Question):
    def __init__(self) -> None:
        self.numbers = []
        self.operations = []
        self.answer = None

    def generate_question(self) -> None:
        ops = {
            "+": operator.add,
            "-": operator.sub,
        }

        # Ensure at least 3 or 4 consecutive values are used
        num_operations = random.choice(
            [2, 3],
        )  # This gives 3 or 4 values in total
        op_symbol, operation = random.choice(list(ops.items()))
        while True:
            # Choose a single operator for the entire question

            self.numbers = [
                random.randint(1, 10) for _ in range(num_operations + 1)
            ]
            self.operations = [op_symbol] * num_operations

            # Calculate the result to ensure it is not negative
            result = self.numbers[0]
            valid = True
            for num in self.numbers[1:]:
                if operation == operator.sub and result < num:
                    valid = False
                    break
                result = operation(result, num)

            if valid:
                self.answer = result
                break

    def ask_question(self) -> str:
        expression = f"{self.numbers[0]}"
        for op, num in zip(self.operations, self.numbers[1:], strict=False):
            expression += f" {op} {num}"
        return input(f"What is {expression}? ")

    def check_answer(self, user_input: str) -> bool:
        try:
            user_answer = int(user_input)
            if user_answer == self.answer:
                return True
            print("Incorrect. Please try again.")
        except ValueError:
            print("Please enter a valid integer.")
        return False


class SymbolicEquationQuestion(Question):
    def __init__(self) -> None:
        self.symbols: list[str] = []
        self.values: dict[str, int] = {}
        self.equations: list[str] = []

    def generate_question(self) -> None:
        possible_symbols = ["x", "y", "z", "r", "a", "b", "c"]
        n_symbols = random.randint(3, 4)
        self.symbols = random.sample(possible_symbols, k=n_symbols)

        # Assign random values
        self.values = {s: random.randint(1, 10) for s in self.symbols}

        # Build the ring equations
        ring_eqs: list[str] = []
        for i in range(n_symbols):
            s1 = self.symbols[i]
            s2 = self.symbols[(i + 1) % n_symbols]
            val_sum = self.values[s1] + self.values[s2]
            eq_str = f"{s1} + {s2} = {val_sum}"
            ring_eqs.append(eq_str)

        # Replace the FIRST ring equation with a single-unknown equation:
        # e.g., if the first symbol is s0 with value val_s0,
        # turn "s0 + s1 = X" into "s0 = val_s0".
        s0 = self.symbols[0]
        val_s0 = self.values[s0]
        ring_eqs[0] = f"{s0} = {val_s0}"

        self.equations = ring_eqs

    def ask_question(self) -> str:
        print("Solve the following system of equations:")
        for i, eq in enumerate(self.equations, start=1):
            print(f"{i}) {eq}")
        return input("Enter your solution (e.g., x=3, y=5, z=2): ")

    def check_answer(self, user_input: str) -> bool:
        try:
            user_solution: dict[str, int] = {}
            parts = user_input.split(",")
            for p in parts:
                lhs, rhs = p.split("=")
                user_solution[lhs.strip()] = int(rhs.strip())

            all_correct = True
            for sym, val in self.values.items():
                guess = user_solution.get(sym)
                if guess != val:
                    print(
                        f"Incorrect value for {sym}. "
                        f"(Your guess: {guess}, correct: {val})",
                    )
                    all_correct = False
        except (ValueError, IndexError):
            print("Invalid format. Please enter like: x=3, y=5, z=2")
            return False
        else:
            return all_correct


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
    def __init__(
        self,
        filename: str = "stats.json",
        timezone: str = "Europe/Helsinki",
    ) -> None:
        self.filename = filename
        self.stats = self.load_stats()
        self.timezone = pytz.timezone(timezone)

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
        today = datetime.datetime.now(tz=self.timezone).strftime("%Y-%m-%d")
        self.stats[today] = self.stats.get(today, 0) + 1
        self.save_stats()

    def get_today_count(self) -> int:
        return self.stats.get(
            datetime.datetime.now(tz=self.timezone).strftime("%Y-%m-%d"),
            0,
        )


def play_game() -> None:
    stats_manager = StatsManager()
    question_types = [
        ArithmeticQuestion,
        ComparisonQuestion,
        SequenceArithmeticQuestion,
        SymbolicEquationQuestion,
    ]

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
