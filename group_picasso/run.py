"""Group Example's main file.

Should contain initialize- and create-functions.
"""

import os


class RandomImageCreator:

    def __init__(self, *args, **kwargs):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """

        print("Group Example initialize.")

        # Each creator should have domain specified: title, poetry, music, image, etc.
        self.domain = 'image'
        self.folder = os.path.dirname(os.path.realpath(__file__))

    def generate(self, *args, **kwargs):
        """Random image generator.
        """

        return os.path.join(self.folder, 'picasso.jpg')

    def evaluate(self, image):
        """Evaluate image.
        """

        return 0

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

        img = self.generate()
        return [(img, {"evaluation": self.evaluate(img)})]
