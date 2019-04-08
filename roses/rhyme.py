from typing import Dict, List

WORDS = ['crisscross', 'dos', 'chess', 'completed', 'depleted', 'hugged']


def rhyme(emotion: str, word_pairs: Dict[str, List]):

    partials_and_rhymes = []
    for word_pair in word_pairs['word_pairs']:
        partials_and_rhymes.extend(
            [{'word_pair': word_pair, 'rhymes': [*WORDS]}]
        )

    return partials_and_rhymes
