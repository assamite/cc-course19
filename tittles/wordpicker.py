import random
from nltk.corpus import wordnet as wn
try:
    from . import thesaurus
except ImportError:
    import thesaurus

class WordPicker():

    def __init__(self):
        self.thesaurus = thesaurus

    def find_pairs(self, adjectives, ncandidates=3):
        """
        Finds candidate adjectives and picks the best candidate
        Doesn't do much yet, is better suited for comparing words of the same POS
        """
        candidates = []
        scores = []
        animals = self.thesaurus.find_members('animal', adjectives)
        animal = random.choices(list(animals.keys()), list(animals.values()))[0]
        candidates = random.sample(adjectives, ncandidates)
        for i in range(ncandidates):
            candidate = candidates[i]
            oppositeness = self.get_oppositeness_score(animal, candidate)
            scores.append(oppositeness)
        adjective = candidates[scores.index(min(scores))]
        return((animal, adjective))

    def get_oppositeness_score(self, word1, word2):
        """
        Gets measure of how far words are from each other semantically, using WordNet
        Score of 0 is neutral
        Score of -0.5 means words are related (hyper- or hyponyms)
        Score of -1 means words are synonyms
        Score of 0.5 means words are semi-antonyms (hyper- or hyponym of antonym)
        Score of 1 means words are antonyms
        """
        opposites = []
        related = []
        antonym_related = []
        synsets = wn.synsets(word1)
        for synset in synsets:
            if word2 in synset.lemma_names():
                return -1
            for hypernym in synset.hypernyms():
                related.append(hypernym.lemmas()[0].name())
            for hyponym in synset.hyponyms():
                related.append(hyponym.lemmas()[0].name())
            for lemma in synset.lemmas():
                for antonym in lemma.antonyms():
                    opposites.append(antonym.name())
                    for hypernym in antonym.hypernyms():
                        antonym_related.append(hypernym.name())
                    for hyponym in antonym.hyponyms():
                        antonym_related.append(hyponym.name())
        if word2 in opposites:
            return 1
        if word2 in related:
            return -0.5
        if word2 in antonym_related:
            return 0.5
        return 0

