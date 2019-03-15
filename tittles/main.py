

class tittlesTitle():
    def __init__(self):
        self.threshold = 0.8
        self.domain = 'word'

    def generate(self, *args, **kwargs):
        return self.create("", {}, number_of_artifacts=1)

    def evaluate(self, title):
        return 1.

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
            # get synonyms
            # get template
            # morphology
            v = self.evaluate("")
            if v >= self.threshold:
                ret.append((":)", {"evaluation": v}))

        return ret

if __name__ == "__main__":
    T = tittlesTitle()
    print(T.create("", {}, number_of_artifacts=3))
