"""Group Example's main file.

Should contain initialize- and create-functions.
"""
import os
from typing import List, Tuple

from .fgen import generate_face, create_noise_vector, select_image
from .pgen import generate_portrait, evaluate_portrait

"""
This global variable will store feedback of face emotion evaluation
This storage could be useful if this feedback is somehow cumulative
"""
FACE_GENERATION_FEEDBACK = None


class RandomTeamImageGenerator:

    def __init__(self, *args, **kwargs):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """
        print("Random team fancy image generator initialization started")

        # Each creator should have domain specified: title, poetry, music, image, etc.
        self.domain = 'image'

        # This code gets an absolute path to our group folder
        # Please, note, that we should use only absolute paths
        # So use this folder path for all files which we read/write in our code
        self.path_to_group_folder = os.path.dirname(os.path.realpath(__file__))
        print("Initialization is finished")

    def generate_face(self, emotion: str, word_pairs: List[Tuple[str, str]], output_folder, **kwargs):
        global FACE_GENERATION_FEEDBACK
        generated_face = generate_face(create_noise_vector(emotion, word_pairs, FACE_GENERATION_FEEDBACK), select_image(emotion, word_pairs, FACE_GENERATION_FEEDBACK), output_folder)
        return generated_face

    def evaluate_emotion(self, face_image):
        """Evaluate word by counting how many vocals it has.
        """
        return face_image is not None

    def create(self, emotion: str, word_pairs: List[Tuple[str, str]], number_of_artifacts=10, **kwargs):
        global FACE_GENERATION_FEEDBACK
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
        FACE_GENERATION_FEEDBACK = [(face, self.evaluate_emotion(face)) for face in [self.generate_face(emotion, word_pairs, self.path_to_group_folder) for _ in range(number_of_artifacts)]]
        generated_portraits = [generate_portrait(face, emotion, word_pairs) for face, evaluation in FACE_GENERATION_FEEDBACK]
        return [(portrait, {'evaluation': evaluate_portrait(portrait)}) for portrait in generated_portraits]
