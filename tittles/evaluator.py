import cmudict
import pickle
import os
import random
import csv
from operator import add
import math

import logging
logger = logging.getLogger(__name__)

class Evaluator():
    TITLE_DUMP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "titles.pickle")
    SENTIMENT_LEXICON_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "EmotionLexicon.txt")

    def __init__(self):
        self.emotions = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']

        self.cmudict = cmudict.dict()

        self.title_bank = None

        # Try reading content for the title_bank

        try:
            with open(self.TITLE_DUMP_PATH, "rb") as f:
                self.title_bank = pickle.load(f)

        except FileNotFoundError:
            from title_scrape import download_gutenberg, gutenberg_preprocess

            download_gutenberg()
            gutenberg_preprocess()

            with open(self.TITLE_DUMP_PATH, "rb") as f:
                self.title_bank = pickle.load(f)

        #Read content for the sentiment dictionary
        self.sentimentDictionary = {}
        with open(self.SENTIMENT_LEXICON_PATH) as emotionLexicon:
            lexicon = csv.reader(emotionLexicon, delimiter='\t')
            word = ""
            values = {}
            for row in lexicon:
                if word != row[0]:
                    self.sentimentDictionary[word] = values
                    word = row[0]
                    values = {}
                values[row[1]] = row[2]

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

        print("Learned following weights (nov, alli)")
        print(novelty, alliteration)

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

    def add_title(self, title):
        """
        Save the given title as one that has been observed before.

        Args:
            title (str) : Title to be added.

        Returns:
            Boolean : True if title was saved succesfully.
        """
        assert(isinstance(title, str))

        if self.title_bank is None:
            return False

        # Generate a random key for the title
        used_keys = set(self.title_bank.keys())

        if len(used_keys) == 1500000:
            # Close to exhausted space
            return False

        key = None

        while key is None:
            candidate = random.randint(-1000000, 1000000)
            if candidate not in used_keys:
                key = candidate

        self.title_bank[key] = {"title": title}
        return True


    def dump_titles(self):
        """
        Saves the current known titles to a local file.

        Returns:
            None
        """
        # Overwrite previous file
        with open(self.TITLE_DUMP_PATH, "wb") as f:
            pickle.dump(self.title_bank, f)

    def edit_distance(self, phenotype, weights=(1, 1, 1)):
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

    def evaluate(self, title, emotion):
        """Runs the different evaluation schemes, which return values between 0 and 1, and returns an average over them.

        Args:
            title (list) : list of words forming the title when.

        Returns:
            float : Weighted average of the different evaluations.
        """

        logger.debug("input " + str(title))

        # Refuse titles that are not accepted by eval_numbers.
        # Allows to skip expensive novelty checking
        if self.eval_numbers(" ".join(title)) == 0.0:
            logger.debug("too many numbers in title")
            return 0.
        if len(" ".join(title)) > 55:
            logger.debug("title too long")
            return 0.

        nov = self.eval_novelty(" ".join(title))
        print("     Novelty: {}".format(nov))
        w_nov = nov*self.pref_novelty
        logger.debug(f"novelty {nov}")
        logger.debug(f"weighted novelty {w_nov}")

        alli = self.eval_alliteration(title)
        w_alli = alli*self.pref_alliteration
        logger.debug(f"alliteration {alli}")
        logger.debug(f"weighted alliteration {w_alli}")

        # Sentiment values seem to be consistently around 0.6, scale up closer to one.
        # Still make sure, that value is not over 1.0
        senti = self.eval_sentiment(title, emotion)
        print("     Sentiment: {}".format(senti))
        w_senti = min(1.0, senti*1.4)
        logger.debug(f"sentiment {senti}")
        logger.debug(f"weighted sentiment {w_senti}")

        # Novelty & Alliteration are weighted against each other to result in 1.0 weight together.
        # Sentiment has 1.0 weight at the moment, so scale everything down in same fractions, so that output range [0,1]
        result = (w_nov + w_alli)*0.5 + (w_senti*0.5)
        logger.debug(f'final evaluation {result}')

        return result

    def eval_novelty(self, title):
        if self.title_bank is None:
            return 0.8
        else:
            dist = self.edit_distance(title, (1, 1, 1))
            # Scale with the title length
            # Can be higher than 1 if weights are not all 1.
            dist = min(1.0, dist/len(title))
            return dist


    def eval_alliteration(self, title):
        unique_phonemes = []
        title_length = 0

        for word in title:

            word = word.lower()
            word = word.replace(":", "")
            word = word.replace("'", "")
            word = word.replace(";", "")
            word = word.replace(";", "")
            word = word.replace(".", "")
            word = word.replace("!", "")
            word = word.replace("?", "")

            try:
                phonemes = self.cmudict[word][0]
                title_length += len(phonemes)
                for phoneme in phonemes:
                    if phoneme not in unique_phonemes:
                        unique_phonemes.append(phoneme)
            except IndexError:
                #word was not in dict
                continue

        try:
            ratio = len(unique_phonemes) / title_length
        except ZeroDivisionError:
            ratio = 0.

        return self.get_alliteration_score(ratio)


    def get_alliteration_score(self, ratio):
        """ A function that has it maximum = 1 when ratio is 1/2, meaning half of the phonemes in the
        title are non-unique, otherwise it grows close to 0
        """
        return max(0., 1 - (abs(ratio-0.5))**4)

    def eval_sentiment(self, title, emotion):
        """
        Builds a vector of emotions in the title and compares that vector to the emotion in the input
        Each word gets a weight of 1/n, where n is the number of words in the title
        """
        self.emotions = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']
        goal_sentiment = list(map(lambda x: int(x == emotion), self.emotions))
        self.emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']
        title_sentiment = [0, 0, 0, 0, 0, 0]
        for word in title:
            sentiments = self.sentimentDictionary.get(word.lower(), None)
            if sentiments is not None:
                word_sentiment = list(map(lambda x: int(sentiments[x]), self.emotions))
                title_sentiment = list(map(add, title_sentiment, word_sentiment))
        title_sentiment = list(map(lambda x: x/len(title), title_sentiment))
        return self.get_sentiment_vector_diff(goal_sentiment, title_sentiment)

    def get_sentiment_vector_diff(self, goal, sentiment):
        """
        Take squared difference of vectors
        """
        diff = 0
        for i in range(len(self.emotions)):
            diff += (goal[i] - sentiment[i])**2
        #Normalize to range 0-1 and take complement, since small difference is good
        return 1 - math.sqrt(diff)/math.sqrt(6)


    def eval_numbers(self, title):
        digits = 0
        for character in title:
            if str.isdigit(character):
                digits += 1
        if digits > 3:
            # Refuse more than 3 digits
            return 0.
        return 1 - (digits / (digits + len(title)))
