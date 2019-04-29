from typing import List, Tuple


def generate_word_pairs(emotion: str, word_pairs: List[Tuple[str, str]]):
    """
    Generates a bunch of word pairs depending on input word pairs and emotion.
    """
    return [{'word_pair': (word_pair[0], word_pair[1]), 'verb': 'is'} for word_pair in word_pairs]
