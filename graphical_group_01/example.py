"""Group Example's main file.

Contains init and create functions.
"""
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
__IMAGE_WIDTH__ = 800
__IMAGE_HEIGHT__ = 600
__COLOR_CHANNELS__ = 3


class RandomImageCreator:

    def __init__(self, *args, **kwargs):
        """Initialises the class.

        Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Parameters
        ----------
        args: tuple
            arguments

        kwargs: dict
            keywords arguments

        Notes
        -----
        Only keyword arguments are supported in config.json.

        """
        self.domain = 'image'
        self.group_name = 'Graphical group 01'
        print(f"{self.group_name}... Initialised!")

    def generate(self, *args, **kwargs):
        """Generates artifacts as random images.

        Saves a new image under the 'dummies' directory and returns its path.

        Parameters
        ----------
        args: tuple
            arguments

        kwargs: dict
            keywords arguments

        Returns
        -------
        str:
            path to the generated image

        """
        image_tensor = np.random.randint(low=0, high=256, size=(__IMAGE_HEIGHT__,
                                                                __IMAGE_WIDTH__,
                                                                __COLOR_CHANNELS__))
        image = Image.fromarray(image_tensor, 'RGB')
        image_path = self.get_unique_save_path_name(directory=__GENERATED_DUMMY_DIR__,
                                                    basename="dummy",
                                                    extension="png")
        image.save(image_path, 'PNG')
        return image_path

    def get_unique_save_path_name(self, directory, basename, extension):
        """Generates a unique filename under the given directory.

        Parameters
        ----------
        directory: str
            path where the file is intended to be saved

        basename: str
            base part of the name to which a suffix can be added

        extension: str
            type of file extension

        Returns
        -------
        str:
            unique pathname including directory and unique filename

        """
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
        """Evaluates the goodness of an image artifact by its scaled average.

        Parameters
        ----------
        image_path: str
            path to an image that is supported by PIL

        Returns
        -------
        float:
            value grade for the artifact

        """
        image = Image.open(image_path)
        image_matrix = np.array(image, dtype=np.float)

        image_matrix /= 255.0
        return np.average(image_matrix)

    def create(self, emotion, word_pairs, number_of_artifacts=10, **kwargs):
        """Creates and evaluates artifacts in the group's domain.

        The given inputs can be parsed and deciphered by the system using any methods available.


        Parameters
        ----------
        emotion: str
            One of "the six basic emotions": anger, disgust, fear, happiness, sadness or surprise.
            The emotion should be perceivable in the output(s).

        word_pairs: list of tuple of str
            List of 2-tuples, the word pairs associated with the output(s). The word_pairs are (noun, property) pairings
            where each pair presents a noun and its property which may be visible in the output. (Think of more creative
            ways to present the pairings than literal meaning.)

        number_of_artifacts: int (optional)
            Number of artifacts returned. Defaults to 10.

        kwargs: dict
            keywords arguments

        Returns
        -------
        list of tuple
            The function returns a list in the following form:

            [
                (artifact_1, {"evaluation": 0.76, 'foo': 'bar'}),
                (artifact_2, {"evaluation": 0.89, 'foo': 'baz'}),
                .
                .                  .
                .                                         .
                (artifactn, {"evaluation": 0.29, 'foo': 'bax'})
            ]

        """
        basic_emotions = ["anger", "disgust", "fear", "happiness", "sadness", "surprise"]
        if emotion not in basic_emotions:
            raise ValueError(f"Argument 'emotion'='{emotion}'' is not accepted. Accepted values are: {basic_emotions}.")

        print("")
        ret = [(im, {'evaluation': self.evaluate(im)}) for im in [self.generate() for _ in range(number_of_artifacts)]]
        return ret


def test():
    print(f"__CURRENT_PROJECT_ROOT__: {__CURRENT_PROJECT_ROOT__}")
    print(f"__RESOURCES_FOLDER__: {__GENERAL_PROJECT_ROOT__}")
    im_creator = RandomImageCreator()
    print(im_creator.create(emotion='happiness',
                            word_pairs=[("akku", "ankka")]))


if __name__ == "__main__":
    test()
