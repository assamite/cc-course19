from typing import Dict, List, Tuple
import string
import nltk 
import os
import sys

nltk.download('cmudict')

WORDS = ['crisscross', 'dos', 'chess', 'completed', 'depleted', 'hugged']

# this is a placeholder because I dont know to get it from generate_rhyming_words(emotion: str, word_pairs: List[Dict[str, Tuple[str, str]]]) 
LASTWORDLINE2 = "help"  

def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
        
    return rhymes

def doTheyRhyme(word1, word2):
    if word1.find(word2) == len(word1) - len(word2):
        return False
    if word2.find(word1) == len(word2) - len(word1): 
        return False

    return word1 in rhyme(word2, 1)

# setting how strict the rhyme has to be, can be changed
def define_strictness_of_rhyme(wordToRhyme):
    strictness = 3
    if len(LASTWORDLINE2) < 4:
            strictness = 2

def generate_rhyming_words(emotion: str, word_pairs: List[Dict[str, Tuple[str, str]]]):
    """
    Finds possible rhyming words for the ending of line 2
    """

    partials_and_rhymes = []
    for row in word_pairs:
        strictness = define_strictness_of_rhyme(LASTWORDLINE2)
        row['rhymes'] = [rhyme(LASTWORDLINE2,strictness)]
        partials_and_rhymes.append(row)

    return partials_and_rhymes
