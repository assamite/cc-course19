from typing import Dict, List


def fill_and_create_text(emotion: str, rhyming_partials: List[Dict]):
    return [
        # f'Roses are red', f'{word_pair[0]} are {word_pair[1]}'
        ['Roses are red', f'{rp["word_pair"][0]} are {rp["word_pair"][1]}',
            f'this project is not done', f'and you should be {word}']
        for rp in rhyming_partials
        for word in rp['rhymes']
    ]
