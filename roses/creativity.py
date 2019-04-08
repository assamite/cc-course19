from typing import Dict, List


def creativity(emotion: str, rhyming_partials: List[Dict]):
    return [
        [rp['partial'][0], rp['partial'][1], f'this project is not done', f'and you should be {word}']
        for rp in rhyming_partials
         for word in rp['rhymes']
          ]
