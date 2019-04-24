"""Group Example's main file.

Contains init and create functions.

Test it with (from repo root): "python3 main.py -c graphical_group_01/main_config.json"
"""
import sys

from kolme_musaa import settings as s
from kolme_musaa.utils import debug_log
from kolme_musaa.main import run_pipeline

sys.path.append(s.__KOLME_MUUSAA_PROJECT_ROOT__)
sys.path.append(s.__GENERAL_PROJECT_ROOT__)


class KolmeMuusaaInterface:

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
        debug_log(f"{self.group_name}... Initialised!")


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
            Number of artifacts to be returned. Defaults to 10. If the number of word pairs is lower,
            it then uses that value instead.

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

        debug_log(f"Receiving:\n"
                  f"- emotion: {emotion}\n"
                  f"- word_pairs: {word_pairs}\n"
                  f"- number_of_artifacts: {number_of_artifacts}")
        # ret = [(im, {'evaluation': self.evaluate(im)})
        #        for im in [self.generate(emotion=emotion, word_pair=wp)
        #                   for wp in word_pairs]]
        return run_pipeline(emotion, word_pairs, number_of_artifacts)


def test():
    import subprocess
    command = f"{sys.executable} main.py -c graphical_group_01/main_config.json"
    command_list = command.split(" ")
    print(f"Running `{command}` ...")
    subprocess.run(command_list, cwd=s.__GENERAL_PROJECT_ROOT__)


if __name__ == "__main__":
    test()
