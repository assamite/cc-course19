import cmudict
import pickle
import os
import random

class Evaluator():
    def __init__(self):
        self.cmudict = cmudict.dict()

        self.title_bank = None
        self.folder = os.path.dirname(os.path.realpath(__file__))

        # Try reading content for the title_bank
        
        try:
            with open(os.path.join(self.folder, "data", "titles.pickle"), "rb") as f:
                self.title_bank = pickle.load(f)
        
        except FileNotFoundError:
            from title_scrape import download_gutenberg, gutenberg_preprocess
        
            download_gutenberg()
            gutenberg_preprocess()
        
            with open(os.path.join(self.folder, "data", "titles.pickle"), "rb") as f:
                self.title_bank = pickle.load(f)

        self.pref_novelty, self.pref_alliteration = self.__learn_preference(sample_size=100)


    def __learn_preference(self, sample_size=100):
        """
        Learns preference weights from the title_bank.

        Returns:
            tuple : weights for novelty and alliteration.
        """

        universe = set(self.title_bank.keys())
        
        sample = random.sample(universe, sample_size)
        
        # Learn novelty
        # print("Learning novelty preference for titles")
        dists = []

        for tid in list(sample):

            # From tid to title
            title = self.title_bank[tid]["title"].strip()

            closest = 1000
            
            # Create subsample
            subsample = set(sample)
            subsample.remove(tid)

            for cid in list(subsample):
                # Skip candidates using lower-bound of the levenshtein distance.
                # Does not take the weights into account
                comparable = self.title_bank[cid]["title"].strip()

                if abs(len(title) - len(comparable)) > closest:
                    continue

                levenshtein = self.__iterative_levenshtein(title, comparable)
                closest = min(closest, levenshtein)
            
            dists.append(closest)

        # print("Learning alliteration preference for titles")

        alliterations = [self.eval_alliteration(self.title_bank[tid]["title"].strip().split(" ")) for tid in sample]


        # Find combination for the preferences
        observed_aestetics = []

        for nov, alli in zip(dists, alliterations):
            scaled_nov = nov / max(dists)
            scaled_alli = alli / max(alliterations)

            aestetic = scaled_alli + scaled_nov

            weight_nov = scaled_nov/aestetic
            weight_alli = scaled_alli/aestetic

            observed_aestetics.append((aestetic, (weight_nov, weight_alli)))

        observed_aestetics = sorted(observed_aestetics, key=lambda x: x[0])

        # Choose preferred aestetic
        # Prefer artifacts close to 90th percentile
        preferred_aestetic = observed_aestetics[-int(len(observed_aestetics)/10)]
        novelty, alliteration = preferred_aestetic[1]

        return (novelty, alliteration)


    # Modified from https://www.python-course.eu/levenshtein_distance.php
    def __iterative_levenshtein(self, s, t, weights=(1, 1, 1)):
        """ 
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings 
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein 
        distance between the first i characters of s and the 
        first j characters of t

        weight_dict: keyword parameters setting the costs for characters,
                     the default value for a character will be 1
        """
        rows = len(s)+1
        cols = len(t)+1


        dist = [[0 for x in range(cols)] for x in range(rows)]
        # source prefixes can be transformed into empty strings 
        # by deletions:
        for row in range(1, rows):
            dist[row][0] = dist[row-1][0] + weights[0]
        # target prefixes can be created from an empty source string
        # by inserting the characters
        for col in range(1, cols):
            dist[0][col] = dist[0][col-1] + weights[1]

        for col in range(1, cols):
            for row in range(1, rows):
                deletes = weights[0]
                inserts = weights[1]
                subs = max( (weights[2], weights[2]))
                if s[row-1] == t[col-1]:
                    subs = 0
                else:
                    subs = subs
                dist[row][col] = min(dist[row-1][col] + deletes,
                                     dist[row][col-1] + inserts,
                                     dist[row-1][col-1] + subs) # substitution

        return dist[row][col]


    def editDistance(self, phenotype, weights=(1, 1, 1)):
        """
        Calculate the shortest levenshtein distance between phenotype and known titles.

        Args:
            phenotype (str) : Candidate phenotype.
            title_bank (dict) : Known titles, needs to have dictionaries as values, and those disctionaries need to have
                                'title' key.
            weights (tuple of floats) : Weights for different operations. In order: Delete, Insert, Substitute

        Returns:
            int : Shortest edit distance.
        """

        # Checking for exact match from the dictionary is fast
        if phenotype in self.title_bank:
            return 0

        closest = 1000

        for _, b_info in self.title_bank.items():
            # Skip candidates using lower-bound of the levenshtein distance.
            # Does not take the weights into account
            if abs(len(phenotype.strip()) - len(b_info["title"].strip())) > closest:
                continue

            levenshtein = self.__iterative_levenshtein(phenotype.strip(), b_info["title"].strip(), weights)
            closest = min(closest, levenshtein)

        return closest

    def evaluate(self, title):
        """Runs the different evaluation schemes, which return values between 0 and 1, and returns an average over them.
        
        Args:
            title (list) : list of words forming the title when.

        Returns:
            float : Weighted average of the different evaluations.
        """
        nov = self.eval_novelty(" ".join(title))*self.pref_novelty
        alli = self.eval_alliteration(title)*self.pref_alliteration
        return nov + alli


    def eval_novelty(self, title):
        if self.title_bank is None:
            return 0.8
        else:
            dist = self.editDistance(title, (1, 1, 1))
            # Scale with the title length
            # Can be higher than 1 if weights are not all 1.
            dist = min(1.0, dist/len(title))
            return dist


    def eval_alliteration(self, title):
        unique_phonemes = []
        title_length = 1
        for word in title:
            try:
                phonemes = self.cmudict[word][0]
                title_length += len(phonemes)
                for phoneme in phonemes:
                    if phoneme not in unique_phonemes:
                        unique_phonemes.append(phoneme)
            except:
                #word was not in dict
                continue
        return len(unique_phonemes) / title_length


    def get_alliteration_score(self, ratio):
        """ A function that has it maximum = 1 when ratio is 1/2, meaning half of the phonemes in the
        title are non-unique, otherwise it grows close to 0
        """
        return max(0., 1 - (abs(ratio-0.5))**4)
