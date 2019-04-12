from typing import Dict, List


def find_lines(emotion: str, rhyming_partials: List[Dict]):
    """
    Creates combinations of ending lines (3rd and 4th) from some knowledgebase.
    """

    ret = []
    for partial in rhyming_partials:
        for word in partial['rhymes']:
            third = 'this project is not done'
            fourth = f'and you should be {word}'
            partial['rest'] = (third, fourth)
            ret.append(partial)
    return ret