"""Group GPRI's main file.

Contains initialize- and create-functions.
"""

import random
import os
from io import BytesIO
import IPython.display
import numpy as np
import random
import PIL.Image
from scipy.stats import truncnorm
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import tensorflow_hub as hub
import cv2
import time

GPU_MODE = False


animal_idxs =[i for i in range(0,398)]
activity_idxs =[i for i in range(398,1000)]


class RandomImageCreator:

    def __init__(self, *args, **kwargs):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """
        print("Group GPRI initialize.")

        # Each creator should have domain specified: title, poetry, music, image, etc.
        self.domain = 'image'
        self.dims = kwargs.pop('resolution', [100, 100])
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.sess = None
        choice='N'
        choice = input("Enable GPU mode (Y/n)? Select N if you don't have a GPU. ")
        while True:
            if choice == 'N' or choice == 'n':
                GPU_MODE=False
                print('CPU mode enabled, loading dummy image.....')
                break
            elif choice == 'Y' or choice == 'y':
                GPU_MODE=True
                print('GPU mode enabled..\n')
                break
            else:
                print('Try again (Invalid input).')
        if GPU_MODE:
            global graph,model
            tf.reset_default_graph()
            graph = tf.get_default_graph()
            from .gpri_helper import model
            initializer = tf.global_variables_initializer()
            self.sess = tf.Session()
            self.sess.run(initializer)
        

    def generate(self, idx, *args,**kwargs):
        """Random image generator.
        """
        PATH = str(self.folder)
        NAME = str("GPRI_%s.png" % (time.time()))
            
        if GPU_MODE:
            truncate=0.8
            noise=0
            n_samples=1
            print(idx)
            idx_cat = idx
            with graph.as_default():
                z = model.truncated_z_sample(n_samples, truncate, noise)
                y = idx_cat
                ims = model.sample(self.sess, z, y, truncate)
            print('Saving image.....')
            image = cv2.cvtColor(ims[0], cv2.COLOR_BGR2RGB)
            cv2.imwrite(f"{PATH}\{NAME}", image)
        else:
            return (os.path.join(PATH, "babylon_drawing.jpg"))
        return os.path.join(PATH, NAME)


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
        with open(f"{self.folder}\categories.txt", "r") as file:
            buffer = file.read()
            cat = buffer.split("\n")
        for pairs in word_pairs:
            noun = pairs[0]
            print(noun)
            if noun == "animal":
                idx = int(random.choice(animal_idxs))    
            elif noun == "activity":
                idx = int(random.choice(activity_idxs))
            else:
                idx = -1 #CheeseBurger
            break #taking the first pair for now
        if idx == -1:
            print("Category not available yet as, category annotation is pending, returning yummy cheeseburger.... (Try animal/activity only)")
            ret = [(w, {'evaluation': self.evaluate(w)}) for w in [self.generate(933) for _ in range(number_of_artifacts)]]
        else:
            ret = [(w, {'evaluation': self.evaluate(w)}) for w in [self.generate(idx) for _ in range(number_of_artifacts)]]
