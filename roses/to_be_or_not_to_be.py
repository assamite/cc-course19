from typing import Tuple
import inflect


def fit_verb(word_pair: Tuple[str, str], verb: str):
    """
    Fits the verb to the word pair.
    """
    p = inflect.engine()
    if p.singular_noun(word_pair[0]) == False:
        return verb
    return p.plural_verb(verb)


# For testing
if __name__ == '__main__':
    example_verb = 'walks'
    example_word_pair = ("people", "boss")
    output = fit_verb(example_word_pair, example_verb)
    print(output)