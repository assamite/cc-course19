from typing import Dict, List, Tuple

WORDS = ['crisscross', 'dos', 'chess', 'completed', 'depleted', 'hugged']


def generate_rhyming_words(emotion: str, word_pairs: List[Dict[str, Tuple[str, str]]]):
    """
    Finds possible rhyming words for the ending of line 2
    """

    partials_and_rhymes = []
    for row in word_pairs:
        row['rhymes'] = [*WORDS]
        partials_and_rhymes.append(row)

    return partials_and_rhymes
