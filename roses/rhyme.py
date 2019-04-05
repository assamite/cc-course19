from typing import List


def rhyme(emotion: str, partials: List[List[str]]):
    word = 'crisscross'
    return [{'partial': partial, 'rhymes': [word]} for partial in partials]
