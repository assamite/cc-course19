from typing import List


def rhyme(emotion: str, partials: List[List[str]]):
    words = ['crisscross', 'dos', 'chess']
    return [{'partial': partial, 'rhymes': [*words]} for partial in partials]
