import random
from nltk.corpus import wordnet as wn
try:
    from . import thesaurus
except ImportError:
    import thesaurus

class WordPicker():

    def __init__(self):
        self.thesaurus = thesaurus

    def find_pairs(self, adjectives, tags):
        """
        Finds 2 candidates for each slot of adjectives and nouns and picks the best combination (4 combinations with 2 slots)
        tags: 0 = adjective, 1 = noun, 2 = person, 3 = location
        Todo: add singular/plural checking
        """
        candidates = []
        scores = []
        tag_list = ['ADJ', 'NP', 'PERSON', 'LOC']
        for i in range(4):
            tag = tag_list[i]
            for slot in tags[tag]:
                if i == 0:
                    candidates.append(self.get_adjective())
                if i == 1:
                    candidates.append(self.get_noun('animal', adjectives[0]))
                if i == 2:
                    candidates.append(self.get_noun('person', adjectives[1]))
                if i == 3:
                    #todo: get location nuances for adjectives instead
                    candidates.append(self.get_noun('location', adjectives[1]))
        #If template has only one slot, no need to get oppositeness score
        if len(candidates) == 1:
            return candidates[0][0]

        candidate_pairs = [(candidates[0][0], candidates[1][0]), (candidates[0][0], candidates[1][1]), (candidates[0][1], candidates[1][0]), (candidates[0][1], candidates[1][1])]
        for i in range(len(candidate_pairs)):
            candidate = candidate_pairs[i]
            oppositeness = self.get_oppositeness_score(candidate[0], candidate[1])
            scores.append(oppositeness)
        word_pair = candidate_pairs[scores.index(min(scores))]

        return word_pair

    def get_adjective(self):
        """
        Returns two candidates for adjective
        Todo: implement fetching nuance adjectives from thesaurus rex
        """
        return ("black", "white")

    def get_noun(self, category, adjectives):
        """
        Returns two candidates for adjective
        """
        candidates = self.thesaurus.find_members(category, adjectives)
        return random.sample(list(candidates), 2)


    def get_oppositeness_score(self, word1, word2):
        """
        Gets measure of how far words are from each other semantically, using WordNet
        Score of 0.5 means words are related (hyper- or hyponyms) or semi-antonyms (hyper- or hyponym of antonym)
        Score of 1 means words are antonyms or synonyms
        If words are none of these things, wordnet path similarity is used
        Default score: 0
        """
        if word1 == word2:
            return 0
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
        synsets2 = wn.synsets(word2)
        if len(synsets) == 0 or len(synsets2) == 0:
            return 0
        synset1 = synsets[0]
        synset2 = synsets2[0]
        wn_similarity = wn.path_similarity(synset1, synset2)
        if wn_similarity == None:
            return 0
        return wn_similarity
