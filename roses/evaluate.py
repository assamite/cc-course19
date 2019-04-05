from typing import List, Tuple


def evaluate_poems(emotion: str, word_pairs: List[Tuple[str, str]], poems: List[List[str]]):
    return list(zip(poems, [1 for x in range(len(poems))]))
