"""Group Example's main file.

Should contain initialize- and create-functions.
"""
import random

import os
import sys

import numpy as np
from PIL import Image

__CURRENT_PROJECT_ROOT__ = os.path.dirname(os.path.realpath(__file__))
__GENERAL_PROJECT_ROOT__ = os.path.dirname(__CURRENT_PROJECT_ROOT__)

sys.path.append(__CURRENT_PROJECT_ROOT__)
sys.path.append(__GENERAL_PROJECT_ROOT__)

from resources.sample_inputs import SAMPLE_INPUTS


__GENERATED_DUMMY_DIR__ = os.path.join(__CURRENT_PROJECT_ROOT__, "dummies")
__IM_WIDTH__ = 800
__IM_HEIGHT__ = 600
__COLOR_CHANNELS__ = 3



class RandomImageCreator:

    def __init__(self, *args, **kwargs):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json.
        """
        print("Graphical group 01. \nInitialisation...")
        # self.alphabet = kwargs.pop('alphabet', "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        # self.vocals = kwargs.pop('vocals', "AEIOUY")
        # self.word_length = kwargs.pop('word_length', (4, 8))

        # Each creator should have domain specified: title, poetry, music, image, etc.
        self.domain = 'image'

    def generate(self, *args, **kwargs):
        """Generator function.
        """
        image_tensor = np.random.randint(low=0, high=256, size=(__IM_HEIGHT__, __IM_WIDTH__, 3))
        image = Image.fromarray(image_tensor, 'RGB')
        image_path = self.get_unique_save_path_name(directory=__GENERATED_DUMMY_DIR__,
                                                    basename="dummy",
                                                    extension="png")
        image.save(image_path, 'PNG')
        return image_path

    def get_unique_save_path_name(self, directory, basename, extension):
        i = 0
        tentative_path = os.path.join(directory, f"{basename}.{extension}")
        if not os.path.exists(tentative_path):
            return tentative_path

        while True:
            i += 1
            tentative_path = os.path.join(directory, f"{basename}_{i}.{extension}")
            if not os.path.exists(tentative_path):
                return tentative_path

    def evaluate(self, image_path):
        """Evaluate word by counting how many vocals it has.
        """
        image = Image.open(image_path)
        image_matrix = np.array(image, dtype=np.float)

        image_matrix /= 255.0
        return np.average(image_matrix)

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
        print("Graphical group 01.")
        ret = [(im, {'evaluation': self.evaluate(im)}) for im in [self.generate() for _ in range(number_of_artifacts)]]
        return ret

def test():
    print(f"__CURRENT_PROJECT_ROOT__: {__CURRENT_PROJECT_ROOT__}")
    print(f"__RESOURCES_FOLDER__: {__GENERAL_PROJECT_ROOT__}")
    print(f"SAMPLE_INPUTS: {SAMPLE_INPUTS}")
    im_creator = RandomImageCreator()
    print(im_creator.create())

if __name__ == "__main__":
    test()
