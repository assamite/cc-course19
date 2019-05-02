from typing import Dict, List
import json
import random
import os
from roses.utils import read_json_file # works with main.py
# from utils import read_json_file # works with roses.py
import string

def find_lines(emotion: str, rhyming_partials: List[Dict]):
    """
    Creates combinations of ending lines (3rd and 4th) from some knowledgebase.
    """

    data = read_json_file("data/bible_kjv_wrangled.json")
    
    # There probably is a better/faster way to do this using dictionaries but I dont know how rn
    keys = []
    sentences = []
    last_word_of_sentences = []
    
    for key, value in data.items():
        keys.append(key)
        sentences.append(value)
        last_word_of_sentence = value.translate(str.maketrans('', '', string.punctuation))
        last_word_of_sentence = last_word_of_sentence.strip().split(' ')[-1]
        last_word_of_sentences.append(last_word_of_sentence.lower())

    
 

    ret = []
    for partial in rhyming_partials:
        for word in partial['rhymes']:
            rhyming_sentences = []
            indices = [i for i, x in enumerate(last_word_of_sentences) if x == word]
            if indices:
                for ix in indices:
                    rhyming_sentences.append(keys[ix])



            third = data[random.choice(list(data))]

            # selects rhyming sentence if there is at least one, else select random sentence as before
            if rhyming_sentences:
                fourth = data[random.choice(rhyming_sentences)]
            else:
                continue
            
            new_partial = partial.copy()
            new_partial['rest'] = (third, fourth)
            ret.append(new_partial)
    return ret


# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_rhyming_partials = [{'word_pair': ('animal', 'legged'), 'verb': 'is', 'rhymes': [
        'gielgud', 'rugged', 'ragged', 'begged', 'pegged']}]
    output = find_lines(example_emotion, example_rhyming_partials)
    print(output)
