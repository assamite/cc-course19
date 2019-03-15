"""Group Example's main file.

Should contain initialize- and create-functions.
"""
import os
import time

import cv2
import numpy as np


class RandomTeamImageGenerator:

    def __init__(self, *args, **kwargs):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """
        print("Random team fancy image generator initialization started")
        self.path_to_dummy_image = "dummy.jpg"

        # Each creator should have domain specified: title, poetry, music, image, etc.
        self.domain = 'image'
        self.path_to_group_folder = os.path.dirname(os.path.realpath(__file__))
        print("Initialization is finished")

    def generate(self, *args, **kwargs):
        """Random image generator.
        """

        # Read dummy image
        dummy_image = cv2.imread(os.path.join(self.path_to_group_folder, self.path_to_dummy_image), cv2.IMREAD_COLOR)
        random_variable = np.random.randint(1, 3)
        if random_variable == 1:
            print("Creating HSV image")
            hsv_transformed = cv2.cvtColor(dummy_image, cv2.COLOR_BGR2HSV)
            created_image_path = os.path.join(self.path_to_group_folder, str("%s.%s.jpg" % (time.time(), "hsv")))
            print("Image is saved to %s" % created_image_path)
            cv2.imwrite(created_image_path, hsv_transformed)
        elif random_variable == 2:
            print("Creating Grayscale image")
            created_image_path = os.path.join(self.path_to_group_folder, str("%s.%s.jpg" % (time.time(), "grayscale")))
            print("Image is saved to %s" % created_image_path)
            grayscale_transformed = cv2.cvtColor(dummy_image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(created_image_path, grayscale_transformed)
        return created_image_path

    def evaluate(self, word):
        """Evaluate word by counting how many vocals it has.
        """
        return word is not None

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
        print("Group Example create with input args: {} {}".format(emotion, word_pairs))
        ret = [(w, {'evaluation': self.evaluate(w)}) for w in [self.generate() for _ in range(number_of_artifacts)]]
        return ret
