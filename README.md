# Math Quiz Game

Welcome to the **Math Quiz Game**! This interactive command-line application asks questions in Swedish, modelled on the exercises in Rafael's school workbook (chapters 2-11: mental addition and subtraction up to 1000, place value, comparing and ordering numbers, number sequences and euro word problems). It tracks the number of correct answers each day, which is what unlocks the games.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
- [Usage](#usage)
- [Games](#games)

## Features

- **Räkna**: Addition and subtraction up to 1000, including chains of three or four terms (`125 + 93 + 244`).
- **Talföljder**: Continue a sequence up or down (`380, 382, 384, 386, ...`).
- **Tal som fattas**: Find the missing term (`32 - □ = 15`).
- **Talsorter**: Split a number into hundreds, tens and ones (`548 = 500 + 40 + 8`) and back again.
- **Jämföra och ordna**: Pick `<`, `=` or `>` (also against a split number, `240 __ 200 + 60`) and sort six numbers.
- **Pengar och textuppgifter**: Count euro notes and coins, and solve the workbook's story problems.
- **Bokstavsekvationer**: Work out what each letter stands for from a small system of equations.
- **Forgiving answers**: `500 + 40 + 8`, `500 40 8` and `92 €` are all accepted; after three wrong tries the answer is shown and the question does not count.
- **Daily Statistics**: Tracks and stores the number of correct answers each day in Helsinki's timezone.
- **Persistent Storage**: Statistics are saved in a `stats.json` file, allowing you to monitor your progress over time.
- **User-Friendly Interface**: Simple command-line prompts make the game easy to play.

## Installation

### Prerequisites

- **Python 3.12 or later**: Ensure you have Python installed on your system. You can download it from the [official website](https://www.python.org/downloads/).
- **UV**: Download and install UV from the [official website](https://docs.astral.sh/uv/getting-started/installation/). 

### Clone the Repository

```bash
git clone https://github.com/david-bielen/mathematics_rafael.git
cd mathematics_rafael
```

## Usage

Run the game with uv:
```bash
uv run main.py
```

`uv run` installs Python 3.12 and the dependencies (`pydantic`, `pytz`) on first run, so
there is no separate install step.


## Games

`mario.py` and `karting.py` only start their game once `stats.json` shows
`REQUIRED_CORRECT_ANSWERS` (10) correct answers for today; otherwise they say
in Swedish how many questions are still missing.

```bash
uv run mario.py
uv run karting.py
```
