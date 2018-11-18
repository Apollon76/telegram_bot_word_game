from dataclasses import dataclass


@dataclass
class User:
    id: int
    question_id: int
    points: int
