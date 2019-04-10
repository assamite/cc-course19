from typing import Dict, List


def alter_rest(emotion: str, rhyming_partials: List[Dict]):
    """
    Alters the third and fourth lines to be more creative.
    """
    ret = []
    for partial in rhyming_partials:
        third = partial['rest'][0]
        fourth = partial['rest'][1]
        ret.append(partial)

    return ret
