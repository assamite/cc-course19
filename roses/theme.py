from typing import List, Tuple


def theme(emotion: str, word_pairs: List[Tuple[str, str]]):
    return [[f'Roses are red', f'{word_pair[0]} are {word_pair[1]}'] for word_pair in word_pairs]
