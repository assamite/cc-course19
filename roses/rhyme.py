from typing import Dict, List, Tuple

WORDS = ['crisscross', 'dos', 'chess', 'completed', 'depleted', 'hugged']


def rhyme(emotion: str, word_pairs: List[Dict[str, Tuple[str, str]]]):

    partials_and_rhymes = []
    for row in word_pairs:
        row['rhymes'] = [*WORDS]
        partials_and_rhymes.append(row)

    return partials_and_rhymes
