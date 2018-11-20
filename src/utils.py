import random
from typing import List


def random_definitions(definitions: List[str], correct: str, number: int) -> List[str]:
    result = [correct]
    for i in range(number - 1):
        while True:
            word = random.choice(definitions)
            if word in result:
                continue
            result.append(word)
            break
    random.shuffle(result)
    return result
