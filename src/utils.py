from typing import Any, List

from src.question import Question


def make_question_from_row(row: List[Any]) -> Question:
    return Question(row[0], row[1:-1], row[-1])
