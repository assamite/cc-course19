from typing import List, Tuple
from random import randint


def evaluate_poems(emotion: str, word_pairs: List[Tuple[str, str]], poems: List[List[str]]):
    """
    Evaluates given poems and gives them a score.
    """
    return list(zip(poems, [randint(1, 100) for x in range(len(poems))]))


# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [("people", "boss"), ("animal", "legged")]
    example_poems = [
        ["Roses are red", 
        "human is boss", 
        "this project is not done", 
        "and you should be closs"
        ],
        ["Roses are red", 
        "animal is legged", 
        "this project is not done", 
        "and you should be egged"
        ]
    ]
    output = evaluate_poems(example_emotion, example_word_pairs, example_poems)
    print(output)