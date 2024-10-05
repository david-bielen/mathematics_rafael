# Math Quiz Game

Welcome to the **Math Quiz Game**! This interactive command-line application challenges users with arithmetic and comparison questions, tracking the number of correct answers each day. Perfect for sharpening your math skills while keeping a daily log of your progress.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Install Dependencies](#install-dependencies)
- [Usage](#usage)

## Features

- **Arithmetic Questions**: Solve addition, subtraction, and multiplication problems.
- **Comparison Questions**: Determine the correct relational operator (`<`, `=`, `>`) between two expressions.
- **Daily Statistics**: Tracks and stores the number of correct answers each day in Helsinki's timezone.
- **Persistent Storage**: Statistics are saved in a `stats.json` file, allowing you to monitor your progress over time.
- **User-Friendly Interface**: Simple command-line prompts make the game easy to play.

## Installation

### Prerequisites

- **Python 3.12 or later**: Ensure you have Python installed on your system. You can download it from the [official website](https://www.python.org/downloads/).
- **UV**: Download and install UV from the [official website](https://docs.astral.sh/uv/getting-started/installation/). 

### Clone the Repository

```bash
git clone https://github.com/yourusername/math-quiz-game.git
cd math-quiz-game
```

### Install Dependencies

The game relies on the pytz library for timezone handling. Add it using uv:
```bash
uv add pytz
```

## Usage

Run the game using Python:
```bash
uv run main.py
```

