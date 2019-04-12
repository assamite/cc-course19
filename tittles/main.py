import random
import os
import pickle
from pattern.en import pluralize, singularize

try:
    from .templates import TemplateBank, Title
except ModuleNotFoundError:
    from templates import TemplateBank, Title

try:
    from .evaluations import editDistance
except ModuleNotFoundError:
    from evaluations import editDistance


class tittlesTitle():
    def __init__(self):
        self.threshold = 0.8
        self.domain = 'word'
        self.folder = os.path.dirname(os.path.realpath(__file__))

        self.template_bank = TemplateBank(os.path.join(self.folder, "data", "templates.short.uniq"))

        self.title_bank = None

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


    def generate(self, *args, **kwargs):
        return self.create("", {}, number_of_artifacts=1)

    def evaluate(self, title):
        """
        Evaluates given title to [0,1] range. 1 being best possible value.

        Args:
            Title (str) : title to be evaluated.

        Returns:
            Float [0, 1] : How good the title was - high being better.
        """
        if len(title) == 0:
                # Empty title
                return 0.

        if self.title_bank is None:
            return 0.8
        else:
            dist = editDistance(title, self.title_bank, (1, 1, 1))
            # Scale with the title length
            # Can be higher than 1 if weights are not all 1.
            dist = min(1, (dist/len(title))*(len(title)//5))
            return dist
        

    def inject(self, title, word_pair):
        for i, cat in title.get_slots('NP'):
            if cat == 'plural':
                title.inject(pluralize(word_pair[0]).capitalize(), 'NP')
            else:
                title.inject(singularize(word_pair[0]).capitalize(), 'NP')
        for i, cat in title.get_slots('ADJ'):
            title.inject(word_pair[1], 'ADJ')

    def create(self, emotion, word_pairs, number_of_artifacts=10, **kwargs):
        """Create artifacts in the group's domain.

        The given inputs can be parsed and deciphered by the system using any methods available.

        The function should return a list in the form of:

            [
                (artifact1, {"evaluation": 0.76, 'foo': 'bar'}),
                (artifact2, {"evaluation": 0.89, 'foo': 'baz'}),
                # ...
                (artifactn, {"evaluation": 0.29, 'foo': 'bax'})
            ]

        :param str emotion:
            One of "the six basic emotions": anger, disgust, fear, happiness, sadness or surprise.
            The emotion should be perceivable in the output(s).
        :param list word_pairs:
            List of 2-tuples, the word pairs associated with the output(s). The word_pairs are (noun, property) pairings
            where each pair presents a noun and its property which may be visible in the output. (Think of more creative
            ways to present the pairings than literal meaning.)
        :param int number_of_artifacts:
            Number of artifacts returned
        :returns:
            List with *number_of_artifacts* elements. Each element should be (artifact, metadata) pair, where metadata
            should be a dictionary holding at least 'evaluation' keyword with float value.

        """

        ret = []

        while len(ret) != number_of_artifacts:
            # TODO: get synonyms
            word_pair = random.choice(word_pairs)
            template = self.template_bank.random_template()
            title = Title(template)
            self.inject(title, word_pair)
            title = str(title)
            v = self.evaluate(title)
            if v >= self.threshold:
                ret.append((title, {"evaluation": v}))

        return ret

if __name__ == "__main__":
    import pprint
    import sys
    sys.path.insert(0,'..')
    import inputs
    pp = pprint.PrettyPrinter(indent=2)
    emotion, word_pairs = inputs.get_input(False)
    T = tittlesTitle()
    print('INPUT')
    pp.pprint({'emotion': emotion, 'word_pairs': word_pairs})
    print('')
    print('OUTPUT')
    pp.pprint(T.create(emotion, word_pairs, number_of_artifacts=3))
