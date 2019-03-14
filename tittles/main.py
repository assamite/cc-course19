

class tittlesTitle():
    def __init__(self):
        pass

    def generate(self, *args, **kwargs):
        pass

    def evaluate(self, title):
        return 1.

    def create(self, emotion, word_pairs, number_of_artifacts=10, **kwargs):

        ret = []

        while len(ret) != number_of_artifacts:
            # get synonyms
            # get template
            # morphology
            v = self.evaluate("")
            if v >= 0.8:
                ret.append(":)")

        return ",".join(ret)
