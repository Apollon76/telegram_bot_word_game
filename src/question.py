from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    text: str
    options: List[str]
    correct: int
