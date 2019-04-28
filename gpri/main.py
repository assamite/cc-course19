"""Group GPRI's main file.

Contains initialize- and create-functions.
"""

import os
import sys
import numpy as np
import numpy.random as npr
import tensorflow as tf
import cv2
import logging
from google_images_download import google_images_download
import shutil


#silence tensorflow spurious-warnings
tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.disable(logging.WARNING)
logging.getLogger('tensorflow').disabled = True

#silence keras messages
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
sys.stderr = stderr

animal_idxs = np.arange(398)
activity_idxs = np.arange(398, 1000)


class RandomImageCreator:

    def __init__(self, *args, **kwargs):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """
        print("/----------------Group GPRI initialize----------------/")

        # Each creator should have domain specified: title, poetry, music, image, etc.
        self.domain = 'image'
        self.dims = kwargs.pop('resolution', [128, 128])
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.sess = None
        self.GPU_MODE = False

        #load style transfer module
        global style_transfer
        from .gpri_helper import style_transfer

        # Check if user wants to use GPU:
        choice = input("Enable GPU mode for BigGAN (Y/N)?")

        while True:
            if choice == 'Y' or choice == 'y':
                self.GPU_MODE = True
                print('GPU mode enabled..')
                global graph_GAN, model
                tf.reset_default_graph()
                graph_GAN = tf.Graph()
                from .gpri_helper import model
                initializer = tf.global_variables_initializer()
                self.sess = tf.Session()
                self.sess.run(initializer)
                break
            elif choice == 'N' or choice == 'n':
                self.GPU_MODE = False
                print('GPU mode disabled, a dummy image is required here: gpri/images/content.jpg .....')
                break
            else:
                choice = input("Invalid input, Try again..")

    def generate(self, *args, **kwargs):
        """Random image generator.
        """
        emotion, word_pairs= args
        #generate content image at images/content
        self.generate_contentImage(emotion, word_pairs)
        #generate style image at images/style
        #styleImage = self.generate_styleImage(emotion)
        #Apply style-transfer to n - generated images for an emotion and n word pairs in images/output, alpha [0,1] (higher means more style)

        images_dir = self.folder + "/images"
        os.makedirs(images_dir, exist_ok = True)

        content_images_path = self.folder + "/images/content.jpg"
        style_images_path   = self.folder + "/images/style.jpg"
        output_images_path  = self.folder + "/images/output.jpg"

        style_transfer.stylize(alpha=0.1,content_path = content_images_path, style_path = style_images_path, output_path = output_images_path)

        if self.GPU_MODE:
            return output_images_path
        return output_images_path

    '''
    def generate_styleImage(self, emotion):
        """
        Generate the content image for the style transfer.
        :param emotion: Emotion input
        :return:
            Nothing for the moment.
        """
        si.create_styleImage((128, 128), 180, 15, 5, 10)
        # Now the style image is available as numpy array. What to do next?
        # Get the style transfer working, and get the entire pipeline working..
        return None
    '''
    def get_googleStyleImage(self, emotion, property_):
        """
        Fetch the style image for the style transfer.
        :param emotion: Emotion input and noun property
        :return:
            medium sized style image that captures specified emotion and property.
        """
        response = google_images_download.googleimagesdownload()
        arguments = {"keywords":f"{property_} {emotion} abstract art",
                     "limit":1,
                     "size":"medium",
                     "format":"jpg",
                     "color_tye":"full-color",
                     "type":"photo",
                     "output_directory":f"{str(self.folder)}",
                     "image_directory":"images/google_style_dump"}
        path = response.download(arguments)
        path = [k for k in path.values()]
        #rename the downloaded styleImage to a proper name
        try:
            style_images_path   = self.folder + "/images/style.jpg"
            shutil.move(str(path[0][0]), style_images_path)
        except:
            pass

    def generate_contentImage(self, emotion, word_pairs):
        """
        Generates the intial image, the content image in terms of style
        transfer, from the 'noun' input variable. Currently only supports a
        sample image.
        :param word_pairs: Word pairs input
        :return:
            String with file path
        """
        PATH = self.folder + '/images/content.jpg'

        with open(f"{self.folder}/categories.txt", "r") as file:
            buffer = file.read()
            cat = buffer.split("\n")
        for pairs in word_pairs:
            noun, property_ = pairs
            self.get_googleStyleImage(emotion, property_)
            NAME = str(f"GPRI_{noun}_{property_}_0.png")
            if noun == "animal":
                idx = int(npr.choice(animal_idxs))
            elif noun == "activity":
                idx = int(npr.choice(activity_idxs))
            else:
                idx = -1  # CheeseBurger
            break  # taking the first pair for now

        if self.GPU_MODE:

            truncate = 0.3
            noise = 0
            n_samples = 1
            idx_cat = idx
            with graph_GAN.as_default():
                z = model.truncated_z_sample(n_samples, truncate, noise)
                y = idx_cat
                ims = model.sample(self.sess, z, y, truncate)
            print(f'Saving image content image .....')
            image = cv2.cvtColor(ims[0], cv2.COLOR_BGR2RGB)
            cv2.imwrite(PATH, image)

        return PATH

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
        print("Group Example create with input args: {} {}".format(emotion,
                                                                   word_pairs))

        ret = [(w, {'evaluation': self.evaluate(w)}) for w in
               [self.generate(emotion, word_pairs) for _ in
                range(number_of_artifacts)]]

        print('-' * 100)
        print('-' * 100)

        print(ret)
        print('-' * 100)
        print('-' * 100)
        return ret
