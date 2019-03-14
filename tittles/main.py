

class tittlesTitle():
    def __init__(self):
        self.threshold = 0.8

    def generate(self, *args, **kwargs):
        return self.create("", {}, number_of_artifacts=1)

    def evaluate(self, title):
        return 1.

    def create(self, emotion, word_pairs, number_of_artifacts=10, **kwargs):

        ret = []

        while len(ret) != number_of_artifacts:
            # get synonyms
            # get template
            # morphology
            v = self.evaluate("")
            if v >= self.threshold:
                ret.append(":)")

        return ",".join(ret)
