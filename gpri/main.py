"""Group GPRI's main file.

Contains initialize- and create-functions.
"""

import random
import os
from io import BytesIO
#import IPython.display
import numpy as np
import PIL.Image
import tensorflow as tf
import tensorflow_hub as hub
from gpri.gpri_helper import model
import cv2

class RandomImageCreator:

    def __init__(self, *args, **kwargs):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """
        print("Group GPRI initialize.")
        self.dims = kwargs.pop('resolution', [100, 100])
        self.folder = os.path.dirname(os.path.realpath(__file__))

        #tf.reset_default_graph()


        #initializer = tf.global_variables_initializer()
        #self.sess = tf.Session()
        #self.sess.run(initializer)

        # Each creator should have domain specified: title, poetry, music, image, etc.
        self.domain = 'image'

    def generate(self, *args, **kwargs):
        """Random image generator.
        """
        truncate=0.8
        noise=0
        n_samples=1
        idx_cat = args[0]
        z = model.truncated_z_sample(n_samples, 0.8, noise)
        y = idx_cat
        ims = model.sample(z, y, 0.8)
        cv2.imwrite("gpri/broken_sample.jpg", ims[0])
        return os.path.join(self.folder, "broken_sample.jpg")

    def evaluate(self, image):
        """Evaluate image. For now this is a dummy.
        """
        return 1

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
        with open("gpri/categories.txt", "r") as file:
            buffer = file.read()
            cat = buffer.split("\n")
        cat_indx = []
        for pairs in word_pairs[1]:
            noun = pairs
            print(noun)
            if noun == "animal":
                idxs =[i for i in range(0,398)]
            elif noun == "activity":
                idxs =[i for i in range(398,1000)]
            else:
                idxs = -1
            if idxs == -1:
                print("Category not available yet as, category annotation is pending.... (Try animal/activity only)")
            else:
                import random
                idx_cat = int(random.choice(idxs))
            ret = [(w, {'evaluation': self.evaluate(w)}) for w in [self.generate(idx_cat) for _ in range(number_of_artifacts)]]
        return ret
